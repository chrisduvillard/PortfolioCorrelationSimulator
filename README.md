
# PortfolioCorrelationSimulator

A Streamlit application that simulates the performance of a synthetic asset portfolio based on user-defined parameters.

## Features

- **Customizable Parameters**: Adjust the number of assets (1 to 20), average correlation between assets (-1 to 1), mean return, volatility, and investment horizon (1 to 10 years).
- **Interactive Charts**: Visualize asset performance and portfolio metrics using Plotly line charts.
- **Comprehensive Metrics**: Analyze key performance indicators such as Total Cumulative Return, Annualized Return, Annualized Volatility, Maximum Drawdown, Sharpe Ratio, Sortino Ratio, and Calmar Ratio.
- **User-Friendly Interface**: Simple and intuitive controls using Streamlit's interactive widgets.

## Installation

### Prerequisites

- Python 3.7 or higher

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/PortfolioCorrelationSimulator.git
   cd PortfolioCorrelationSimulator
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application with the following command:

```bash
streamlit run src/app.py
```

This will launch the Streamlit application in your default web browser.

## Project Structure

```
PortfolioCorrelationSimulator/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   ├── app.py
│   ├── utils.py (if applicable)
│   └── __init__.py
├── data/ (if applicable)
└── tests/ (if applicable)
```

## Dependencies

- **Streamlit**: Web application framework for Python.
- **NumPy**: Fundamental package for numerical computations.
- **Pandas**: Data manipulation and analysis library.
- **Plotly**: Interactive graphing library.
- **SciPy**: Library for scientific and technical computing.

All dependencies are listed in `requirements.txt` and can be installed via `pip`.

## Features in Detail

### Customizable Parameters

- **Number of Assets**: Choose between 1 to 20 assets.
- **Average Correlation**: Set the average correlation between assets, ranging from -1 to 1.
- **Number of Years to Plot**: Select the investment horizon from 1 to 10 years.
- **Mean Daily Return (%)**: Specify the expected mean daily return.
- **Daily Volatility (%)**: Define the daily volatility of the assets.
- **Risk-Free Rate (%)**: Input the risk-free rate for Sharpe and Sortino ratio calculations.

### Interactive Charts

- **Asset Price Simulation**: Visualize the simulated price paths of individual assets and the equally weighted portfolio.
- **Dynamic Updates**: Charts update in real-time as you adjust the parameters.

### Performance Metrics

- **Total Cumulative Return**: Overall return over the investment period.
- **Annualized Return**: Average yearly return.
- **Annualized Volatility**: Yearly volatility of returns.
- **Maximum Drawdown**: Largest peak-to-trough decline.
- **Sharpe Ratio**: Risk-adjusted return measure.
- **Sortino Ratio**: Variation of Sharpe Ratio considering downside risk.
- **Calmar Ratio**: Measures return relative to maximum drawdown.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

   Click on the 'Fork' button at the top right of the repository page to create a copy on your account.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/PortfolioCorrelationSimulator.git
   cd PortfolioCorrelationSimulator
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

4. **Commit Your Changes**

   ```bash
   git commit -am 'Add some feature'
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

6. **Open a Pull Request**

   Go to the original repository and open a pull request from your feature branch.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact me at [your.email@example.com].

## Acknowledgments

- **Streamlit Community**: For providing an excellent framework for rapid application development.
- **Financial Modeling Resources**: For inspiration on financial metrics and portfolio simulations.

## Screenshots

![App Image](./image.png)

## Author

Made with ❤️ by [Chris](https://github.com/chrisduvillard)

## Acknowledgments

- Streamlit
- Plotly