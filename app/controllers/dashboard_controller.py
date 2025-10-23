from fastapi import APIRouter
import logging

# Simplified dashboard controller
# The main dashboard is now served as static HTML with frontend navigation
# This file remains for potential future API endpoints

router = APIRouter(prefix="/dashboard-api", tags=["Dashboard API"])
logger = logging.getLogger("dashboard_controller")

# Future API endpoints can be added here
# Currently, the dashboard.html is served statically with frontend-based navigation