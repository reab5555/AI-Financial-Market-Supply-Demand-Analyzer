import gradio as gr
from data_processing import process_product_data, check_stock_performance
from visualization import plot_stock_performance, plot_product_performance, create_heatmap
from datetime import datetime, timedelta

MARKET_INDEX = "S&P500"


def analyze_stocks(year, month, day, n_days, n_categories, pct_threshold):
    # Process input
    initial_date = f"{year}-{month:02d}-{day:02d}"
    start_date = datetime(year, month, day)
    end_date = start_date + timedelta(days=n_days)

    # Get product data
    product_dict, stock_symbols = process_product_data(initial_date, n_categories, MARKET_INDEX)

    # Check stock performance
    performance_results = check_stock_performance(stock_symbols, start_date, end_date, pct_threshold)

    # Create visualizations
    stock_performance_plot = plot_stock_performance(performance_results, start_date, end_date)
    product_performance_plot = plot_product_performance(product_dict, performance_results, start_date, end_date)
    heatmap_plot = create_heatmap(product_dict, performance_results, start_date, end_date)

    # Prepare results text
    results_text = f"Stock Performance ({MARKET_INDEX}):\n"
    sorted_results = sorted(performance_results.items(), key=lambda x: x[1]['percentage_increase'], reverse=True)
    for symbol, data in sorted_results:
        initial_date_str = data['initial_date'].strftime('%Y-%m-%d')
        final_date_str = data['final_date'].strftime('%Y-%m-%d')
        results_text += f"Stock Symbol: {symbol}, Initial Date: {initial_date_str}, Initial Close: {data['initial_close']:.2f}, Final Date: {final_date_str}, Final Close: {data['final_close']:.2f}, Percentage Increase: {data['percentage_increase']:.2f}%\n"

    return results_text, stock_performance_plot, product_performance_plot, heatmap_plot


# Create lists for dropdown menus
current_year = datetime.now().year
current_month = datetime.now().month
years = list(range(2010, current_year + 1))
months = list(range(1, 13))
days = list(range(1, 32))

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Stock Market Analysis App")
    gr.Markdown(f"Analyze {MARKET_INDEX} stock performance based on product categories and market trends.")

    with gr.Row():
        year = gr.Dropdown(choices=years, value=current_year, label="Year", info="Select the year for analysis")
        month = gr.Dropdown(choices=months, value=current_month, label="Month", info="Select the month for analysis")
        day = gr.Dropdown(choices=days, value=1, label="Day", info="Select the day for analysis")

    n_days = gr.Slider(minimum=30, maximum=365, step=1, value=100, label="Number of Days",
                       info="The duration of the analysis period in days")
    n_categories = gr.Slider(minimum=5, maximum=20, step=1, value=10, label="Number of Categories",
                             info="The number of product categories to analyze")
    pct_threshold = gr.Slider(minimum=1, maximum=20, step=0.5, value=5, label="Percentage Threshold",
                              info="The minimum percentage increase for a stock to be included in the results")

    submit_button = gr.Button("Submit")

    results = gr.Textbox(label="Results")
    stock_performance = gr.Plot(label="Stock Performance")
    product_performance = gr.Plot(label="Product Performance")
    heatmap = gr.Plot(label="Performance Heatmap")

    submit_button.click(
        analyze_stocks,
        inputs=[year, month, day, n_days, n_categories, pct_threshold],
        outputs=[results, stock_performance, product_performance, heatmap]
    )

iface.launch()