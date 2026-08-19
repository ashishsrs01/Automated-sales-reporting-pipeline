from pathlib import Path
import matplotlib.pyplot as plt
from src.reporting.models import ReportData

def _save_figure(figure, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close(figure)
    return output_path

def plot_monthly_revenue(report, output_dir):
    dataframe = report.tables.monthly_metrics
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(dataframe['Month'].astype(str), dataframe['Revenue'], marker='o')
    axis.set_title('Monthly Revenue')
    axis.set_xlabel('Month')
    axis.set_ylabel('Revenue')
    axis.tick_params(axis='x', rotation=45)
    return _save_figure(figure, output_dir / 'monthly_revenue.png')

def plot_revenue_by_region(report, output_dir):
    dataframe = report.tables.by_region
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(dataframe['Region'].astype(str), dataframe['Revenue'])
    axis.set_title('Revenue by Region')
    axis.set_xlabel('Region')
    axis.set_ylabel('Revenue')
    axis.tick_params(axis='x', rotation=30)
    return _save_figure(figure, output_dir / 'revenue_by_region.png')

def plot_revenue_by_category(report, output_dir):
    dataframe = report.tables.by_category
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(dataframe['Category'].astype(str), dataframe['Revenue'])
    axis.set_title('Revenue by Category')
    axis.set_xlabel('Category')
    axis.set_ylabel('Revenue')
    axis.tick_params(axis='x', rotation=30)
    return _save_figure(figure, output_dir / 'revenue_by_category.png')

def plot_top_products(report, output_dir, top_n=10):
    dataframe = report.tables.by_product.sort_values('Revenue', ascending=False).head(top_n).sort_values('Revenue')
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.barh(dataframe['Product'].astype(str), dataframe['Revenue'])
    axis.set_title(f'Top {top_n} Products by Revenue')
    axis.set_xlabel('Revenue')
    axis.set_ylabel('Product')
    return _save_figure(figure, output_dir / 'top_products.png')

def plot_salesperson_revenue(report, output_dir):
    dataframe = report.tables.by_salesperson.sort_values('Revenue', ascending=False)
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(dataframe['Salesperson'].astype(str), dataframe['Revenue'])
    axis.set_title('Revenue by Salesperson')
    axis.set_xlabel('Salesperson')
    axis.set_ylabel('Revenue')
    axis.tick_params(axis='x', rotation=30)
    return _save_figure(figure, output_dir / 'salesperson_revenue.png')

def generate_all_charts(report, output_dir):
    return {'monthly_revenue': plot_monthly_revenue(report, output_dir), 'revenue_by_region': plot_revenue_by_region(report, output_dir), 'revenue_by_category': plot_revenue_by_category(report, output_dir), 'top_products': plot_top_products(report, output_dir), 'salesperson_revenue': plot_salesperson_revenue(report, output_dir)}