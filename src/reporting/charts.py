import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def _save_figure(figure, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(figure)
    return output_path


def _format_revenue(value, _position=None):
    """Format revenue values using business-friendly Indian units."""
    value = float(value)
    absolute_value = abs(value)

    if absolute_value >= 1e7:
        return f"₹{value / 1e7:.2f} Cr"
    if absolute_value >= 1e5:
        return f"₹{value / 1e5:.2f} L"
    if absolute_value >= 1e3:
        return f"₹{value / 1e3:.1f} K"

    return f"₹{value:.0f}"


def _add_bar_labels(axis, bars):
    """Add formatted revenue labels to bar charts."""
    for bar in bars:
        value = bar.get_height()
        axis.annotate(
            _format_revenue(value),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def _add_horizontal_bar_labels(axis, bars):
    """Add formatted revenue labels to horizontal bar charts."""
    for bar in bars:
        value = bar.get_width()
        axis.annotate(
            _format_revenue(value),
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9,
        )


def _style_axis(axis):
    """Apply consistent executive-report styling."""
    axis.grid(axis="y", linestyle="--", alpha=0.25)
    axis.set_axisbelow(True)


def plot_monthly_revenue(report, output_dir):
    dataframe = report.tables.monthly_metrics.copy()

    figure, axis = plt.subplots(figsize=(10, 5))

    months = dataframe["Month"].astype(str)
    revenue = dataframe["Revenue"]

    axis.plot(months, revenue, marker="o", linewidth=2)

    axis.set_title("Monthly Revenue", fontsize=16, pad=12)
    axis.set_xlabel("Month")
    axis.set_ylabel("Revenue")

    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    axis.tick_params(axis="x", rotation=45)
    _style_axis(axis)

    # Highlight the lowest-revenue month as a potential anomaly.
    minimum_index = revenue.idxmin()
    minimum_revenue = revenue.loc[minimum_index]
    minimum_month = str(dataframe.loc[minimum_index, "Month"])

    axis.annotate(
        f"Lowest revenue\n{_format_revenue(minimum_revenue)}",
        xy=(minimum_month, minimum_revenue),
        xytext=(0, 35),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        arrowprops={"arrowstyle": "->"},
    )

    # Annotate the largest month-over-month decline.
    percentage_change = revenue.pct_change()
    largest_decline_index = percentage_change.idxmin()

    if largest_decline_index != revenue.index[0]:
        decline = percentage_change.loc[largest_decline_index]

        axis.annotate(
            f"MoM change: {decline:.1%}",
            xy=(
                str(dataframe.loc[largest_decline_index, "Month"]),
                revenue.loc[largest_decline_index],
            ),
            xytext=(0, -35),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            arrowprops={"arrowstyle": "->"},
        )

    figure.tight_layout()

    return _save_figure(
        figure,
        output_dir / "monthly_revenue.png",
    )


def plot_revenue_by_region(report, output_dir):
    dataframe = report.tables.by_region.sort_values("Revenue", ascending=False).copy()

    figure, axis = plt.subplots(figsize=(9, 5))

    bars = axis.bar(
        dataframe["Region"].astype(str),
        dataframe["Revenue"],
    )

    axis.set_title("Revenue by Region", fontsize=16, pad=12)
    axis.set_xlabel("Region")
    axis.set_ylabel("Revenue")

    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    axis.tick_params(axis="x", rotation=30)
    _style_axis(axis)
    _add_bar_labels(axis, bars)

    figure.tight_layout()

    return _save_figure(
        figure,
        output_dir / "revenue_by_region.png",
    )


def plot_revenue_by_category(report, output_dir):
    dataframe = report.tables.by_category.sort_values("Revenue", ascending=False).copy()

    figure, axis = plt.subplots(figsize=(9, 5))

    bars = axis.bar(
        dataframe["Category"].astype(str),
        dataframe["Revenue"],
    )

    axis.set_title("Revenue by Category", fontsize=16, pad=12)
    axis.set_xlabel("Category")
    axis.set_ylabel("Revenue")

    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    axis.tick_params(axis="x", rotation=30)
    _style_axis(axis)
    _add_bar_labels(axis, bars)

    figure.tight_layout()

    return _save_figure(
        figure,
        output_dir / "revenue_by_category.png",
    )


def plot_top_products(report, output_dir, top_n=10):
    dataframe = (
        report.tables.by_product.sort_values("Revenue", ascending=False)
        .head(top_n)
        .sort_values("Revenue")
    )

    figure, axis = plt.subplots(figsize=(10, 6))

    bars = axis.barh(
        dataframe["Product"].astype(str),
        dataframe["Revenue"],
    )

    axis.set_title(
        f"Top {top_n} Products by Revenue",
        fontsize=16,
        pad=12,
    )
    axis.set_xlabel("Revenue")
    axis.set_ylabel("Product")

    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis)
    _add_horizontal_bar_labels(axis, bars)

    figure.tight_layout()

    return _save_figure(
        figure,
        output_dir / "top_products.png",
    )


def plot_salesperson_revenue(report, output_dir):
    dataframe = report.tables.by_salesperson.sort_values(
        "Revenue",
        ascending=False,
    ).copy()

    figure, axis = plt.subplots(figsize=(9, 5))

    bars = axis.bar(
        dataframe["Salesperson"].astype(str),
        dataframe["Revenue"],
    )

    axis.set_title(
        "Revenue by Salesperson",
        fontsize=16,
        pad=12,
    )
    axis.set_xlabel("Salesperson")
    axis.set_ylabel("Revenue")

    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    axis.tick_params(axis="x", rotation=30)
    _style_axis(axis)
    _add_bar_labels(axis, bars)

    figure.tight_layout()

    return _save_figure(
        figure,
        output_dir / "salesperson_revenue.png",
    )


def generate_all_charts(report, output_dir):
    return {
        "monthly_revenue": plot_monthly_revenue(report, output_dir),
        "revenue_by_region": plot_revenue_by_region(report, output_dir),
        "revenue_by_category": plot_revenue_by_category(report, output_dir),
        "top_products": plot_top_products(report, output_dir),
        "salesperson_revenue": plot_salesperson_revenue(report, output_dir),
    }
