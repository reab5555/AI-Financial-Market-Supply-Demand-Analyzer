# Financial Market Demand and Supply Analyzer

This project is designed to identify the products or supplies with the most demand for a specific date period, determine the main suppliers of these products, and analyze their stock values. Additionally, it evaluates the percentage change in stock value from the demand period to a specified number of days afterward to assess how much these suppliers profited from the increased demand and subsequent sales.

## Features

- **Demand Identification:** Uses AI/LLM Claude model and prompt engineering to identify the products or categories with the highest demand for a given date range.
- **Supplier Analysis:** Identifies the main suppliers of the high-demand products and retrieves their stock values.
- **Profit Analysis:** Calculates the percentage change in stock value from the demand date to a specified number of days later, indicating the profit margin of the suppliers.

## How It Works

1. **Demand Identification:**
   - Utilizes the Claude AI model and prompt engineering techniques to analyze market data and identify high-demand products or categories for a given date period.
   
2. **Supplier and Stock Value Retrieval:**
   - Determines the main suppliers for the identified high-demand products.
   - Retrieves stock values for these suppliers during the specified date range.

3. **Profit Margin Calculation:**
   - Calculates the percentage change in stock values from the initial demand date to `X` days after.
   - Provides insights into how much the suppliers profited from the increased demand and product sales.

## Installation

To use this project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Stocks-Demand-Supply-Analysis.git

Navigate to the project directory:

bash

cd Stocks-Demand-Supply-Analysis

Install the required dependencies:

bash

    pip install -r requirements.txt

Usage

To run the analysis, execute the script with the following command:

bash

python Stocks_Demand_Supply.py

Make sure to update the script with the appropriate parameters for the date range and the number of days for profit analysis.
Configuration

The script requires configuration for:

    Date Period: The specific date range for identifying high-demand products.
    Number of Days for Analysis: The number of days after the demand date to analyze stock value changes.

Dependencies

    Python 3.x
    Claude AI/LLM
    Prompt Engineering Libraries

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
