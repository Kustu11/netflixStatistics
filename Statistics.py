"""
Main program for Netflix statistics
"""

#import modules
from pandas import *
from time import *
import matplotlib.pyplot as plt
from netflixToCSV import *

#Ask user info
print("Do you already have NetflixCSV.csv(Netflix history with additional info, like runtime?)")
isNetflixToCSV = int(input("Yes(1) or No(0): "))
if isNetflixToCSV == 0:
    isTrue = int(input('Are you sure? Yes(1) or No(0): '))
    if isTrue == 1:
        NetflixCsv()
df = read_csv("RuntimeCSV.csv",encoding = "UTF-8")

#Find and output statistics from pandas Dataframe
summ = df.sum(min_count=1)['Runtime']
sumMovie = df[df.isMovie == True].sum()["Runtime"]
sumTv = df[df.isMovie == False].sum()["Runtime"]
df['Date'] = to_datetime(df['Date'])
print("---------------------") # Total runtime 
print("Total runtime: ")
print(str(summ)+" minutes")
print(str(round(summ/60,2))+" hours")
print(str(round(summ/60/24,2))+" days")
print(str(round(summ/60/24/30,2))+" months")
print("---------------------") # Movies and tv runtime
print("Movies total runtime")
print(str(sumMovie)+" minutes")
print(str(round(sumMovie/60,2))+" hours")
print("Tv series total runtime:")
print(str(sumTv)+" minutes")
print(str(round(sumTv/60,2))+" hours")
print("---------------------") # Average runtimes
print("Average title runtime")
print(round(df["Runtime"].mean(),2))
print("Average movie runtime")
print(round(df[df.isMovie == True].mean()["Runtime"],2))
print("Average tv episode runtime")
print(round(df[df.isMovie == False].mean()["Runtime"],2))
print("Median title runtime")
print(int(df["Runtime"].median()))
print("Median movie runtime")
print(int(df[df.isMovie != False].quantile(.5)["Runtime"]))
print("Median tv episode runtime")
print(int(df[df.isMovie == False].quantile(.5)["Runtime"]))
print("---------------------") # First and last date 
print("First viewing date:")
print(min(df['Date']).strftime('%d %b %Y'))
print("Last viewing date:")
print(max(df['Date']).strftime('%d %b %Y'))
print("---------------------") # Money
print("Total time:")
numtest = (max(df['Date'])-min(df['Date']))
numMonth = int(numtest.days/30)
print(str(int(numtest.days/30))+" months paying")
print("Total if 12€/month: "+str(numMonth*12)+"€")
print("Same if 3€/month: "+str(numMonth*4)+"€")
print("12€/Month: "+str(round((numMonth*12)/(summ/60),3))+"€/Hour")
print("3€/Month: "+str(round((numMonth*3)/(summ/60),3))+"€/Hour")
print("---------------------") # Average info
print("Average hours per month: "+str(round((summ/60)/numMonth,2)))
print("Average minutes per day: "+str(round((summ)/(numtest.days),2)))
df_month = (df.resample('MS', on='Date')['Runtime'].sum().to_frame())
df_day = df.resample('D', on='Date')['Runtime'].sum().to_frame()
print("---------------------") # Most popular months
month_dict = df_month.nlargest(5,"Runtime")
month_dict["Runtime"] = round(month_dict["Runtime"]/60,1)
month_dict["Hours_per_Day"] = round(month_dict["Runtime"]/30,1)
print("Top 5 months(hours):")
print(month_dict)
print("---------------------") # Most popular days
day_dict = df_day.nlargest(10,"Runtime")
day_dict["Runtime"] = round(day_dict["Runtime"]/60,1)
print("Top 10 days(hours):")
print(day_dict)
print("---------------------") # Zero days/months
print('Months of 0 minutes')
print(str(df_month.shape[0]-df_month.astype(bool).sum(axis=0)['Runtime'])+'/'+str(numMonth))
print(str(round(((df_month.shape[0]-df_month.astype(bool).sum(axis=0))['Runtime'])*100/numMonth,2))+'%')

print('Days of 0 minutes')
print(str(df_day.shape[0]-df_day.astype(bool).sum(axis=0)['Runtime'])+'/'+str(numtest.days))
print(str(round((df_day.shape[0]-df_day.astype(bool).sum(axis=0)['Runtime'])*100/numtest.days,2))+'%')

genresBase = df["Genre"].value_counts().to_dict()
genres = {}
for i in genresBase:
    n = list(i.split(","))
    for j in n:
        if j not in genres:
            genres[j] = genresBase[i]
        else:
            genres[j] += genresBase[i]
print("---------------------") #Unique things
print("Unique titles:")
print(df["Title"].nunique())
print("Unique Tv series episodes:")
print(df["Tv"].nunique())
print("Unique Movies:")
print(df[df.isMovie == True].nunique()["Title"])
#print(df[df.isMovie == True].count()["isMovie"])
print("---------------------") #Popular genres
genresKey = sorted(genres, key=genres.get, reverse=True)[:5]
print("Top 5 genres:")
for i in genresKey:
    print(i,genres[i])
print("---------------------") # Popular series
tvDict = df["Tv"].value_counts()[:10].to_dict()
print("Top 10 series:")
for i in tvDict:
    print(i,tvDict[i])
print("---------------------")

# Shows tabels
# Create figure and plot space
"""
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(df_month.index.values,
        df_month['Runtime'],
        color='blue')

# Set title and labels for axes
ax.set(xlabel="Month",
       ylabel="Runtime",
       title="Netflix runtime per month")

fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(df_day.index.values,
        df_day['Runtime'],
        color='blue')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Runtime",
       title="Netflix runtime per day")
"""
plt.figure(figsize=(10, 10))

# Add x-axis and y-axis
plt.subplot(211)
plt.plot(df_month.index.values,
        df_month['Runtime'],
        color='blue')
plt.xlabel("Dates")
plt.ylabel("Minutes")
plt.title("Netflix runtime per month")
plt.grid(True)
# Set title and labels for axes
#plt.set(xlabel="Month",
#       ylabel="Runtime",
#       title="Netflix runtime per month")

plt.subplot(212)

# Add x-axis and y-axis
plt.plot(df_day.index.values,
        df_day['Runtime'],
        color='blue')

# Set title and labels for axes
#plt.set(xlabel="Date",
#       ylabel="Runtime",
#       title="Netflix runtime per day")
plt.xlabel("Dates")
plt.ylabel("Minutes")
plt.title("Netflix runtime per day")
plt.grid(True)

plt.show()
input()