#PREDICTION FOR INC, BJP, UPA
import pandas as pd
from collections import defaultdict

# Load the dataset
df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")

# Define coalitions for 2014 and expected coalitions for 2019
NDACoalition = ["BJP", "SHS", "TDP", "LJP", "SAD", "BLSP", "SWP", "AD", "PMK", "AINRC", "NPF", "NPEP"]
UPACoalition = ["INC", "NCP", "RJD", "IUML", "JMM", "KEC(M)", "RSP"]

# Define swing percentages
ndaSwingIncumbent = 93
ndaSwingNotIncumbent = 97
upaSwingIncumbent = 103
upaSwingNotIncumbent = 107

# Initialize vote counters
totalVotesCount = 0
totalNdaVotesCount = 0
totalUpaVotesCount = 0

# Calculate NDA and UPA votes
firstNDA = df.loc[(df['Party Abbreviation'].isin(NDACoalition)) & (df['Position'] == 1)]
firstUPA = df.loc[(df['Party Abbreviation'].isin(UPACoalition)) & (df['Position'] == 1)]

# Analyze NDA seats
ndaSeatsFromNDA2014 = 0
upaSeatsFromNDA2014 = 0
nda2014SeatsStatewise = defaultdict(int)

for constIndex, constRow in firstNDA.iterrows():
    nda2014SeatsStatewise[constRow["State name"]] += 1
    selected = df.loc[(df["ST_CODE"] == constRow["ST_CODE"]) & (df["PC Number"] == constRow["PC Number"])]
    upaVotes = 0
    ndaVotes = 0

    for index, row in selected.iterrows():
        totalVotesCount += row['Total Votes Polled']
        if row['Party Abbreviation'] in UPACoalition:
            upaVotes += (upaSwingNotIncumbent / 100) * row['Total Votes Polled']
        if row['Party Abbreviation'] in NDACoalition:
            ndaVotes += (ndaSwingIncumbent / 100) * row['Total Votes Polled']

    totalNdaVotesCount += ndaVotes
    totalUpaVotesCount += upaVotes

    if ndaVotes > upaVotes:
        ndaSeatsFromNDA2014 += 1
    else:
        upaSeatsFromNDA2014 += 1

# Analyze UPA seats
upaSeatsFromUPA2014 = 0
ndaSeatsFromUPA2014 = 0
upa2014SeatsStatewise = defaultdict(int)

for constIndex, constRow in firstUPA.iterrows():
    upa2014SeatsStatewise[constRow["State name"]] += 1
    selected = df.loc[(df["ST_CODE"] == constRow["ST_CODE"]) & (df["PC Number"] == constRow["PC Number"])]
    upaVotes = 0
    ndaVotes = 0

    for index, row in selected.iterrows():
        totalVotesCount += row['Total Votes Polled']
        if row['Party Abbreviation'] in UPACoalition:
            upaVotes += (upaSwingIncumbent / 100) * row['Total Votes Polled']
        if row['Party Abbreviation'] in NDACoalition:
            ndaVotes += (ndaSwingNotIncumbent / 100) * row['Total Votes Polled']

    totalNdaVotesCount += ndaVotes
    totalUpaVotesCount += upaVotes

    if upaVotes > ndaVotes:
        upaSeatsFromUPA2014 += 1
    else:
        ndaSeatsFromUPA2014 += 1

# Final results
totalNDASeats2014 = ndaSeatsFromNDA2014 + upaSeatsFromNDA2014
totalUPASeats2014 = upaSeatsFromUPA2014 + ndaSeatsFromUPA2014

print(f"Total NDA Seats in 2014: {totalNDASeats2014}, Total UPA Seats in 2014: {totalUPASeats2014}")

# Calculate vote shares
voteShareNDA = totalNdaVotesCount / totalVotesCount * 100
voteShareUPA = totalUpaVotesCount / totalVotesCount * 100

print(f"NDA Vote Share: {voteShareNDA:.2f}%, UPA Vote Share: {voteShareUPA:.2f}%")