import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_csv("data/Online_Retail.csv", delimiter=",", encoding="ISO-8859-1")


#Dropping unnecessary columns (InvoiceNo, StockCode, CustomerID, Country) not required for revenue analysis.
df=df.drop(columns=["InvoiceNo","StockCode","CustomerID","Country"],axis=1)

#Converting the InvoiceDate column to datetime format for proper time series analysis.
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"],format="%m/%d/%y %H:%M")


monthly_data={}
month_names = {1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june", 7: "july", 8: "august", 9: "september", 10: "october", 11: "november", 12: "december"}

# Collecting data for each month of 2011 into a dictionary.
for i in range(1,13):
    key_name="{}_2011_data".format(month_names[i])

    filter=(df["InvoiceDate"].dt.year==2011) & (df["InvoiceDate"].dt.month==i)

    monthly_data[key_name] = df[filter].copy()


# Calculating the 'Revenue' column (Quantity * UnitPrice) for each month.
for i in range(1,13):
    key_name="{}_2011_data".format(month_names[i])

    quantity=monthly_data[key_name]["Quantity"]
    unit_price=monthly_data[key_name]["UnitPrice"]
    monthly_data[key_name]["Revenue"]=quantity*unit_price

# Grouping by 'Description' and summing the 'Revenue' for identical products in each month.
for i in range(1,13):
    key_name="{}_2011_data".format(month_names[i])

    monthly_data[key_name]=monthly_data[key_name].groupby("Description")["Revenue"].sum()


for i in range(1,13):
    key_name="{}_2011_data".format(month_names[i])
    monthly_data[key_name]=monthly_data[key_name].reset_index()
    monthly_data[key_name].columns=["Description","Revenue"]
    monthly_data[key_name]=monthly_data[key_name].sort_values(by="Revenue",ascending=False)

#Identifying the top 3 highest-selling products by revenue for each month.
monthly_top_3_products={}
for month,value in monthly_data.items():
    monthly_top_3_products[month]=value.head(3)


#To improve graph readability, product names are being found and shortened.

products=set()
for month,value in monthly_top_3_products.items():
    products.update(value["Description"])

product_short_name = {
    "REGENCY CAKESTAND 3 TIER": "CAKESTAND 3 TIER",
    "WHITE HANGING HEART T-LIGHT HOLDER": "HEART T-LIGHT HOLDER",
    "PICNIC BASKET WICKER 60 PIECES": "WICKER BASKET 60PC",
    "SET OF TEA COFFEE SUGAR TINS PANTRY": "TEA SUGAR TINS SET",
    "PAPER CHAIN KIT 50'S CHRISTMAS": "PAPER CHAIN CHRISTMAS",
    "DOTCOM POSTAGE": "POSTAGE",
    "JUMBO BAG RED RETROSPOT": "JUMBO BAG RED",
    "ASSORTED COLOUR BIRD ORNAMENT": "BIRD ORNAMENT",
    "VINTAGE UNION JACK MEMOBOARD": "UNION JACK MEMOBOARD",
    "PARTY BUNTING": "PARTY BUNTING",
    "RABBIT NIGHT LIGHT": "RABBIT NIGHT LIGHT",
}
#Applying the shortened names to the top 3 products data.
for month, df_top3 in monthly_top_3_products.items():
    df_top3["Description"] = df_top3["Description"].replace(product_short_name)

#Plotting the top 3 revenue-generating products for each month of 2011.
plt.figure(figsize=(18, 20))
for i in range(1,13):
    key_name="{}_2011_data".format(month_names[i])
    month=key_name.strip().split("_")[0].capitalize()


    plt.subplot(3,4,i)
    plt.bar(
        monthly_top_3_products[key_name]["Description"],
        monthly_top_3_products[key_name]["Revenue"],
        color=["b","g","r"],
    )
    plt.title("{}".format(month),fontsize=12)
    plt.xticks(rotation=90, ha='center', fontsize=6)
    plt.yticks([0, 10000, 20000, 30000, 40000])
    plt.suptitle("Top 3 Products by Monthly Revenue (2011)",fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(hspace=1)
    plt.savefig('Figure_1.png')
plt.show()


# ANNUAL REVENUE ANALYSIS (TOP 10)

#Combining all monthly dataframes into a single list
yearly_data=[]
for data in monthly_data.values():
    yearly_data.append(data)

yearly_data=pd.concat(yearly_data,ignore_index=True)

#Summing revenue for the same products across the entire year and sorting descending.
yearly_data=yearly_data.groupby("Description")["Revenue"].sum().reset_index()
yearly_data=yearly_data.sort_values(by="Revenue",ascending=False)
#Selecting the top 10 products with the highest total annual revenue.
top_10_yearly_products=yearly_data.head(10)

#Plotting the top 10 revenue-generating products for the entire year 2011.
plt.figure(figsize=(12,6))
plt.bar(
    top_10_yearly_products["Description"],
    top_10_yearly_products["Revenue"],
    color="green"
)
plt.title("Top 10 Revenue-Generating Products in 2011")
plt.xlabel("Product")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45,ha="right",fontsize=5)
plt.tight_layout()
plt.savefig('Figure_2.png')
plt.show()
