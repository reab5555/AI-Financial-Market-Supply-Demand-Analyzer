# Financial Market Demand and Supply Analyzer
This project is designed to identify the markets or categories of products with the most demand for a specific date, determine the main suppliers of these products in the market, and analyze their stock values.

## Features
- **Demand Identification:** Uses Claude LLM model by Anthropic and prompt engineering to identify the products or categories with the highest demand for a given date range.
- **Supplier Analysis:** Identifies the main suppliers of the high-demand products and retrieves their stock values.
- **Profit Analysis:** Calculates the percentage change in stock value from the demand date to a specified number of days later, indicating the profit margin of the suppliers.
Using Claude Opus with Prompt Engineering

In the Financial Market Demand and Supply Analyzer, the Claude Opus model is utilized to identify products or categories with the highest demand. This involves crafting precise prompts to guide the model in generating the desired information.

## Prompt Engineering
Claude Opus is an advanced language model developed by Anthropic, designed for a variety of natural language processing tasks guided by prompts.   
Prompt engineering involves designing specific prompts that guide the language model to produce the required output. Here’s how it is applied in this project:   

### Define the Task:   
**User Prompt**   
*"What type of specific products as of {initial_date} were with the most demand?"*     
       
**System Prompt**  
"   
*As an analyst in finance, list {n_categories} types or categories of products.   
also mention which companies provide these products or services - stocks must be from the {market_index} index.*   
"      
       
### Specify the Model Output Format:  
"   
*list the results only in the following format for example:      
|| 1. Products: products | Suppliers: stock symbol 1, stock symbol 2, stock symbol 3, stock symbol 4, stock symbol 5   
|| 2. Products: products | Suppliers: stock symbol 1, stock symbol 2, stock symbol 3, stock symbol 4, stock symbol 5 ||....*    
"  
    
### Set Parameters:    
initial_date = "3/2020"   
n_days = 100   
market_index = "S&P500"   
n_categories = 10   
pct_threshold = 5   

