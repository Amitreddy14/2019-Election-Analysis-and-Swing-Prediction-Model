#Q3) What is the distribution of assets, liabilities and net worth of the elected MPs?


import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Load the election data
raw_election_data = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS_2.0.csv")

# Function to convert asset/liability values
def convert(x):
    if str(x)[0] == 'R':
        return float(str(x).split()[1].replace(",", ""))
    return 0.0 

# Apply conversion to ASSETS and LIABILITIES
raw_election_data.ASSETS = raw_election_data.ASSETS.apply(convert)
raw_election_data.LIABILITIES = raw_election_data.LIABILITIES.apply(convert)

# Adjusting WINNER column
raw_election_data.at[192, "WINNER"] = 1
raw_election_data.at[702, "WINNER"] = 1
raw_election_data.at[951, "WINNER"] = 1
raw_election_data.at[1132, "WINNER"] = 1
raw_election_data.at[172, "WINNER"] = 0

# Prepare candidates DataFrame
candidates_df = raw_election_data.drop(['SYMBOL', 'GENERAL\nVOTES', 'POSTAL\nVOTES',
                        'OVER TOTAL ELECTORS \nIN CONSTITUENCY', 'OVER TOTAL VOTES POLLED \nIN CONSTITUENCY'], axis=1)

# Rename columns for easier access
candidates_df.rename(columns={"CRIMINAL\nCASES": "CRIMINAL CASES", "TOTAL\nVOTES": "TOTAL VOTES"}, inplace=True)
candidates_df.sort_values(["STATE", "CONSTITUENCY"], inplace=True)

# Convert CRIMINAL CASES to numeric
candidates_df["CRIMINAL CASES"] = pd.to_numeric(candidates_df["CRIMINAL CASES"], errors='coerce').convert_dtypes()

# Filter out NOTA candidates
candidates_personal_df = candidates_df[candidates_df.NAME != "NOTA"]
candidates_personal_df = candidates_personal_df.drop(["TOTAL VOTES", "TOTAL ELECTORS"], axis=1)

# Winners DataFrame
winners_df = candidates_df[candidates_df.WINNER == 1].sort_values(["STATE", "CONSTITUENCY"]).reset_index()
winners_df.drop(["index", "WINNER"], axis=1, inplace=True)

winners_df.insert(11, "NET WORTH", winners_df["ASSETS"] - winners_df["LIABILITIES"])
# insert a new column called "NET WORTH", which is Assets - Liabilities

intervals = [5e6, 1e7, 5e7, 10e7, 25e7, 50e7, 100e7]
# money intervals

assets = winners_df["ASSETS"].sort_values()
liabilities = winners_df["LIABILITIES"].sort_values()
net_worth = winners_df["NET WORTH"].sort_values()
# individual columns extracted as Series

# helper function
def segregate(intervals, ownings):
    '''
    Function to return a list containing number of winners in each interval.

    intervals - list containing money intervals
    ownings - DataFrame containing data which is to be segregated into groups
    '''
    l = []
#     list to store the values
    l.append(ownings[ownings<=intervals[0]].count())
#     first entry
    
    for i in range(len(intervals)-1):
        l.append(ownings[(ownings > intervals[i]) & (ownings <= intervals[i+1])].count())
#         middle entries
        
    l.append(ownings[ownings>intervals[i+1]].count())
#     last entry
    return l

data = {"ASSETS" : segregate(intervals, assets),
        "LIABILITIES" : segregate(intervals, liabilities),
        "NET WORTH" : segregate(intervals, net_worth)}
# data generated 

worth_df = pd.DataFrame(data, index = ["<=50lac", ">50lac & <=1cr", ">1cr & <=5cr", ">5cr & <=10cr", ">10cr & <=25cr",
                           ">25cr & <=50cr", ">50cr & <=100cr", ">100cr"])
# new dataframe created

print(worth_df)
# Purely for visualization purposes

