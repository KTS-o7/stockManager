# Stock Manager: A Comprehensive Financial Analysis and Trading Platform

### Stats :

![GitHub Languages](https://img.shields.io/github/languages/count/KTS-o7/stockManager)
![GitHub Last Commit](https://img.shields.io/github/last-commit/KTS-o7/stockManager)
![GitHub Contributors](https://img.shields.io/github/contributors/KTS-o7/stockManager)
![GitHub top language](https://img.shields.io/github/languages/top/KTS-o7/stockManager)
![GitHub](https://img.shields.io/github/license/KTS-o7/stockManager)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FKTS-o7%2FstockManager&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Stock Manager is a cutting-edge financial analysis and trading platform designed to empower users with the tools they need to make informed decisions in the stock market. Built with a focus on simplicity and efficiency, our platform provides a wide range of features including real-time stock data, automated backtesting of trading strategies, and a user-friendly interface for managing portfolios.

Our platform is built on top of powerful technologies such as Python, Streamlit, Backtrader, and Yahoo Finance, ensuring a robust and reliable experience for users. Whether you're a seasoned trader or just starting out, Stock Manager is designed to cater to your needs.

## Features

- **Real-time Stock Data**: Access up-to-date information on stocks from major exchanges around the world.
- **Automated Backtesting**: Test your trading strategies against historical data to evaluate their performance.
- **Portfolio Management**: Add or remove stocks from your portfolio, view your portfolio's performance, and manage your trades efficiently.
- **User-friendly Interface**: Easily navigate through the platform with a clean and intuitive design.
- **Customizable Strategies**: Develop and implement your own trading strategies using our flexible framework.

## Installation

To get started with Stock Manager, follow these simple steps:

1. **Clone the Repository**: Use the following command to clone the repository to your local machine:
   ```
   git clone https://github.com/KTS-o7/stockManager.git
   ```
2. **Install Dependencies**: Navigate to the project directory and install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```
3. **Run the Application**: Start the Streamlit application by running the following command:
   ```
   streamlit run Home.py
   ```
   This will launch the Stock Manager platform in your default web browser.

## Usage

Once the application is running, you can start exploring the features of Stock Manager. Here's a quick guide to get you started:

- **Create Tables**: Use the create Table SQL script to create the tables in the database.
- **Sign In/Register**: Use the "Sign In" or "Register" buttons to log in or create a new account.
- **View Market Data**: Check the current levels of major market indices like NASDAQ, NYSE, and Nifty 50.
- **Manage Portfolio**: Add or remove stocks from your portfolio, view your portfolio's performance, and manage your trades.
- **Backtest Strategies**: Enter your trading strategy code and run backtests to evaluate its performance.

## Contributing

We welcome contributions from the community! If you're interested in contributing to Stock Manager, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Open a pull request with a detailed description of your changes.

## License

Stock Manager is open-source software licensed under the GNU General Public License, Version 3. This license ensures that you have the freedom to share and change all versions of the program, making it free software for all its users. For more details, please refer to the [LICENSE](LICENSE) file included in this repository.

---

**Note**:

- You need to replace the MongoDB URI in the `pages/Analysis.py` file with your own URI to connect to the database.
- You need to have the following as your sql database:
  - Database Name: STOCKMANAGER

```json
{
'user': 'mysql',
'password': 'mysql',
'host': '127.0.0.1',
'port': '3306',
'database': 'STOCKMANAGER',
'raise_on_warnings': True,
}
```
