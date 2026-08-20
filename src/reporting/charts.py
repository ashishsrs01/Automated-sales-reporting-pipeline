import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
BAR = "#93c5fd"
PRIMARY_FILL = "#dbeafe"
MUTED = "#64748b"
GRID = "#e2e8f0"
DANGER = "#dc2626"
TEXT = "#172033"
UNKNOWN = "#cbd5e1"


def _save_figure(figure, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_path,
        bbox_inches="tight",
        pad_inches=0.12,
        dpi=180,
        transparent=True,
    )
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
    for bar in bars:
        value = bar.get_height()
        axis.annotate(
            _format_revenue(value),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color=TEXT,
            fontweight="bold",
        )


def _add_horizontal_bar_labels(axis, bars):
    for bar in bars:
        value = bar.get_width()
        axis.annotate(
            _format_revenue(value),
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8.5,
            color=TEXT,
            fontweight="bold",
        )


def _mark_unknown_bars(axis, bars, labels):
    for bar, label in zip(bars, labels):
        if str(label).strip().lower() == "unknown":
            bar.set_color(UNKNOWN)
            bar.set_edgecolor(UNKNOWN)


def _ranked_bar_colors(values):
    colors = [BAR] * len(values)
    if colors:
        colors[-1] = PRIMARY
    return colors


def _style_axis(axis, horizontal=False):
    if horizontal:
        axis.grid(axis="x", linestyle="-", color=GRID, alpha=0.75, linewidth=0.8)
        axis.grid(axis="y", visible=False)
    else:
        axis.grid(axis="y", linestyle="-", color=GRID, alpha=0.75, linewidth=0.8)
        axis.grid(axis="x", visible=False)

    axis.set_axisbelow(True)

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    if horizontal:
        axis.spines["left"].set_visible(False)
        axis.spines["bottom"].set_color(GRID)
        axis.tick_params(axis="y", length=0, pad=7, labelsize=9)
        axis.tick_params(axis="x", colors=MUTED, labelsize=8.5, length=0, pad=6)
    else:
        axis.spines["bottom"].set_visible(False)
        axis.spines["left"].set_visible(False)
        axis.tick_params(axis="x", length=0, pad=7, labelsize=9)
        axis.tick_params(axis="y", colors=MUTED, labelsize=8.5, length=0, pad=6)

    axis.xaxis.label.set_color(MUTED)
    axis.yaxis.label.set_color(MUTED)
    axis.xaxis.label.set_size(9)
    axis.yaxis.label.set_size(9)


def _prepare_figure(size):
    figure, axis = plt.subplots(figsize=size)
    figure.patch.set_alpha(0)
    axis.set_facecolor("none")
    return figure, axis


def _set_horizontal_bar_limits(axis, values):
    maximum = max([float(value) for value in values] or [0])
    axis.set_xlim(left=0, right=maximum * 1.22 if maximum > 0 else 1)
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))


