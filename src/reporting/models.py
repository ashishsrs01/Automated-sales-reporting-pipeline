from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.analytics.insights import BusinessInsights


@dataclass(frozen=True)
class ReportMetadata:
	"""Metadata describing the generated report."""

	title: str
	reporting_start: str
	reporting_end: str
	generated_at: str


@dataclass(frozen=True)
class KPISet:
	"""Executive-level business KPIs."""

	total_revenue: float
	total_orders: int
	total_units: int
	average_order_value: float


@dataclass(frozen=True)
class ReportTables:
	"""Tabular datasets used in the report."""

	by_region: pd.DataFrame
	by_category: pd.DataFrame
	by_product: pd.DataFrame
	by_salesperson: pd.DataFrame
	monthly_metrics: pd.DataFrame


@dataclass(frozen=True)
class Recommendation:
	"""A deterministic business recommendation."""

	title: str
	description: str
	severity: str


@dataclass(frozen=True)
class ReportData:
	"""Complete presentation-ready report data."""

	metadata: ReportMetadata
	kpis: KPISet
	tables: ReportTables
	insights: BusinessInsights
	recommendations: tuple[Recommendation, ...]
