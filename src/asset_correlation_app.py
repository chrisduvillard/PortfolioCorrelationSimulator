import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import norm

# Set the page layout
st.set_page_config(layout="wide")

# Title
st.title("Synthetic Asset Portfolio Simulator")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")

# Number of assets
num_assets = st.sidebar.slider("Number of Assets", min_value=1, max_value=20, value=5)

# Correlation input
max_negative_correlation = -1 / (num_assets - 1) if num_assets > 1 else -1.0
correlation = st.sidebar.slider(
    "Average Correlation between Assets",
    min_value=max_negative_correlation,
    max_value=1.0,
    value=0.4,
    step=0.01,
    format="%.2f",
)

# Number of years
num_years = st.sidebar.slider("Number of Years to Plot", min_value=1, max_value=10, value=5)

# Simulation parameters
st.sidebar.header("Return Parameters")
mean_return = st.sidebar.number_input("Mean Daily Return (%)", value=0.05, step=0.01)
volatility = st.sidebar.number_input("Daily Volatility (%)", value=1.0, step=0.1)

# Convert percentages to decimals
mean_return /= 100
volatility /= 100

# Risk-free rate
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", value=0.0, step=0.01) / 100

# Generate the correlation matrix
def generate_correlation_matrix(n, corr):
    if n == 1:
        return np.array([[1.0]])
    else:
        corr_matrix = np.full((n, n), corr)
        np.fill_diagonal(corr_matrix, 1.0)
        return corr_matrix

# Ensure positive definiteness
def is_positive_definite(matrix):
    return np.all(np.linalg.eigvals(matrix) > 0)

corr_matrix = generate_correlation_matrix(num_assets, correlation)

# Check for positive definiteness
if not is_positive_definite(corr_matrix):
    st.error(
        f"The correlation matrix is not positive definite for correlation={correlation:.2f} "
        f"and number of assets={num_assets}. Please adjust the correlation."
    )
else:
    # Number of trading days
    trading_days = num_years * 252

    # Generate returns
    mean_vector = np.full(num_assets, mean_return)
    cov_matrix = corr_matrix * (volatility ** 2)

    returns = np.random.multivariate_normal(
        mean=mean_vector, cov=cov_matrix, size=trading_days
    )
    returns = pd.DataFrame(returns, columns=[f"Asset {i+1}" for i in range(num_assets)])

    # Calculate cumulative returns
    prices = (1 + returns).cumprod()
    prices *= 100  # Start prices at 100

    # Calculate portfolio
    portfolio = prices.mean(axis=1)
    prices["Portfolio"] = portfolio

    # Plot the time series
    st.header("Asset Price Simulation")
    fig = go.Figure()

    for column in prices.columns:
        fig.add_trace(go.Scatter(x=prices.index, y=prices[column], name=column))

    fig.update_layout(
        xaxis_title="Trading Days",
        yaxis_title="Price",
        legend_title="Assets",
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Calculate metrics
    st.header("Performance Metrics")

    def calculate_metrics(prices, returns):
        metrics = {}
        total_return = prices.iloc[-1] / prices.iloc[0] - 1
        annualized_return = (1 + total_return) ** (1 / num_years) - 1
        annualized_volatility = returns.std() * np.sqrt(252)
        max_drawdown = ((prices.cummax() - prices) / prices.cummax()).max()
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        downside_returns = returns.copy()
        downside_returns[downside_returns > 0] = 0
        downside_deviation = downside_returns.std() * np.sqrt(252)
        sortino_ratio = (annualized_return - risk_free_rate) / downside_deviation
        calmar_ratio = annualized_return / max_drawdown

        metrics["Total Cumulative Return"] = total_return
        metrics["Annualized Return"] = annualized_return
        metrics["Annualized Volatility"] = annualized_volatility
        metrics["Maximum Drawdown"] = max_drawdown
        metrics["Sharpe Ratio"] = sharpe_ratio
        metrics["Sortino Ratio"] = sortino_ratio
        metrics["Calmar Ratio"] = calmar_ratio

        return metrics

    metrics_data = []

    for column in returns.columns:
        metrics = calculate_metrics(prices[column], returns[column])
        metrics["Asset"] = column
        metrics_data.append(metrics)

    # Portfolio metrics
    portfolio_returns = portfolio.pct_change().dropna()
    portfolio_prices = portfolio.loc[portfolio_returns.index]
    portfolio_metrics = calculate_metrics(portfolio_prices, portfolio_returns)
    portfolio_metrics["Asset"] = "Portfolio"
    metrics_data.append(portfolio_metrics)

    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.set_index("Asset", inplace=True)

    # Format the dataframe
    metrics_df = metrics_df.applymap(lambda x: f"{x:.2%}" if isinstance(x, float) else x)

    st.dataframe(metrics_df)

    # Show correlation matrix
    st.header("Correlation Matrix")
    corr_df = pd.DataFrame(
        corr_matrix, columns=[f"Asset {i+1}" for i in range(num_assets)], index=[f"Asset {i+1}" for i in range(num_assets)]
    )
    st.dataframe(corr_df)
