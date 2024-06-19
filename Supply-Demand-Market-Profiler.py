import base64
import anthropic
import pandas as pd
from datetime import datetime, timedelta
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

# Parameters
initial_date = "3/2020"
n_days = 100
market_index = "S&P500"
n_categories = 10
pct_threshold = 5

# Claude API key
client = anthropic.Anthropic(api_key="your_api_key_here")

prompt = f"What type of specific products as of {initial_date} were with the most demand?"

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4000,
    temperature=0.8,
    system=
    f"""
    As an analyst in finance, list {n_categories} types or categories of products.
    also mention which companies provide these products or services - stocks must be from the {market_index} index.
    list it only in the following format for example:
    || 1. Products: products | Suppliers: stock symbol 1, stock symbol 2, stock symbol 3, stock symbol 4, stock symbol 5 || 2. Products: products | Suppliers: stock symbol 1, stock symbol 2, stock symbol 3, stock symbol 4, stock symbol 5 ||....
    """,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
)

# Extract the text content from the response
response_text = response.content

print(response_text)

ai_output = response_text

def check_stock_performance(stock_symbols, start_date, end_date):
    results = {}
    for symbol in stock_symbols:
        try:
            stock_data = yf.download(symbol, start=start_date, end=end_date)
            if not stock_data.empty:
                initial_close = stock_data['Close'].iloc[0]
                final_close = stock_data['Close'].iloc[-1]
                percentage_increase = ((final_close - initial_close) / initial_close) * 100
                if percentage_increase > pct_threshold:
                    results[symbol] = {
                        'initial_date': stock_data.index[0],
                        'initial_close': initial_close,
                        'final_date': stock_data.index[-1],
                        'final_close': final_close,
                        'percentage_increase': percentage_increase
                    }
        except Exception as e:
            print(f"Failed to download data for {symbol}: {e}")
    return results

# Extract stock symbols from the response text
stock_symbols = re.findall(r'\b[A-Z]{2,4}\b', str(ai_output))
print("Extracted stock symbols:", stock_symbols)

# Calculate the date range
start_date = datetime.strptime(initial_date, "%m/%Y")
end_date = start_date + timedelta(days=n_days)

# Check stock performance
performance_results = check_stock_performance(stock_symbols, start_date, end_date)
print("Performance results:", performance_results)

# Sort results by percentage increase in descending order
sorted_results = sorted(performance_results.items(), key=lambda x: x[1]['percentage_increase'], reverse=True)

# Print the products and suppliers
product_pattern = r'\|\|\s\d+\.\sProducts:\s([^\|]+)\s\|\sSuppliers:\s([^\|]+)\s\|\|'
products = re.findall(product_pattern, str(ai_output))
print("Parsed products and suppliers:", products)

product_dict = {}
for product in products:
    product_name = product[0].strip()
    suppliers = [s.strip() for s in product[1].split(",")]
    product_dict[product_name] = suppliers
    print(f"{product_name} | Suppliers: {', '.join(suppliers)}")

# Print sorted stock performance results
print("\nStock Performance (S&P 500):")
for symbol, data in sorted_results:
    initial_date_str = data['initial_date'].strftime('%Y-%m-%d')
    final_date_str = data['final_date'].strftime('%Y-%m-%d')
    print(f"Stock Symbol: {symbol}, Initial Date: {initial_date_str}, Initial Close: {data['initial_close']}, Final Date: {final_date_str}, Final Close: {data['final_close']}, Percentage Increase: {data['percentage_increase']:.2f}%")

# Plotting the stock performance results
if sorted_results:
    symbols, increases = zip(*[(symbol, data['percentage_increase']) for symbol, data in sorted_results])
    plt.figure(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab20', len(symbols)).colors
    bars = plt.bar(symbols, increases, color=colors[:len(symbols)])
    plt.xlabel('Stock Symbols')
    plt.ylabel('Percentage Increase')
    plt.title(f'Stock Performance (S&P 500) from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
    plt.xticks()
    for bar, increase in zip(bars, increases):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{increase:.2f}%', ha='center', va='bottom')
    plt.tight_layout()
    plt.show()
else:
    print("No stock performance data to plot.")

# Plotting products and their corresponding suppliers as bar chart with mean percentage increases
plt.figure(figsize=(12, 6))
product_names = list(product_dict.keys())
mean_increases = []
filtered_product_names = []
for product in product_names:
    percentages = [performance_results[supplier]['percentage_increase'] for supplier in product_dict[product] if supplier in performance_results]
    if percentages:
        mean_increases.append(np.mean(percentages))
        filtered_product_names.append(product)

if filtered_product_names:
    bars = plt.bar(filtered_product_names, mean_increases, color=plt.cm.tab20.colors[:len(filtered_product_names)])
    plt.xlabel('Products')
    plt.ylabel('Mean Percentage Increase')
    plt.title(f'Mean Percentage Increase for Product Categories from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
    plt.xticks(rotation=45, fontsize=10)
    for bar, mean_increase in zip(bars, mean_increases):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{mean_increase:.2f}%', ha='center', va='bottom')
    plt.tight_layout()
    plt.show()
else:
    print("No product performance data to plot.")

# Creating a heatmap for product suppliers performance
supplier_symbols = list({symbol for suppliers in product_dict.values() for symbol in suppliers})
heatmap_data = pd.DataFrame(index=filtered_product_names, columns=supplier_symbols)
for product in filtered_product_names:
    for supplier in supplier_symbols:
        if supplier in performance_results and supplier in product_dict[product]:
            heatmap_data.loc[product, supplier] = performance_results[supplier]['percentage_increase']

heatmap_data = heatmap_data.dropna(how='all', axis=1).dropna(how='all', axis=0).replace(0, np.nan)
heatmap_data = heatmap_data.astype(float)

if not heatmap_data.empty:
    # Define a function to format the annotations
    def annot_format(x):
        if np.isnan(x):
            return ""
        else:
            return f"{x:.2f}%"

    # Set up the figure and axis
    plt.figure(figsize=(12, 6))

    # Use a diverging colormap and set the color limits
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(
        heatmap_data,
        annot=heatmap_data.applymap(annot_format),
        fmt='',
        cmap=cmap,
        cbar=True,
        cbar_kws={'label': 'Percentage Increase'},
        center=0,
        linewidths=0.5,
        linecolor='black',
        annot_kws={'color': 'black'}
    )

    # Set the title and labels
    plt.title(f'Product Suppliers Performance Heatmap from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
    plt.xlabel('Suppliers')
    plt.ylabel('Products')

    # Adjust the layout for better fitting
    plt.tight_layout()
    plt.show()
else:
    print("No heatmap data to plot.")