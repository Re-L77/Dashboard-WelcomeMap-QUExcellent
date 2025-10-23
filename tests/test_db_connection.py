import os
import pytest
import pyodbc

from app.models import db_connection as db_conn


def test_sql_server_connection():
    """Integration test: verify the app can connect to SQL Server using env vars.

    This test calls the existing `test_connection()` helper which attempts a pyodbc
    connection using environment variables (DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD).

    Note: This is an integration test that requires a running SQL Server reachable
    from the test runner. For local development, run the `db` service in docker compose
    before running pytest.
    """
    # Allow skipping in CI if env indicates no DB available
    if os.getenv("CI") == "true" or os.getenv("SKIP_DB_TESTS") == "1":
        pytest.skip("DB tests disabled in CI or by SKIP_DB_TESTS")

    # Ensure the required ODBC driver is present locally; pyodbc will fail with IM002 if not.
    required_driver = "ODBC Driver 18 for SQL Server"
    available = pyodbc.drivers()
    if required_driver not in available:
        pytest.skip(f"Required ODBC driver not found: {required_driver}. Available drivers: {available}")

    assert db_conn.test_connection() is True
