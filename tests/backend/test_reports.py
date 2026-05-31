"""
Tests for reporting API endpoints (quarterly performance and monthly trends).

These also exercise the get_quarter() date-bucketing helper used by the
quarterly endpoint.
"""
import pytest


# Flattened set of YYYY-MM prefixes that map to a quarter (mirrors QUARTER_MAP).
QUARTER_MONTHS = {f"2025-{m:02d}" for m in range(1, 13)}
VALID_QUARTERS = {"Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"}


class TestQuarterlyReports:
    """Test suite for /api/reports/quarterly."""

    def test_get_quarterly_reports(self, client):
        """Test getting quarterly reports returns the expected structure."""
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for quarter in data:
            assert quarter["quarter"] in VALID_QUARTERS
            assert "total_orders" in quarter
            assert "total_revenue" in quarter
            assert "avg_order_value" in quarter
            assert "fulfillment_rate" in quarter
            assert quarter["total_orders"] > 0
            assert 0 <= quarter["fulfillment_rate"] <= 100

    def test_quarterly_reports_sorted(self, client):
        """Test that quarters are returned in ascending order."""
        data = client.get("/api/reports/quarterly").json()
        quarters = [q["quarter"] for q in data]
        assert quarters == sorted(quarters)

    def test_quarterly_avg_order_value_calculation(self, client):
        """Test avg_order_value equals total_revenue / total_orders."""
        data = client.get("/api/reports/quarterly").json()
        for quarter in data:
            expected = quarter["total_revenue"] / quarter["total_orders"]
            assert abs(quarter["avg_order_value"] - expected) < 0.01

    def test_quarterly_totals_match_orders(self, client):
        """Cross-validate: quarterly order counts match the underlying orders.

        Every order whose order_date falls in a 2025 quarter must be counted
        exactly once, which also confirms get_quarter() buckets correctly.
        """
        orders = client.get("/api/orders").json()
        expected_total = sum(
            1 for o in orders if o.get("order_date", "")[:7] in QUARTER_MONTHS
        )

        data = client.get("/api/reports/quarterly").json()
        reported_total = sum(q["total_orders"] for q in data)
        assert reported_total == expected_total


class TestMonthlyTrends:
    """Test suite for /api/reports/monthly-trends."""

    def test_get_monthly_trends(self, client):
        """Test getting monthly trends returns the expected structure."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for month in data:
            assert "month" in month
            assert "order_count" in month
            assert "revenue" in month
            assert "delivered_count" in month
            # month is YYYY-MM
            assert len(month["month"]) == 7
            assert month["month"][4] == "-"
            assert month["delivered_count"] <= month["order_count"]

    def test_monthly_trends_sorted(self, client):
        """Test that months are returned in ascending order."""
        data = client.get("/api/reports/monthly-trends").json()
        months = [m["month"] for m in data]
        assert months == sorted(months)

    def test_monthly_trends_total_matches_orders(self, client):
        """Cross-validate: monthly order counts sum to all dated orders."""
        orders = client.get("/api/orders").json()
        expected_total = sum(1 for o in orders if o.get("order_date"))

        data = client.get("/api/reports/monthly-trends").json()
        reported_total = sum(m["order_count"] for m in data)
        assert reported_total == expected_total
