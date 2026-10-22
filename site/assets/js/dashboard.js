const numberFormat = new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 });
const currencyFormat = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

function money(value) {
  return currencyFormat.format(Number(value) || 0);
}

function number(value) {
  return numberFormat.format(Number(value) || 0);
}

function percentage(value) {
  const formatted = `${Number(value) > 0 ? "+" : ""}${Number(value).toFixed(1)}%`;
  return formatted;
}

function setText(id, value) {
  document.getElementById(id).textContent = value ?? "Not available";
}

function append(parent, tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined && text !== null) element.textContent = String(text);
  parent.append(element);
  return element;
}

function svgElement(tag, attributes = {}) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [name, value] of Object.entries(attributes)) element.setAttribute(name, value);
  return element;
}

function renderTrend(rows) {
  const host = document.getElementById("trend-chart");
  if (!rows.length) return append(host, "p", "empty", "No monthly revenue data is available.");
  const width = 920;
  const height = 300;
  const margin = { top: 25, right: 20, bottom: 52, left: 76 };
  const values = rows.map((row) => Number(row.Revenue) || 0);
  const max = Math.max(...values, 1);
  const min = Math.min(...values, 0);
  const range = max - min || 1;
  const x = (index) => margin.left + (index * (width - margin.left - margin.right)) / Math.max(rows.length - 1, 1);
  const y = (value) => margin.top + ((max - value) * (height - margin.top - margin.bottom)) / range;
  const svg = svgElement("svg", { viewBox: `0 0 ${width} ${height}`, role: "presentation", "aria-hidden": "true" });
  const defs = svgElement("defs");
  const gradient = svgElement("linearGradient", { id: "trend-fill", x1: "0", x2: "0", y1: "0", y2: "1" });
  gradient.append(svgElement("stop", { offset: "0%", "stop-color": "#61c7b2", "stop-opacity": ".28" }));
  gradient.append(svgElement("stop", { offset: "100%", "stop-color": "#61c7b2", "stop-opacity": "0" }));
  defs.append(gradient);
  svg.append(defs);
  for (let i = 0; i < 4; i += 1) {
    const fraction = i / 3;
    const value = max - fraction * range;
    const yy = margin.top + fraction * (height - margin.top - margin.bottom);
    svg.append(svgElement("line", { x1: margin.left, x2: width - margin.right, y1: yy, y2: yy, class: "chart-gridline" }));
    const label = svgElement("text", { x: margin.left - 10, y: yy + 4, "text-anchor": "end", class: "chart-axis-text" });
    label.textContent = new Intl.NumberFormat("en-IN", { notation: "compact", maximumFractionDigits: 1 }).format(value);
    svg.append(label);
  }
  const points = values.map((value, index) => [x(index), y(value)]);
  const path = points.map(([xx, yy], index) => `${index ? "L" : "M"} ${xx} ${yy}`).join(" ");
  const area = `${path} L ${points.at(-1)[0]} ${height - margin.bottom} L ${points[0][0]} ${height - margin.bottom} Z`;
  svg.append(svgElement("path", { d: area, class: "trend-area" }));
  svg.append(svgElement("path", { d: path, class: "trend-path" }));
  points.forEach(([xx, yy], index) => {
    const point = svgElement("circle", { cx: xx, cy: yy, r: 5, class: "trend-point" });
    const tip = svgElement("title");
    tip.textContent = `${rows[index].Month}: ${money(values[index])}`;
    point.append(tip);
    svg.append(point);
    const label = svgElement("text", { x: xx, y: height - 22, "text-anchor": "middle", class: "chart-axis-text" });
    label.textContent = rows[index].Month;
    svg.append(label);
  });
  host.replaceChildren(svg);
}

function renderBars(hostId, rows, key, limit = 10) {
  const host = document.getElementById(hostId);
  const sorted = [...rows].sort((a, b) => Number(b.Revenue) - Number(a.Revenue)).slice(0, limit);
  if (!sorted.length) return append(host, "p", "empty", "No breakdown data is available.");
  const width = 650;
  const rowHeight = 37;
  const labelWidth = 140;
  const valueWidth = 95;
  const barWidth = width - labelWidth - valueWidth - 24;
  const svg = svgElement("svg", { viewBox: `0 0 ${width} ${sorted.length * rowHeight + 6}`, role: "presentation", "aria-hidden": "true" });
  const max = Math.max(...sorted.map((row) => Number(row.Revenue) || 0), 1);
  sorted.forEach((row, index) => {
    const yy = index * rowHeight + 5;
    const label = svgElement("text", { x: 0, y: yy + 15, class: "chart-axis-text" });
    label.textContent = String(row[key] ?? "Unknown");
    svg.append(label);
    svg.append(svgElement("rect", { x: labelWidth, y: yy + 3, width: barWidth, height: 13, rx: 6, class: "bar-track" }));
    const fill = svgElement("rect", { x: labelWidth, y: yy + 3, width: Math.max(3, (Number(row.Revenue) / max) * barWidth), height: 13, rx: 6, class: String(row[key]).toLowerCase() === "unknown" ? "bar-fill unknown" : "bar-fill" });
    const tip = svgElement("title");
    tip.textContent = `${row[key]}: ${money(row.Revenue)}`;
    fill.append(tip);
    svg.append(fill);
    const value = svgElement("text", { x: width, y: yy + 15, "text-anchor": "end", class: "chart-value-text" });
    value.textContent = money(row.Revenue);
    svg.append(value);
  });
  host.replaceChildren(svg);
}

