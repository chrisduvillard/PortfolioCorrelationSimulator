import numpy as np
import pandas as pd
import plotly.graph_objects as go
from taipy.gui import Gui


def generate_data(N, rho_avg, Y):
    # Ensure the average correlation is within valid bounds
    rho_min = -1 / (N - 1) if N > 1 else -1
    if rho_avg < rho_min or rho_avg > 1:
        raise ValueError(f"Average correlation must be between {rho_min:.2f} and 1.")

    # Construct the correlation matrix
    R = (1 - rho_avg) * np.eye(N) + rho_avg * np.ones((N, N))

    # Set annualized volatility and compute daily volatility
    sigma_annual = 0.15  # 15% annual volatility
    sigma_daily = sigma_annual / np.sqrt(252)

    # Compute the covariance matrix
    Sigma = (sigma_daily ** 2) * R

    # Number of trading days
    D = 252
    T = Y * D

    # Generate returns
    mean_returns = np.zeros(N)
    returns = np.random.multivariate_normal(mean_returns, Sigma, size=T)

    # Compute cumulative returns
    prices = 100 * (1 + returns).cumprod(axis=0)

    # Equally weighted portfolio
    portfolio_returns = np.mean(returns, axis=1)
    portfolio_prices = 100 * (1 + portfolio_returns).cumprod()

    # Create a DataFrame with dates
    dates = pd.date_range(end=pd.Timestamp.today(), periods=T)
    prices_df = pd.DataFrame(prices, index=dates, columns=[f'Asset {i+1}' for i in range(N)])
    prices_df['Portfolio'] = portfolio_prices
    return prices_df


def calculate_metrics(returns, cumulative_returns, num_years):
    total_return = cumulative_returns[-1] / cumulative_returns[0] - 1
    annualized_return = (1 + total_return) ** (1 / num_years) - 1
    annualized_volatility = np.std(returns) * np.sqrt(252)
    cumulative_max = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_max - cumulative_returns) / cumulative_max
    max_drawdown = drawdown.max()
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else np.nan
    downside_returns = returns[returns < 0]
    downside_deviation = np.std(downside_returns) * np.sqrt(252)
    sortino_ratio = annualized_return / downside_deviation if downside_deviation != 0 else np.nan
    calmar_ratio = annualized_return / max_drawdown if max_drawdown != 0 else np.nan
    return {
        'Total Cumulative Return': total_return,
        'Annualized Return': annualized_return,
        'Annualized Volatility': annualized_volatility,
        'Maximum Drawdown': max_drawdown,
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Calmar Ratio': calmar_ratio
    }


def compute_metrics(prices_df, Y):
    metrics = {}
    for col in prices_df.columns:
        asset_prices = prices_df[col]
        asset_returns = asset_prices.pct_change().dropna()
        cumulative_returns = asset_prices.dropna()
        m = calculate_metrics(asset_returns.values, cumulative_returns.values, Y)
        metrics[col] = m
    metrics_df = pd.DataFrame(metrics).T
    return metrics_df


# Initialize variables at the module level
N = 5
rho_avg = 0.4
Y = 5

# Generate initial data
prices_df = generate_data(N, rho_avg, Y)
metrics_df = compute_metrics(prices_df, Y)

# Create initial Plotly figure
fig = go.Figure()
for col in prices_df.columns:
    fig.add_trace(go.Scatter(x=prices_df.index, y=prices_df[col], mode='lines', name=col))
fig.update_layout(title='Cumulative Returns', xaxis_title='Date', yaxis_title='Price')

# Define the 'on_generate' function before the GUI


def on_generate(state):
    try:
        # Cast slider values to appropriate types
        state.N = int(state.N)
        state.rho_avg = float(state.rho_avg)
        state.Y = int(state.Y)

        state.prices_df = generate_data(state.N, state.rho_avg, state.Y)
        state.metrics_df = compute_metrics(state.prices_df, state.Y)

        # Create Plotly figure
        fig = go.Figure()
        for col in state.prices_df.columns:
            fig.add_trace(go.Scatter(x=state.prices_df.index, y=state.prices_df[col], mode='lines', name=col))
        fig.update_layout(title='Cumulative Returns', xaxis_title='Date', yaxis_title='Price')
        state.fig = fig  # Assign Plotly figure to state
    except ValueError as e:
        state.dialog = str(e)


# Define GUI page content using the 'plot' control
page = """
# Asset Correlation Analyzer

### Select the Number of Assets:
<|{N}|slider|min=1|max=20|on_change=on_generate|>

### Select the Average Correlation:
<|{rho_avg}|slider|min=-1|max=1|step=0.01|on_change=on_generate|>

### Select the Number of Years to Plot:
<|{Y}|slider|min=1|max=10|on_change=on_generate|>

<|Generate Data|button|on_action=on_generate|>

## Cumulative Returns

<|{fig}|plot|>

## Metrics Table

<|{metrics_df}|table|width=100%|height=500px|>
"""

# Instantiate the GUI after all variables and functions are defined
gui = Gui(page)

# Run the application
gui.run(title="Asset Correlation Analyzer", dark_mode=False, use_reloader=False)
