import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np 
import time



def getBestSellers(df, quantity=10 , plotGraph = False):
    # Finds the top 10 sneakers with the best average resell value
    resell = df.groupby(['Sneaker Name'], as_index= True)['Sale Price', 'Retail Price'].mean()
    #retail = df.groupby(['Sneaker Name'])['Retail Price']
    resell['Sale Price'] = resell['Sale Price'] - resell['Retail Price']
    #resell['Profit'] = resell['Sale Price']/resell['Retail Price'] * 100
    resell = resell.nlargest(quantity, 'Sale Price' ,keep = 'first')
    #resell = resell.set_index('Sneaker Name')
    if plotGraph:
        resell.plot.barh(stacked = True)
        plt.show()
    return resell

def getMostSold(df, sList):
    # Finds the top 10 most traded sneakers during this time frame
    df = selectShoes(df, sList)
    avg = df.groupby(['Sneaker Name'], as_index=True)['Sale Price'].mean()
    df = df.groupby(['Sneaker Name']).size().reset_index(name='counts')
    df = pd.merge(df, avg, on='Sneaker Name')
    return df

def regionProfit(df, sList=""):
    # Returns in descending order which regions spent the most in sneaker purchases within the US
    if sList!="":
        df = selectShoes(df, sList)

    sum = df.groupby(['Buyer Region'])['Sale Price'].sum().reset_index(name='Total')
    count = df.groupby(['Buyer Region'])['Sale Price'].count().reset_index(name='count')
    result = pd.merge(sum, count, on='Buyer Region')
    result.sort_values(by=['Total'], inplace=True, ascending=False)
    result.set_index('Buyer Region')
    return result

def sizeDifference(df, name, plotGraph = False):
    # Returns DF with different size stats for each sneaker
    shoeMatch = df['Sneaker Name'] == name
    shoeDF = df[shoeMatch]
    #shoeDF = shoeDF['Sneaker Name, Shoe Size, Sale Price']
    sizeStat = shoeDF.groupby(['Shoe Size'])['Sale Price'].mean().reset_index(name= name)
    sizeCount = shoeDF.groupby(['Shoe Size'])['Sale Price'].count().reset_index(name='count')
    sizeResult = pd.merge(sizeStat, sizeCount, on='Shoe Size')
    #sizeStat = shoeDF.groupby(['Shoe Size'])['Sale Price'].max()
    if plotGraph:
        plt.plot(sizeStat['Shoe Size'],sizeStat[name], label="line 1")
        plt.show()
    return sizeStat

def demand(df, name="", plotGraph = False):
    # Finds most sold sneaker
    if name != "":
        shoeMatch = df['Sneaker Name'] == name
        shoeDF = df[shoeMatch]
    else:
        shoeDF = df
    demand = shoeDF.groupby(['Shoe Size'])['Sale Price'].count().reset_index(name='count')
    #demand.rename(columns={'Sale Price':'count'})
    if plotGraph:
        demand.plot.line()
        plt.show()
    return demand
    #df = df.groupby(['Shoe Size'])['Sale Price'].mean()
    #return df

def appraiseSize(df, slist, plotGraph = False):
    #Compares effect of size on price of sneaker
    set = pd.DataFrame()
    temp = pd.DataFrame()
    for x in range(len(slist)):
        if x == 0:
            set = sizeDifference(df,slist[x], False)
            #set.columns = [str(x)+"size" , slist[x]]
        else:
            set[slist[x]] = sizeDifference(df,slist[x], False)[slist[x]]
            #temp = sizeDifference(df,slist[x], False)
            #temp.columns = [str(x)+"size", slist[x]]
            #set = pd.concat([set, temp], axis=1)
            
    #set.set_index('Shoe Size')
    if plotGraph:
        set.plot.line()
        plt.show()
    return set

def sizeMatter(df):
    # Gets mean sell price for each size from all sneakers
    df = df.groupby(['Shoe Size'])['Sale Price'].mean().reset_index(name='avg')
    return df

def bigAnalysis(df):
    # Preforms an overall indepth analysis of sneaker data
    # Takes in DataFrame and plots results of analysis
    sizeDemand = demand(df)
    sd = sizeDemand.plot.bar(x='Shoe Size', y='count', title='Most Popular Shoe Size')
    sd.set_xlabel("Sneaker Size")
    sd.set_ylabel("Quantitiy Sold")

    # Calculate Profit per region
    region = regionProfit(df)
    rgn = region.plot.barh(x='Buyer Region', y='Total', title="Sale by Region")
    rgn.set_ylabel("Region")
    rgn.set_xlabel("Total Money Spent($1,000,000)")

    # Find top 7 shoe with highest return rate
    bestSell = getBestSellers(df, 7, False)
    bs = bestSell.plot.bar(title='Highest Profit Shoes')
    bs.set_xlabel("Sneaker Names")
    plt.xticks(rotation=10)
    bs.set_ylabel("Price in Dollars ($)")

    # Determine correlation between sneaker size and price
    sizeTrend = sizeMatter(df)
    st = sizeTrend.plot.line(x='Shoe Size', y='avg', title="Size vs Price")
    st.set_ylabel("Avg Price")
    sc = df.plot(kind='scatter', x="Shoe Size", y="Sale Price", title="Distribution of Sales")

    #Volatility = df.plot(kind='scatter', x="Order Date", y="Sale Price", title="Sales over time")

    sum = df.groupby(['Brand'])['Sale Price'].sum().reset_index(name='sum')
    quantity = df.groupby(['Brand'])['Sale Price'].count().reset_index(name='count')
    result = pd.merge(sum, quantity, on='Brand')

    axes = result.plot.bar(x='Brand',rot=0, subplots=True, title="Brand Profit Comparison")
    axes[1].legend(loc=2)

    plt.show()

