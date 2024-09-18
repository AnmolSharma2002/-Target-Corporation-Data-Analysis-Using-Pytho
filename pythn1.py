import pandas as pd
import matplotlib.pyplot as plt
import seaborn as snb
import mysql.connector 

db = mysql.connector.connect(host = "localhost" , 
                             username = "root" ,
                             password = "Anmol1123@#" , 
                             database = "ecommerce")   #This is used to establish connection with mysql 
cur = db.cursor()


# query 1 to print the distinct cities of customers
print("Query 1-->")
query1 = """ select distinct customer_city  from customers"""
cur.execute (query1)
ditinct_citites = cur.fetchall()
df_start = pd.DataFrame(ditinct_citites)
print("ALL THE DISTINCT CITITES OF THE CUSTOMERS ARE" ,df_start.head())
#Query 2--> Count the number of orders placed in 2017
print("Query 2--->")
query2 = """ select count(order_id) from orders where year(order_purchase_timestamp) = 2017"""
cur.execute (query2)
count_of_orders = cur.fetchall()
print(count_of_orders[0][0])

#Query 3---> Find the total sales per catergory
print("Query 3 --->")
query3 = """ SELECT
upper(products.product_category) AS category ,
round(SUM(payments.payment_value) ,2) as sales 
FROM 
products
JOIN 
order_items ON products.product_id = order_items.product_id
JOIN
payments ON payments.order_id = order_items.order_id
GROUP BY
category; 
"""
cur.execute (query3)
sales = cur.fetchall()
df = pd.DataFrame(sales , columns=["Category" , "Sales"])
print(df)

#Query 4 --> CALCULATE THE PERCENTAGE OF ORDERS THAT WERE PAID IN INSTALLMENTS
print("Query 4 -->")
query4 = """ SELECT SUM(case when payment_installments>=1 then 1 else 0 end)/count(*)*100 from payments; 
"""
cur.execute (query4)
paid_in_installments = cur.fetchall()
df_1 = pd.DataFrame(paid_in_installments , columns=["Percentage(%)"])
print(df_1)

#Query 5 --->CALCULATE THE NUMBER OF CUSTOMERS FROM EACH STATE 
print("Query 5-->")
query5 = """ SELECT 
customer_state , COUNT(customer_id) as Number_of_Customers
FROM customers 
GROUP BY
customer_state
"""
cur.execute (query5)
Number_of_customers_in_each_state = cur.fetchall()
df2 = pd.DataFrame(Number_of_customers_in_each_state , columns=["Customer_State" , "Number_of_Customers"])
print(df2)
df2 = df2.sort_values(by= "Number_of_Customers" , ascending= False)
plt.figure(figsize=(9, 7))
plt.bar(df2["Customer_State"] ,df2["Number_of_Customers"])
plt.xticks(rotation = 90)
plt.xlabel("Customer_State")
plt.ylabel("Number_of_Customers")
plt.title("Number of Customers per State")
plt.show()
