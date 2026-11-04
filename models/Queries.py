from sqlalchemy import text
from core import ma, db

# These queries join several tables, so they are written in SQL with text()
# instead of using ORM classes. .mappings().all() turns the results into a
# list of rows that work like dicts, e.g. row['total_spent'] in Python or
# row.total_spent in a template.

def get_top5custs(): 
    top5custs = db.session.execute(text("""SELECT c.customer_id, 
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       city.city, 
       country.country,
       SUM(p.amount) AS total_spent
        FROM customer c
        JOIN address a ON c.address_id = a.address_id
        JOIN city ON a.city_id = city.city_id
        JOIN country ON city.country_id = country.country_id
        JOIN payment p ON c.customer_id = p.customer_id
        GROUP BY c.customer_id, city.city, country.country
        ORDER BY total_spent DESC
        LIMIT 5;"""))
    return top5custs.mappings().all()

def get_avg_rental(): 
    avg_rental = db.session.execute(text("""SELECT s.store_id,
       city.city AS store_location,
       COUNT(r.rental_id) AS total_rentals,
       AVG(DATEDIFF(r.return_date, r.rental_date)) AS avg_rental_days,
       SUM(p.amount) AS total_revenue,
       SUM(p.amount)/COUNT(r.rental_id) AS avg_revenue_per_rental
        FROM store s
        JOIN address a ON s.address_id = a.address_id
        JOIN city ON a.city_id = city.city_id
        JOIN inventory i ON s.store_id = i.store_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY s.store_id, city.city
        ORDER BY total_revenue DESC;"""))
    return avg_rental.mappings().all()