def plot_monthly_revenue(report, output_dir):
    dataframe = report.tables.monthly_metrics.copy()

    figure, axis = _prepare_figure((8, 4.2))

    months = dataframe["Month"].astype(str)
    revenue = dataframe["Revenue"]

    positions = list(range(len(months)))
    axis.plot(
        positions,
        revenue,
        marker="o",
        linewidth=2.5,
        color=PRIMARY,
        markersize=5,
        markerfacecolor="white",
        markeredgewidth=2,
        zorder=3,
    )
    axis.fill_between(positions, revenue, color=PRIMARY_FILL, alpha=0.3, zorder=1)
    axis.set_xticks(positions, labels=months)

    axis.set_title(
        "Monthly Revenue",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=14,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.yaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis)

    latest_position = len(months) - 1
    latest_revenue = revenue.iloc[-1]
    axis.axvspan(
        latest_position - 0.35,
        latest_position + 0.35,
        color="#f8fafc",
        zorder=0,
    )
    axis.plot(
        latest_position,
        latest_revenue,
        marker="o",
        markersize=8,
        color=PRIMARY_DARK,
        zorder=4,
    )

    axis.annotate(
        _format_revenue(latest_revenue),
        xy=(latest_position, latest_revenue),
        xytext=(-7, 10),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color=PRIMARY,
    )

    percentage_change = revenue.pct_change()
    largest_decline_index = percentage_change.iloc[1:].idxmin()

    if (
        largest_decline_index != revenue.index[0]
        and percentage_change.loc[largest_decline_index] < -0.1
    ):
        decline = percentage_change.loc[largest_decline_index]
        decline_position = dataframe.index.get_loc(largest_decline_index)
        decline_rev = revenue.loc[largest_decline_index]
        axis.annotate(
            f"{decline:.0%} drop",
            xy=(decline_position, decline_rev),
            xytext=(0, -18),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=8.5,
            color=DANGER,
            fontweight="bold",
        )
        axis.plot(
            decline_position,
            decline_rev,
            marker="o",
            markersize=8,
            color=DANGER,
            zorder=4,
        )

    axis.margins(x=0.04, y=0.18)
    figure.tight_layout()
    return _save_figure(figure, output_dir / "monthly_revenue.png")


def plot_revenue_by_region(report, output_dir):
    dataframe = report.tables.by_region.sort_values("Revenue", ascending=True).copy()

    figure, axis = _prepare_figure((7, 3.7))

    labels = dataframe["Region"].astype(str)
    bars = axis.barh(
        labels,
        dataframe["Revenue"],
        color=_ranked_bar_colors(dataframe["Revenue"]),
        height=0.6,
    )

    axis.set_title(
        "Revenue by Region",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=14,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _set_horizontal_bar_limits(axis, dataframe["Revenue"])
    _add_horizontal_bar_labels(axis, bars)
    _mark_unknown_bars(axis, bars, labels)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "revenue_by_region.png")


def plot_revenue_by_category(report, output_dir):
    dataframe = report.tables.by_category.sort_values("Revenue", ascending=True).copy()

    figure, axis = _prepare_figure((7, 3.7))

    labels = dataframe["Category"].astype(str)
    bars = axis.barh(
        labels,
        dataframe["Revenue"],
        color=_ranked_bar_colors(dataframe["Revenue"]),
        height=0.6,
    )

    axis.set_title(
        "Revenue by Category",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=14,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _set_horizontal_bar_limits(axis, dataframe["Revenue"])
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

    figure, axis = _prepare_figure((7, 4.2))

    bars = axis.barh(
        dataframe["Product"].astype(str),
        dataframe["Revenue"],
        color=_ranked_bar_colors(dataframe["Revenue"]),
        height=0.6,
    )

    axis.set_title(
        f"Top {top_n} Products by Revenue",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=14,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _set_horizontal_bar_limits(axis, dataframe["Revenue"])
    _add_horizontal_bar_labels(axis, bars)

    figure.tight_layout()
    return _save_figure(figure, output_dir / "top_products.png")


def plot_salesperson_revenue(report, output_dir):
    dataframe = report.tables.by_salesperson.sort_values(
        "Revenue",
        ascending=True,
    ).copy()

    figure, axis = _prepare_figure((7, 3.7))

    labels = dataframe["Salesperson"].astype(str)
    bars = axis.barh(
        labels,
        dataframe["Revenue"],
        color=_ranked_bar_colors(dataframe["Revenue"]),
        height=0.6,
    )

    axis.set_title(
        "Revenue by Salesperson",
        fontsize=13,
        fontweight="bold",
        color=TEXT,
        pad=14,
        loc="left",
    )
    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.xaxis.set_major_formatter(FuncFormatter(_format_revenue))

    _style_axis(axis, horizontal=True)
    _set_horizontal_bar_limits(axis, dataframe["Revenue"])
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
