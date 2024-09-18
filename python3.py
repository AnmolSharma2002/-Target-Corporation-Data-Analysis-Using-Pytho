import pandas as pd
import matplotlib.pyplot as plt
import seaborn as snb
import mysql.connector 
import numpy as np
db = mysql.connector.connect(host = "localhost" , 
                             username = "root" ,
                             password = "Anmol1123@#" , 
                             database = "ecommerce")   #This is used to establish connection with mysql 
cur = db.cursor()
#Query 7--> Find the average number of products per order, grouped by customer city.
print("Query 7--->")
query7 = """ with count_per_order as (SELECT 
orders.order_id , orders.customer_id , count(order_items.order_id) as Order_Count
from  orders join order_items 
on orders.order_id = order_items.order_id
group by
orders.order_id ,orders.customer_id) 
Select customers.customer_city , round(avg(count_per_order.Order_Count),2) as Average_Orders
from customers join count_per_order
on customers.customer_id = count_per_order.customer_id
group by customers.customer_city 
order by Average_Orders DESC
"""
cur.execute (query7)
Average_Number_of_products = cur.fetchall()
df  = pd.DataFrame(Average_Number_of_products , columns=["Customer city" , "Average Products/Order"])
df= df.head(10)    #To print top 10 of the  cities as per average orders
print(df)

#Query 8--> Calculate the percentage of total revenue contributed by each product category.

query8 = """ SELECT
upper(products.product_category) AS category ,
Round((SUM(payments.payment_value)/(Select 
sum(payment_value) from payments))*100 , 2) as sales_percentage 
FROM 
products
JOIN 
order_items ON products.product_id = order_items.product_id
JOIN
payments ON payments.order_id = order_items.order_id
GROUP BY
category
order by sales_percentage desc;
"""
cur.execute (query8)
revenue = cur.fetchall()
df1 = pd.DataFrame(revenue , columns=["Category" , "Percetage(%)"])
print(" ")
print("Query 8--->")
print(df1.head())

#Query 9---> Identify the correlation between product price and the number of times a product has been purchased. 

query9 = """ SELECT
products.product_category , count(order_items.product_id) ,
round(avg(order_items.price),2)
from products join order_items
on products.product_id = order_items.product_id
group by products.product_category ;
"""
cur.execute (query9)
price = cur.fetchall()
print(" ")
print("Query 9--> ")
df2 = pd.DataFrame(price , columns=["Category" , "Order_Count" ,"Price"])
arr1 = df2["Order_Count"]
arr2 = df2["Price"]
k = np.corrcoef([arr1 ,arr2])
print(df2)
print("The corelation of the price and number of items bought is" , k[0][1])