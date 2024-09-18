import pandas as pd
import matplotlib.pyplot as plt
import seaborn as snb
import mysql.connector 

db = mysql.connector.connect(host = "localhost" , 
                             username = "root" ,
                             password = "Anmol1123@#" , 
                             database = "ecommerce")   #This is used to establish connection with mysql 
cur = db.cursor()

#Query 11-->  Calculate the moving average of order values for each customer over their order history.


print("Query 11-->")
query11 = """Select customer_id , order_purchase_timestamp , avg(payment) over(partition by customer_id order by order_purchase_timestamp rows between 2 preceding and current row) as mov_avg from
(Select orders.customer_id , orders.order_purchase_timestamp , payments.payment_value as payment
from payments join orders
on payments.order_id = orders.order_id) as a;  
"""
cur.execute (query11)
moving_avg = cur.fetchall()
df2 = pd.DataFrame(moving_avg , columns=["customer_id" , "order_purchase_timestamp" , "Moving Average"])
print(df2)

#Query 12 --> alculate the cumulative sales per month for each year.
print("Query 12-->")
query12 = """Select years , months , payment ,sum(payment) over(order by years , months) as cumulative_sales from
(Select year(orders.order_purchase_timestamp) as years , month(orders.order_purchase_timestamp) as months,
round(sum(payments.payment_value) ,2) as payment from
orders join payments on orders.order_id = payments.order_id
group by years , months order by years , months) as a

"""
cur.execute (query12)
cumulative_sum = cur.fetchall()
df3= pd.DataFrame(cumulative_sum , columns=["Year" ,"Month" ,"Payments" ,"Cumulative_Sales"])
print(df3)


#Query 13--> Calculate the year-over-year growth rate of total sales.
print("Query 13-->")
query13 = """WITH a AS (
    SELECT YEAR(orders.order_purchase_timestamp) AS years,
           ROUND(SUM(payments.payment_value), 2) AS payment
    FROM orders
    JOIN payments ON orders.order_id = payments.order_id
    GROUP BY years
    ORDER BY years
)
SELECT years,
       ((payment - LAG(payment, 1) OVER (ORDER BY years)) / LAG(payment, 1) OVER (ORDER BY years)) * 100 AS payment_change
FROM a;
;
"""
cur.execute (query13)
Year_on_Year_Growth = cur.fetchall()
df4 = pd.DataFrame(Year_on_Year_Growth , columns=["Year" , "YoY(%) Growth"])
print(df4)
