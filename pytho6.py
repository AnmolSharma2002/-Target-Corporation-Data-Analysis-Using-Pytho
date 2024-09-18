import pandas as pd
import matplotlib.pyplot as plt
import seaborn as snb
import mysql.connector 

db = mysql.connector.connect(host = "localhost" , 
                             username = "root" ,
                             password = "Anmol1123@#" , 
                             database = "ecommerce")   #This is used to establish connection with mysql 
cur = db.cursor()


#Query14--> Calculate the retention rate of customers, defined as the percentage of customers who make another purchase within 6 months of their first purchase.
print("Query 14 --->")
query14 = """WITH a AS (
    SELECT customers.customer_id, 
           MIN(orders.order_purchase_timestamp) AS first_order
    FROM customers 
    JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.customer_id
),
b AS (
    SELECT a.customer_id, 
           COUNT(DISTINCT orders.order_purchase_timestamp) AS next_order 
    FROM a 
    JOIN orders ON orders.customer_id = a.customer_id
                AND orders.order_purchase_timestamp > a.first_order
                AND orders.order_purchase_timestamp < DATE_ADD(a.first_order, INTERVAL 6 MONTH)
    GROUP BY a.customer_id
)
SELECT 100 * COUNT(DISTINCT b.customer_id) / COUNT(DISTINCT a.customer_id) AS percentage
FROM a 
LEFT JOIN b ON a.customer_id = b.customer_id;
    
"""
cur.execute (query14)
Repeated = cur.fetchall()
df5 = pd.DataFrame(Repeated )
print(df5)

#Query15--> Identify the top 3 customers who spent the most money in each year.
print("Query 15-->")
query15 = """select years ,customer_id , payment , d_rank
from 
(Select year(orders.order_purchase_timestamp) years,
orders.customer_id,
sum(payments.payment_value) payment ,
dense_rank() over (partition by year(orders.order_purchase_timestamp)
order by sum(payments.payment_value) desc) d_rank
from orders join payments
on payments.order_id = orders.order_id
group by year(orders.order_purchase_timestamp) , 
orders.customer_id) as a  
where d_rank<=3;     
"""
cur.execute (query15)
Top_3 = cur.fetchall()
df6 = pd.DataFrame(Top_3 , columns=["years" , "Customer_id" , "Payment" ,"d_rank"])
print(df6)