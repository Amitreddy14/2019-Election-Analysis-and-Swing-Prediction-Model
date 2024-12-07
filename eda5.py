#Q4: How many elected MPs have a criminal record and what is their party-wise distribution?

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

candidates = candidates_df[["STATE", "CONSTITUENCY", "NAME", "WINNER", "PARTY", "TOTAL VOTES"]]
candidates = candidates[candidates.NAME != "NOTA"]
# get all the candidates

# winners and runners_up -> temporary DataFrames

winners = candidates[candidates.WINNER == 1]
runners_up = candidates.loc[winners.index + 1]
# winners and runner ups in all seats

winners.reset_index(drop = True, inplace = True)
runners_up.reset_index(drop = True, inplace = True)
# reset index for better access

winners.drop(["WINNER"], axis = 1, inplace = True)
runners_up.drop(["WINNER"], axis = 1, inplace = True)
# drop the win indicator, we know who is who

# margin -> temporary DataFrame
margin = pd.DataFrame(winners["TOTAL VOTES"].to_numpy() - runners_up["TOTAL VOTES"].to_numpy(), columns = ["MARGIN OF VICTORY"])
# winning margin calculated, the order is preserved which helps us later 

# Some more processing done on the temporary DataFrames

winners.insert(3, "WINNER", winners["NAME"] + " (" + winners["PARTY"] + ")")
winners.drop(["NAME", "PARTY"], axis = 1, inplace = True)
winners.rename(columns = {'TOTAL VOTES' : "WINNER VOTES"}, inplace = True)
# Candidate name and Party in one column, drop the previous Name and Party columns and rename votes with winner votes

runners_up.insert(3, "RUNNER UP", runners_up["NAME"] + " (" + runners_up["PARTY"] + ")")
runners_up.drop(["NAME", "PARTY", "STATE", "CONSTITUENCY"], axis = 1, inplace = True)
runners_up.rename(columns = {'TOTAL VOTES' : "RUNNER-UP VOTES"}, inplace = True)
# Candidate name and Party in one column, drop the previous Name and Party columns and rename votes with runner-up votes
# STATE and CONSTITUENCY are dropped because they will be inherited from the 'winners' DataFrame

candidates = pd.concat([winners, runners_up, margin], axis = 1)
# the winners DataFrame and runners_up DataFrame are joined by the columns

lowest_margin = candidates.sort_values(by = "MARGIN OF VICTORY").head(10)
highest_margin = candidates.sort_values(by = "MARGIN OF VICTORY", ascending = False).head(10)
# get the 2 lists

# purely for aesthetics

lowest_margin.insert(2, "PLACE", lowest_margin.CONSTITUENCY + " (" + lowest_margin.STATE + ")")
lowest_margin.drop(["STATE", "CONSTITUENCY"], inplace = True, axis = 1)
lowest_margin.rename(columns = {"PLACE" : "CONSTITUENCY"}, inplace = True)
lowest_margin.index = np.arange(1,11)

# do some styling on both DataFrames for visual purposes

highest_margin.insert(2, "PLACE", highest_margin.CONSTITUENCY + " (" + highest_margin.STATE + ")")
highest_margin.drop(["STATE", "CONSTITUENCY"], inplace = True, axis = 1)
highest_margin.rename(columns = {"PLACE" : "CONSTITUENCY"}, inplace = True)
highest_margin.index = np.arange(1,11)

print(highest_margin)
'''We see from the table, as has been the case for most of the election, 
all 10 winners on the list are from BJP, while 9 of the 10 runners-up are from INC.
As we can infer from the table, Gujarat, Haryana, Rajasthan and NCT of Delhi saw the most one-sided contests.
C.R. Patil won by a record margin of more than 6.89 lakh votes from Navsari, Gujarat. 
BJP National President and future Home Minister Amit Shah won by more than 5.5 lakh votes from Gandhinagar, 
Gujarat.'''

print(lowest_margin)

'''
Compared to the table of the most One-Sided victories, 
the table of Closest victories consists of many different contests and in different regions of the country.
Island seats of Lakshadweep and Andaman & Nicobar Islands saw the 2nd and 4th most competitive contests with a margin of victory of 823 votes and 1407 votes respectively.
B.P. Saroj of BJP won the closest victory over Tribhuvan Ram of BSP with 181 votes in Machhlishahr, Uttar Pradesh.
'''