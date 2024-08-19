import yfinance as yf
from llm_config import get_product_data


def process_product_data(initial_date, n_categories, market_index):
    product_data = get_product_data(initial_date, n_categories, market_index)

    product_dict = {}
    stock_symbols = set()

    for category in product_data.categories:
        product_dict[category.category] = category.suppliers
        stock_symbols.update(category.suppliers)

    return product_dict, list(stock_symbols)


def check_stock_performance(stock_symbols, start_date, end_date, pct_threshold):
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