import pandas as pd
import matplotlib.pyplot as plt
import seaborn as snb
import mysql.connector 

db = mysql.connector.connect(host = "localhost" , 
                             username = "root" ,
                             password = "Anmol1123@#" , 
                             database = "ecommerce")   #This is used to establish connection with mysql 
cur = db.cursor()
 


#Query 6 --> Calculate The Amount of Orders Per Month in 2018
print("Query 6-->")
query6 = """ SELECT monthname(order_purchase_timestamp) AS Months , count(order_id) AS Total_Orders_Per_Month from orders where year(order_purchase_timestamp) =2018 
Group By Months
"""
cur.execute (query6)
Number_of_orders_per_month_in_2018 = cur.fetchall()
df3 = pd.DataFrame(Number_of_orders_per_month_in_2018 ,columns=["Month" , "Number of Orders"])
o = ["January" , "February" ,"March" , "April" ,"May" , "June" , "July" , "August" ,"September" ,"October", "November" ,"December" ]
ax= snb.barplot(x = df3["Month"] , y = df3["Number of Orders"] , data= df3 , order= o , color="Red")
plt.xticks(rotation = 45)
ax.bar_label(ax.containers[0])
plt.title("Amount of Orders in the Year 2018 According to Month")
plt.show()




