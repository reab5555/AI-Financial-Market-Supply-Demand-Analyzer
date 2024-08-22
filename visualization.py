import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import colorsys


def generate_distinct_colors(n):
    HSV_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    RGB_tuples = [colorsys.hsv_to_rgb(*x) for x in HSV_tuples]
    return ['rgb({},{},{})'.format(int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)) for x in RGB_tuples]


def plot_stock_performance(performance_results, start_date, end_date):
    sorted_results = sorted(performance_results.items(), key=lambda x: x[1]['percentage_increase'], reverse=True)
    if sorted_results:
        symbols, increases = zip(*[(symbol, data['percentage_increase']) for symbol, data in sorted_results[:50]])  # Limit to top 50 performers
        colors = generate_distinct_colors(len(symbols))
        fig = go.Figure(data=[
            go.Bar(x=symbols, y=increases,
                   text=[f'{increase:.2f}%' for increase in increases],
                   textposition='auto',
                   marker_color=colors)
        ])
        fig.update_layout(
            title=f'Stock Performance (S&P 500) from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}',
            xaxis_title='Stock Symbols',
            yaxis_title='Percentage Increase',
            xaxis_tickangle=-45
        )
        return fig
    return go.Figure()


def plot_product_performance(product_dict, performance_results, start_date, end_date):
    product_names = list(product_dict.keys())
    mean_increases = []
    filtered_product_names = []
    for product in product_names:
        percentages = [performance_results[supplier]['percentage_increase'] for supplier in product_dict[product] if
                       supplier in performance_results]
        if percentages:
            mean_increases.append(np.mean(percentages))
            filtered_product_names.append(product)

    if filtered_product_names:
        colors = generate_distinct_colors(len(filtered_product_names))

        fig = go.Figure(data=[
            go.Bar(x=filtered_product_names, y=mean_increases,
                   text=[f'{increase:.2f}%' for increase in mean_increases],
                   textposition='auto',
                   marker_color=colors)
        ])
    
        fig.update_layout(
            title=f'Mean Percentage Increase for Product Categories from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}',
            xaxis_title='Products',
            yaxis_title='Mean Percentage Increase',
            xaxis_tickangle=-45
        )
        return fig
    return go.Figure()


def create_heatmap(product_dict, performance_results, start_date, end_date):
    supplier_symbols = list({symbol for suppliers in product_dict.values() for symbol in suppliers})
    heatmap_data = pd.DataFrame(index=product_dict.keys(), columns=supplier_symbols)
    for product, suppliers in product_dict.items():
        for supplier in suppliers:
            if supplier in performance_results:
                heatmap_data.loc[product, supplier] = performance_results[supplier]['percentage_increase']

    heatmap_data = heatmap_data.dropna(how='all', axis=1).dropna(how='all', axis=0).replace(0, np.nan)
    heatmap_data = heatmap_data.astype(float)

    if not heatmap_data.empty:
        fig = px.imshow(heatmap_data,
                        labels=dict(x="Suppliers", y="Products", color="Percentage Increase"),
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        color_continuous_scale='Greens',
                        aspect="auto")

        fig.update_layout(
            title=f'Product Suppliers Performance Heatmap from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}',
            xaxis_title='Suppliers',
            yaxis_title='Products'
        )

        return fig
    return go.Figure()