worth_df = worth_df.transpose()
# dataframe inverted for visualization purposes
worth_df.reset_index(inplace = True)
# index column added to the DataFrame

print(worth_df)

#Stacked Bar Chart, with each of ASSETS, LIABILITIES and NET WORTH as a vertical column 
# and showing different money intervals with different colors
sns.set_palette("tab10")
# set color sequence
worth_df.plot(x = "index", kind = 'bar', stacked = True, figsize = (6,9))
# plot a Stacked Bar chart

plt.xticks(rotation = 0)
plt.tick_params(labelsize = 14)
plt.xlabel(None)
plt.ylabel("No. of Candidates", fontsize = 15, labelpad = 14)
# plot detailing

plt.title("DISTRIBUTION OF ASSETS, LIABILITIES AND \nNET WORTH OF ALL WINNING CANDIDATES", fontsize = 15.25, 
           weight = 'bold')
plt.legend(fontsize = 13.5, bbox_to_anchor = [1.05,0.7]);
# title and legend placed at appropriate positions

# for the following process of writing data on the graph, I'm sure there must be some simpler annotation method, 
# but for now, I'm using the direct printing approach

# ASSETS
plt.figtext(0.232, 0.142, worth_df.loc[0]["<=50lac"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.185, worth_df.loc[0][">50lac & <=1cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.223, 0.345, worth_df.loc[0][">1cr & <=5cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.545, worth_df.loc[0][">5cr & <=10cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.645, worth_df.loc[0][">10cr & <=25cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.745, worth_df.loc[0][">25cr & <=50cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.790, worth_df.loc[0][">50cr & <=100cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.232, 0.823, worth_df.loc[0][">100cr"], color = 'white', fontsize = 12, weight = "bold");

# LIABILITIES
plt.figtext(0.485, 0.345, worth_df.loc[1]["<=50lac"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.490, 0.605, worth_df.loc[1][">50lac & <=1cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.490, 0.705, worth_df.loc[1][">1cr & <=5cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.490, 0.775, worth_df.loc[1][">5cr & <=10cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.490, 0.800, worth_df.loc[1][">10cr & <=25cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.58, 0.827, "}" + str(worth_df.loc[1][">25cr & <=50cr"]+worth_df.loc[1][">50cr & <=100cr"]+worth_df.loc[1][">100cr"]),
            color = 'black', fontsize = 12, weight = "bold");

# NET WORTH
plt.figtext(0.752, 0.148, worth_df.loc[2]["<=50lac"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.202, worth_df.loc[2][">50lac & <=1cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.743, 0.364, worth_df.loc[2][">1cr & <=5cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.555, worth_df.loc[2][">5cr & <=10cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.668, worth_df.loc[2][">10cr & <=25cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.754, worth_df.loc[2][">25cr & <=50cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.797, worth_df.loc[2][">50cr & <=100cr"], color = 'white', fontsize = 12, weight = "bold")
plt.figtext(0.752, 0.825, worth_df.loc[2][">100cr"], color = 'white', fontsize = 12, weight = "bold")
plt.show()

print("Percentage of MPs with Assets >1cr = ",
      round((542-(worth_df.at[0, "<=50lac"] + worth_df.at[0, ">50lac & <=1cr"]))/542*100, 2), "%", sep = "")
print("Percentage of MPs with Net Worth >1cr = ",
      round((542-(worth_df.at[2, "<=50lac"] + worth_df.at[2, ">50lac & <=1cr"]))/542*100, 2), "%", sep = "")

'''Percentage of MPs with Assets >1cr = 88.19%
Percentage of MPs with Net Worth >1cr = 84.87%
We infer, as per the popular opinion, an outrageous 88.19% of the elected MPs have Assets more than 1 crore, 
with 26 MPs being in the Super Rich category with more than 100 crores worth of Assets. 
An 84.87% of the elected MPs have a Net Worth of more than 1 crore, 
with 21 of them belonging to the Super Rich category with a Net Worth of more than 100 crores.'''

