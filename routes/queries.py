# Feature: Dashboard
# Read-only reports that join several tables.

from flask import Blueprint, render_template
from models import Queries

bp = Blueprint('queries', __name__)

# The link to this feature shown on every page: (label, endpoint)
NAV_LINK = ('Dashboard', 'queries.get_queries')

# ROUTE TO RENDER PAGE LISTING THE QUERIES
@bp.route('/get_queries')
def get_queries():
    return render_template('queries/index.html')

# ROUTE TO SHOW THE TOP 5 CUSTOMERS BY AMOUNT SPENT
@bp.route('/queries/top_customers')
def top_customers():
    customers = Queries.get_top5custs()
    return render_template('queries/top_customers.html', customers=customers)

# ROUTE TO SHOW RENTAL AND REVENUE TOTALS FOR EACH STORE
@bp.route('/queries/store_rentals')
def store_rentals():
    stores = Queries.get_avg_rental()
    return render_template('queries/store_rentals.html', stores=stores)
