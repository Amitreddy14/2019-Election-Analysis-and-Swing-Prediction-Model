#q2) Q1: Which States/UTs and Constituencies had the highest and the lowest Voter Turnout?
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

# Calculate Voter Turnout
total_voters = candidates_df.groupby(["STATE", "CONSTITUENCY"])[["TOTAL VOTES"]].sum()
total_electors = winners_df.groupby(["STATE", "CONSTITUENCY"])[["TOTAL ELECTORS"]].sum()
votes_df = total_voters.join(total_electors)
votes_df["VOTER TURNOUT"] = round(votes_df["TOTAL VOTES"] / votes_df["TOTAL ELECTORS"] * 100, 2)
votes_df = votes_df.rename(index={"Andaman & Nicobar Islands": "Andaman &\nNicobar Islands"})

# Sort data for plotting
const_turnout = votes_df.sort_values(by=["VOTER TURNOUT"], ascending=False)
high_consts = const_turnout.head(10)
low_consts = const_turnout.tail(10)

# Prepare labels for constituencies
xh = high_consts.index.get_level_values(1) + "\n(" + high_consts.index.get_level_values(0) + ")"
xl = low_consts.index.get_level_values(1) + "\n(" + low_consts.index.get_level_values(0) + ")"

# State-wise data
states_df = votes_df.groupby("STATE").sum().drop(["VOTER TURNOUT"], axis=1)
states_df["VOTER TURNOUT"] = round(states_df["TOTAL VOTES"] / states_df["TOTAL ELECTORS"] * 100, 2)
states_turnout = states_df.sort_values(by="VOTER TURNOUT", ascending=False)
high_stat = states_turnout.head(10)
low_stat = states_turnout.tail(10)

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(14, 8))  # Adjusted figsize to fit a 13-inch laptop

# Highest State Voter Outcome Plot
axes[0][0].tick_params(axis='x', labelrotation=50)
axes[0][0].plot(high_stat.index[::-1], high_stat["VOTER TURNOUT"][::-1], 'b-o', linewidth=2, markersize=10)
axes[0][0].set_ylabel("VOTER TURNOUT\n (in %)", labelpad=15)
axes[0][0].set_title("STATES/UTs WITH HIGHEST VOTER TURNOUT")
axes[0][0].grid(linewidth=2)

# Lowest State Voter Outcome Plot
axes[0][1].tick_params(axis='x', labelrotation=50)
axes[0][1].plot(low_stat.index, low_stat["VOTER TURNOUT"], 'r-o', linewidth=2, markersize=10)
axes[0][1].set_ylabel("VOTER TURNOUT\n (in %)", labelpad=15)
axes[0][1].set_title("STATES/UTs WITH LOWEST VOTER TURNOUT")
axes[0][1].grid(linewidth=2)

# Highest Constituency Voter Outcome Plot
axes[1][0].tick_params(axis='x', labelrotation=55)
axes[1][0].plot(xh[::-1], high_consts["VOTER TURNOUT"][::-1], 'g-o', linewidth=2, markersize=10)
axes[1][0].set_ylabel("VOTER TURNOUT\n (in %)", labelpad=15)
axes[1][0].set_title("CONSTITUENCIES WITH HIGHEST VOTER TURNOUT")
axes[1][0].grid(linewidth=2)

# Lowest Constituency Voter Outcome Plot
axes[1][1].tick_params(axis='x', labelrotation=55)
axes[1][1].plot(xl, low_consts["VOTER TURNOUT"], 'm-o', linewidth=2, markersize=10)
axes[1][1].set_ylabel("VOTER TURNOUT\n (in %)", labelpad=15)
axes[1][1].set_title("CONSTITUENCIES WITH LOWEST VOTER TURNOUT")
axes[1][1].grid(linewidth=2)

fig.tight_layout()
plt.show()
nat_average = round(states_turnout.sum()["TOTAL VOTES"]/states_turnout.sum()["TOTAL ELECTORS"]*100,2)
print("National Voter Turnout: ", nat_average, "%", sep="")
'''We infer from the plots, that Lakshadweep had the highest Voter Turnout ~87%, 
while Jammu & Kashmir had the lowest Voter Turnout ~43%.
Six North-Eastern states were in the top 10 of Highest Voter Turnout, 
whereas Kingmaker states like Uttar Pradesh, Bihar, Maharashtra, 
Delhi were in the top 10 of Lowest Voter Turnout.

Dhubri in Assam saw the Highest Voter Turnout in all of India, 
with about 87% eligible voters coming out to vote, 
whereas Anantnag in J&K saw the Lowest Voter Turnout with less 10% eligible voters casting their vote.
Andhra Pradesh, West Bengal and Assam saw some of the best performing Constituencies in terms of Voter Turnout.
On the other hand, Telangana, Bihar and Jammu & Kashmir having some of the poorest performing Constituencies in terms of Voter Turnout.'''
