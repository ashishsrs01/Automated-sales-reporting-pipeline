import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Business dashboard colors
PRIMARY = "#2f6fed"
MUTED = "#7b8494"
DANGER = "#e05252"
TEXT = "#172033"


def _save_figure(figure, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, bbox_inches="tight", dpi=150, transparent=True)
    plt.close(figure)
    return output_path


def _format_revenue(value, _position=None):
    """Format revenue values using business-friendly Indian units."""
    value = float(value)
    absolute_value = abs(value)

    if absolute_value >= 1e7:
        return f"₹{value / 1e7:.1f} Cr"
    if absolute_value >= 1e5:
        return f"₹{value / 1e5:.1f} L"
    if absolute_value >= 1e3:
        return f"₹{value / 1e3:.1f} K"

    return f"₹{value:.0f}"


def _add_bar_labels(axis, bars):
    """Add formatted revenue labels to vertical bars."""
    for bar in bars:
        value = bar.get_height()
        axis.annotate(
            _format_revenue(value),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color=TEXT,
            fontweight="bold",
        )


def _add_horizontal_bar_labels(axis, bars):
    """Add formatted revenue labels to horizontal bars."""
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
            color=TEXT,
            fontweight="bold",
        )


def _mark_unknown_bars(axis, bars, labels):
    """Visually distinguish bars representing missing/unknown data."""
    for bar, label in zip(bars, labels):
        if str(label).strip().lower() == "unknown":
            bar.set_color("#e7ebf0")
            bar.set_edgecolor("#cbd1db")
            bar.set_hatch("////")


def _style_axis(axis, horizontal=False):
    """Apply consistent executive-report styling."""
    if horizontal:
        axis.grid(axis="x", linestyle="-", color="#e7ebf0", alpha=0.7)
        axis.grid(axis="y", visible=False)
    else:
        axis.grid(axis="y", linestyle="-", color="#e7ebf0", alpha=0.7)
        axis.grid(axis="x", visible=False)

    axis.set_axisbelow(True)

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    if horizontal:
        axis.spines["left"].set_visible(False)
        axis.spines["bottom"].set_color("#e7ebf0")
        axis.tick_params(axis="y", length=0, pad=8)
        axis.tick_params(axis="x", colors=MUTED, labelsize=9, length=0, pad=6)
    else:
        axis.spines["bottom"].set_visible(False)
        axis.spines["left"].set_visible(False)
        axis.tick_params(axis="x", length=0, pad=8)
        axis.tick_params(axis="y", colors=MUTED, labelsize=9, length=0, pad=6)

    axis.xaxis.label.set_color(MUTED)
    axis.yaxis.label.set_color(MUTED)
    axis.xaxis.label.set_size(10)
    axis.yaxis.label.set_size(10)


def plot_monthly_revenue(report, output_dir):
    dataframe = report.tables.monthly_metrics.copy()

    figure, axis = plt.subplots(figsize=(8, 4.5))

    months = dataframe["Month"].astype(str)
    revenue = dataframe["Revenue"]

    axis.plot(months, revenue, marker="o", linewidth=2.5, color=PRIMARY, markersize=5)

    axis.set_title(
        "Monthly Revenue",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=16,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis)

    latest_month = months.iloc[-1]
    latest_revenue = revenue.iloc[-1]
    axis.plot(latest_month, latest_revenue, marker="o", markersize=8, color=PRIMARY)

    axis.annotate(
        _format_revenue(latest_revenue),
        xy=(latest_month, latest_revenue),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color=PRIMARY,
    )

    percentage_change = revenue.pct_change()
    largest_decline_index = percentage_change.idxmin()

    if (
        largest_decline_index != revenue.index[0]
        and percentage_change.loc[largest_decline_index] < -0.1
    ):
        decline = percentage_change.loc[largest_decline_index]
        decline_month = months.loc[largest_decline_index]
        decline_rev = revenue.loc[largest_decline_index]
        axis.annotate(
            f"{decline:.0%} drop",
            xy=(decline_month, decline_rev),
            xytext=(0, -22),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=9,
            color=DANGER,
            fontweight="bold",
        )
        axis.plot(decline_month, decline_rev, marker="o", markersize=8, color=DANGER)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "monthly_revenue.png")


def plot_revenue_by_region(report, output_dir):
    dataframe = report.tables.by_region.sort_values("Revenue", ascending=True).copy()

    figure, axis = plt.subplots(figsize=(7, 4))

    labels = dataframe["Region"].astype(str)
    bars = axis.barh(labels, dataframe["Revenue"], color=PRIMARY, height=0.6)

    axis.set_title(
        "Revenue by Region",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=16,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _add_horizontal_bar_labels(axis, bars)
    _mark_unknown_bars(axis, bars, labels)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "revenue_by_region.png")


def plot_revenue_by_category(report, output_dir):
    dataframe = report.tables.by_category.sort_values("Revenue", ascending=True).copy()

    figure, axis = plt.subplots(figsize=(7, 4))

    labels = dataframe["Category"].astype(str)
    bars = axis.barh(labels, dataframe["Revenue"], color=PRIMARY, height=0.6)

    axis.set_title(
        "Revenue by Category",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=16,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _add_horizontal_bar_labels(axis, bars)
    _mark_unknown_bars(axis, bars, labels)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "revenue_by_category.png")


def plot_top_products(report, output_dir, top_n=10):
    dataframe = (
        report.tables.by_product.sort_values("Revenue", ascending=False)
        .head(top_n)
        .sort_values("Revenue", ascending=True)
    )

    figure, axis = plt.subplots(figsize=(7, 4.5))

    bars = axis.barh(
        dataframe["Product"].astype(str),
        dataframe["Revenue"],
        color=PRIMARY,
        height=0.6,
    )

    axis.set_title(
        f"Top {top_n} Products by Revenue",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=16,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _add_horizontal_bar_labels(axis, bars)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "top_products.png")


def plot_salesperson_revenue(report, output_dir):
    dataframe = report.tables.by_salesperson.sort_values(
        "Revenue",
        ascending=True,
    ).copy()

    figure, axis = plt.subplots(figsize=(7, 4))

    labels = dataframe["Salesperson"].astype(str)
    bars = axis.barh(labels, dataframe["Revenue"], color=PRIMARY, height=0.6)

    axis.set_title(
        "Revenue by Salesperson",
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        pad=16,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _add_horizontal_bar_labels(axis, bars)
    _mark_unknown_bars(axis, bars, labels)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "salesperson_revenue.png")


def generate_all_charts(report, output_dir):
    return {
        "monthly_revenue": plot_monthly_revenue(report, output_dir),
        "revenue_by_region": plot_revenue_by_region(report, output_dir),
        "revenue_by_category": plot_revenue_by_category(report, output_dir),
        "top_products": plot_top_products(report, output_dir),
        "salesperson_revenue": plot_salesperson_revenue(report, output_dir),
    }
