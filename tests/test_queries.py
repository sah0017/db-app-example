from models import Queries

# These pages only read data, so the tests don't need to clean anything up

def test_home_page_links_to_queries(client):
    response = client.get('/')
    assert b'href="/get_queries"' in response.data

def test_queries_page_links_to_each_query(client):
    response = client.get('/get_queries')
    assert response.status_code == 200
    assert b'href="/queries/top_customers"' in response.data
    assert b'href="/queries/store_rentals"' in response.data

def test_top_customers_returns_five_rows(app):
    customers = Queries.get_top5custs()
    assert len(customers) == 5
    # The query sorts by total spent, highest first
    totals = [row['total_spent'] for row in customers]
    assert totals == sorted(totals, reverse=True)

def test_top_customers_page_shows_customers(client):
    top_customer = Queries.get_top5custs()[0]

    response = client.get('/queries/top_customers')
    assert response.status_code == 200
    assert top_customer['customer_name'].encode() in response.data
    assert f"${top_customer['total_spent']:,.2f}".encode() in response.data

def test_store_rentals_returns_one_row_per_store(app):
    stores = Queries.get_avg_rental()
    assert len(stores) == 2

def test_store_rentals_page_shows_stores(client):
    response = client.get('/queries/store_rentals')
    assert response.status_code == 200
    for store in Queries.get_avg_rental():
        assert store['store_location'].encode() in response.data
