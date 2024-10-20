SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS total_orders,
    SUM(oi.quantity * p.price) AS total_spent,
    EXTRACT(YEAR FROM o.order_date) AS order_year
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
LEFT JOIN 
    order_items oi ON o.order_id = oi.order_id
LEFT JOIN 
    products p ON oi.product_id = p.product_id
WHERE 
    c.status = 'active'
    AND o.order_date >= '2022-01-01'
GROUP BY 
    c.customer_id, c.first_name, c.last_name, EXTRACT(YEAR FROM o.order_date)
HAVING 
    SUM(oi.quantity * p.price) > 100
ORDER BY 
    total_spent DESC;

-- Subquery to get the top 5 customers based on total spent
WITH Top_Customers AS (
    SELECT 
        c.customer_id,
        SUM(oi.quantity * p.price) AS total_spent
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    JOIN 
        products p ON oi.product_id = p.product_id
    WHERE 
        o.order_date >= '2022-01-01'
    GROUP BY 
        c.customer_id
    ORDER BY 
        total_spent DESC
    LIMIT 5
)
SELECT 
    tc.customer_id,
    tc.total_spent,
    c.first_name,
    c.last_name
FROM 
    Top_Customers tc
JOIN 
    customers c ON tc.customer_id = c.customer_id;
