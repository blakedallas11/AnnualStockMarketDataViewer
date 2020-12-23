import csv as csv
import itertools
import statistics
import numpy as np
import matplotlib as matplt
import matplotlib.pyplot as plt 


#opens the CSV file, turns it into a list of lists with tabs as the delimiter not commas
lol = list(csv.reader(open('S&P500_Returns_1926-2020.csv', 'rt'), delimiter='\t'))


#This gets the data starting in 1926 not in 2020
lol.reverse()


#gets the Average yearly returns from the whole 94 years
totalReturns = 0
for i in range(len(lol)-1):
	totalReturns = totalReturns + float(lol[i][1])
totalReturns = totalReturns / 94
print("Average Gains over past 94 years: " + str(round(totalReturns,2)) + "%")


#function that gets the final value of an investment over the specified interval of years
def calculateReturns(initialAmount, startYear, endYear, lists):
	
	investmentAmount = initialAmount
	for row in itertools.islice(lists , startYear, endYear + 1):
		percentChange = float(row[1])
		capitalGains = 1 + (percentChange / 100)
		investmentAmount = investmentAmount * capitalGains
	try:
		#print(str(lists[startYear][0]) + "-" + str(lists[endYear][0]) + "\t" + str(f"{investmentAmount:,.2f}"))
		return investmentAmount
	except:
		print("Something Broke... Fix It")
	

#Runs the 30 year simulation

#list to hold all data 
dataFromEach30 = []
for i in range(len(lol)):
	if i <= (len(lol) - 31):
		dataFromEach30.append(calculateReturns(17000,i,i + 30,lol))


#Changes data type from string
for i in range(len(dataFromEach30)):
	float(dataFromEach30[i])
	round(dataFromEach30[i],2)
	

#finds min, max, and variance of the data
print("Minimum Balance: " + str(f"{min(dataFromEach30):,.2f}"))
print("Maximum Balance: " + str(f"{max(dataFromEach30):,.2f}"))
print("Standard Deviation: " + str(f"{np.std(dataFromEach30):,.2f}"))


#creates a list of the years in the data to be used for plot y axis
years = []
for i in range(65):
	years.append((1956 + i))


# Data for plotting
t = years
s = dataFromEach30


fig, ax = plt.subplots()
ax.plot(t, s)
#keeps the y axis from being in scientific notation
ax.ticklabel_format(useOffset=False)
ax.ticklabel_format(style='plain')


#puts commas in the large numbers on y axis
ax.get_yaxis().set_major_formatter(
    matplt.ticker.FuncFormatter(lambda x, p: format(float(x), ',')))


#horizontal lines to show total cost of mortgage if 3% down and 20% down
ax.axhline(y=182405.00)
ax.axhline(y=119566.02)


#sets titles
ax.set(xlabel='time', ylabel='Investment value (after 30yrs)',
       title='Value of Investment portfolio started at $17,000')
ax.grid()


#shows graph
fig.savefig("test.png")
plt.show()
