# Flask Application for Financial Calculations

This web application, built with Flask, allows users to perform financial calculations such as savings interest analysis, expense tracking, and return on investment for real estate.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [License](#license)

## Project Description

The application provides users with tools to:
- Calculate the total savings profit, including capital gains tax.
- Analyze income versus expenses across various categories.
- Estimate the return period for real estate investments while accounting for fixed and variable costs.

## Features

1. **Savings Interest Calculation**:
   - Computes total profit from savings based on user inputs.
2. **Expense Analysis**:
   - Tracks income and expenses in different categories and calculates the net balance.
3. **Real Estate Investment Analysis**:
   - Calculates the return on investment period and projected profits.

## Requirements

- Python 3.x
- Flask
- HTML templates stored in the `templates` directory:
  - `index.html`
  - `oprocentowanie.html`
  - `suma.html`
  - `mieszkanie.html`

## Installation

1. Clone the repository:
```bash
   git clone <repository-url>
   cd <project-directory>
```
2. Install Flask:
```bash
   pip install -r requirements.txt
```
3. Ensure the HTML files are located in the `templates` directory.

## Running the Application

1. Run the application:
```bash
   python main.py
```
2. Open a browser and navigate to:
   http://127.0.0.1:5000/

3. Select a functionality from the homepage to perform calculations.

## Project Structure

project/
├── templates/                # Directory with HTML templates
│   ├── index.html            # Homepage
│   ├── oprocentowanie.html   # Savings calculation form
│   ├── suma.html             # Expense analysis form
│   └── mieszkanie.html       # Real estate investment form
├── main.py                    # Main Flask application file
└── README.md                 # Project documentation

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it.