def analysis(df, sList, plotGraph = False):
    # Preforms sneaker analysis on set of sneakers out of whole
    # Takes in Dataframe and filters data for sneakers in list
    # Plots result of analysis
    bestSell = getBestSellers(df, 4, False)
    mostPopular = getMostSold(df,sList)
    sizeDif = appraiseSize(df,sList, False)
    region = regionProfit(df,sList)
    oneSize = sizeDifference(df, "NA-Presto-OW")


    bs = bestSell.plot.bar(title='Highest return Shoes')
    bs.set_xlabel("Sneaker Names")
    plt.xticks(rotation=10)
    bs.set_ylabel("Price in Dollars ($)")

    mp = mostPopular.plot.bar(x='Sneaker Name', title='Highest yield')
    mp.set_xlabel("Sneaker Names")
    plt.xticks(rotation=10)
    mp.set_ylabel("Number Sold/Price")

    sd = sizeDif.plot.line(x='Shoe Size',title='Size Comaprison')

    os = oneSize.plot.line(x='Shoe Size', title='NA-Presto-OW')

    scatter= selectShoes(df, sList)
    scatterp = scatter.plot(kind='scatter', x='Order Date', y='Sale Price', title='Sales over time', rot=90)


    plt.show()

def selectShoes(df, sList):
    # Returns DF with only select sneakers
    set = pd.DataFrame()
    temp = pd.DataFrame()
    for x in range(len(sList)):
       temp = df.loc[df['Sneaker Name'] == sList[x]]
       if x == 0:
            set = temp
       elif x !=0:
            set = set.append(temp)
               
    return set





if __name__ == "__main__":
    #plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price")
    # Read in sneaker data from CSV and cleans it
    df = pd.read_csv('StockX-Data-Contest.csv')
    df['Sneaker Name']=df['Sneaker Name'].replace({'Adidas-Yeezy-Boost-350':'AYB350','Off-White':'OW','Air-Jordan-1':'AJ1','adidas-Yeezy-Boost-350':'aYB350','Nike-Air':'NA','Force':'F'}, regex=True)
    df['Sale Price']= df['Sale Price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Retail Price']= df['Retail Price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    #df['Order Date'] = pd.to_datetime(df['Order Date'])
    #df = getBestSellers(df, 5, False)
    #sList = bs['Sneaker Name'].to_List()
    #print(df)
    
    List = ["NA-Max-90-OW", "AJ1-Retro-High-OW-White",  "NA-Presto-OW", "AYB350-Low-Oxford-Tan"]
    theTen = ["Nike-Hyperdunk-OW", "Nike-Zoom-Fly-OW", "Nike-Blazer-OW", "Nike-Air-Presto-OW", "Nike-Air-Max-OW"]
    name = "NA-Presto-OW"
    name2 = "AJ1-Retro-High-Off-White-White"

    analysis(df,List, False)
    #bigAnalysis(df)
    #df = appraiseSize(df, List)
    #df = regionProfit(df, List)
    #df = df.groupby(['Buyer Region'])['Sale Price'].count().reset_index(name='sum')
    #print(df)
    #df = selectShoes(df, List)
    #df.plot.barh(x='Buyer Region', y='Total')
    #df.plot.hexbin(x='Order Date', y='Sale Price', gridsize=25)
    #df = selectShoes(df, name)
    #df.plot.scatter(x='Order Date', y='Sale Price')
    #plt.xticks(rotation=90)
    #print(df['Sneaker Name'])
    #plt.show()
    #df = demand(df)
    #df.plot.bar(x='Shoe Size', y='count')
    #plt.show()
    #df=sizeDifference(df, name)
    df = getMostSold(df, List)
    print(df)
    #df = appraiseSize(df, List, False)
    #df = sizeMatter(df)
    #df = getMostSold(df, List)




'''
    df1 = sizeDifference(df, name , False)
    df1.columns = ['name1 size','name1']
    df2 = sizeDifference(df, name2 , False)
    df2.columns = ['name2 size', 'name2']
    df3 = pd.concat([df2,df1], axis=1, sort=False)
    x1 = df3['name1 size']
    y1 = df3['name1']
    plt.plot(x1, y1, label = "line 1")
    x2 = df3['name2 size']
    y2 = df3['name2']
    plt.plot(x2, y2, label = "line 2")
    plt.legend()
    #plt.show()
'''

    #print(df3)
    #print(df2)

    #df2= getMostSold(df)
    #df = regionProfit(df)
    #print(df)
    #df.plot.barh(x="Buyer Region", y="count", title="plot")
    #plt.show(block=True)