function renderSignals(data) {
  const signals = [
    ["Leading region", data.insights.top_region],
    ["Leading category", data.insights.top_category],
    ["Top product", data.insights.top_product],
    ["Top salesperson", data.insights.top_salesperson],
    ["Best revenue month", data.insights.best_month],
  ];
  const host = document.getElementById("signal-list");
  signals.forEach(([label, value]) => {
    const row = append(host, "div", "signal");
    append(row, "span", "signal-label", label);
    append(row, "span", "signal-value", value || "Not available");
  });
}

function renderInsights(data) {
  const host = document.getElementById("insight-list");
  const rows = data.monthly_metrics;
  const last = rows.at(-1);
  const facts = [];
  if (!data.metadata.latest_period_complete) {
    facts.push(["Latest month may be partial", `Source activity ends ${data.metadata.reporting_end}; its month-over-month comparison is suppressed.`]);
  } else if (last && last.MoM_Growth !== null && Number.isFinite(Number(last.MoM_Growth))) {
    const direction = Number(last.MoM_Growth) < 0 ? "declined" : "increased";
    facts.push([`Latest observed month ${direction}`, `${last.Month}: revenue ${money(last.Revenue)}, ${percentage(last.MoM_Growth)} versus ${rows.at(-2)?.Month ?? "the prior observed month"}.`]);
  } else {
    facts.push(["Latest month comparison unavailable", "A valid prior-month revenue denominator is not available for comparison."]);
  }
  if (data.insights.strongest_growth_month) facts.push(["Strongest observed monthly growth", `${data.insights.strongest_growth_month}: ${percentage(data.insights.strongest_growth_rate)}.`]);
  if (data.insights.largest_decline_month) facts.push(["Largest observed monthly decline", `${data.insights.largest_decline_month}: ${percentage(data.insights.largest_decline_rate)}.`]);
  facts.forEach(([title, detail]) => {
    const row = append(host, "div", "insight-row");
    append(row, "strong", "", title);
    append(row, "span", "", detail);
  });
}

function renderRecommendations(items) {
  const host = document.getElementById("recommendation-list");
  if (!items.length) return append(host, "p", "empty", "No specific investigation prompts were generated for this period.");
  items.forEach((item) => {
    const card = append(host, "div", "recommendation");
    append(card, "span", "severity", item.severity);
    append(card, "strong", "", item.title);
    append(card, "p", "", item.description);
  });
}

function renderQuality(quality) {
  const host = document.getElementById("quality-grid");
  if (!quality) return append(host, "p", "empty", "Cleaning metrics are unavailable.");
  const metrics = [
    ["Source rows", quality.rows_before],
    ["Rows retained", quality.rows_after],
    ["Rows excluded", quality.rows_removed],
    ["Duplicate orders removed", quality.duplicates_removed],
    ["Missing dimensions filled", quality.missing_values_filled],
  ];
  metrics.forEach(([label, value]) => {
    const item = append(host, "div", "quality-item");
    append(item, "span", "quality-number", number(value));
    append(item, "span", "quality-label", label);
  });
}

function render(data) {
  setText("report-period", `${data.metadata.reporting_start} — ${data.metadata.reporting_end}`);
  setText("footer-period", `REPORTING PERIOD ${data.metadata.reporting_start} — ${data.metadata.reporting_end}`);
  setText("generated-at", `Data generated ${new Date(data.metadata.generated_at).toLocaleString()}`);
  if (!data.metadata.latest_period_complete) {
    setText("trend-copy", `Revenue by observed month. The latest month is partial through ${data.metadata.reporting_end}; its month-over-month change is suppressed.`);
  }
  setText("kpi-revenue", money(data.kpis.total_revenue));
  setText("kpi-orders", number(data.kpis.total_orders));
  setText("kpi-aov", money(data.kpis.average_order_value));
  const latest = data.monthly_metrics.at(-1);
  const growth = document.getElementById("kpi-growth");
  if (data.metadata.latest_period_complete && latest && latest.MoM_Growth !== null && Number.isFinite(Number(latest.MoM_Growth))) {
    growth.textContent = percentage(latest.MoM_Growth);
    growth.classList.add(Number(latest.MoM_Growth) >= 0 ? "positive" : "negative");
    setText("growth-note", `${latest.Month} vs ${data.monthly_metrics.at(-2)?.Month ?? "prior observed month"}`);
  } else {
    setText("kpi-growth", "N/A");
    setText("growth-note", data.metadata.latest_period_complete ? "Valid comparison unavailable" : "Latest reporting month may be partial");
  }
  renderTrend(data.monthly_metrics);
  renderBars("region-chart", data.by_region, "Region");
  renderBars("category-chart", data.by_category, "Category");
  renderBars("product-chart", data.by_product, "Product", 8);
  renderBars("sales-chart", data.by_salesperson, "Salesperson");
  renderSignals(data);
  renderInsights(data);
  renderRecommendations(data.recommendations);
  renderQuality(data.quality);
}

fetch("assets/data/dashboard.json")
  .then((response) => {
    if (!response.ok) throw new Error(`Dashboard data request failed (${response.status}).`);
    return response.json();
  })
  .then(render)
  .catch((error) => {
    const message = document.getElementById("load-error");
    message.hidden = false;
    message.textContent = `Dashboard data could not be loaded. ${error.message}`;
  });
