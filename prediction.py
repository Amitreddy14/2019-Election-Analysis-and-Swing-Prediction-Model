import pandas as pd
from collections import defaultdict
#df = pd.read_csv("election-results-csv/LS2009Candidate.csv")
df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")
"""Coalitions in 2014"""
#NDACoalition = ["BJP","SHS","TDP","LJP","SAD","BLSP","SWP","AD","PMK","AINRC","NPF","NPEP"]
#UPACoalition = ["INC","NCP","RJD","IUML","JMM","KEC(M)","RSP"]

"""If BJP and INC were alone"""
#NDACoalition = ["BJP"]
#UPACoalition = ["INC"]

"""Expected Coalitions in 2019""" 
NDACoalition = ["BJP", "SHS","JD(U)","LJP","NPF","SAD","BLSP", "SWP","PMK","NPEP","AINRC","ADMK", "AGP"]
UPACoalition = ["INC", "AD", "RJD","NCP", "DMK","IUML","JD(S)","JKN","JMM","KEC(M)","RSP","BOPF"]

"""In percent. Incumbent swings are likelier to be lesser, as people want change."""
ndaSwingIncumbent = 93
ndaSwingNotIncumbent = 97
upaSwingIncumbent = 103
upaSwingNotIncumbent = 107

"""No swings"""
#ndaSwingIncumbent = 100
#ndaSwingNotIncumbent = 100
#upaSwingIncumbent = 100
#upaSwingNotIncumbent = 100

#totalVotesCount = df.loc[(df['Party Abbreviation'].isin(UPACoalition+NDACoalition)), ['Total Votes Polled']].sum()
totalVotesCount = 0
totalNdaVotesCount = 0
totalUpaVotesCount = 0
totalMgbVotesCount = 0

firstNDA = df.loc[(df['Party Abbreviation'].isin(NDACoalition)) & (df['Position'] == 1)]
firstUPA = df.loc[(df['Party Abbreviation'].isin(UPACoalition)) & (df['Position'] == 1)]
#firstOther = df.loc[~(df['Party Abbreviation'].isin(UPACoalition+NDACoalition)) & (df['Position'] == 1)]
 
"""
#PROTOTYPE FOR UTTAR PRADESH
firstBJPInUP = df.loc[(df['Party Abbreviation'] == "BJP") & (df['Position'] == 1) & (df['State name'] == 'Uttar Pradesh')]
c = 0
numberOfSeatsLost = 0
numberOfSeatsWon = 0

totalBjpVotes = 0
totalCoalitionVotes = 0
totalVotes = 0

for constIndex, constRow in firstBJPInUP.iterrows():
    selected = df.loc[(df["ST_CODE"] == constRow["ST_CODE"]) & (df["PC Number"] == constRow["PC Number"])]
    coalitionVotes = 0
    bjpVotes = 0
    
    for index,row in selected.iterrows():
        totalVotes += row['Total Votes Polled']
        if (row['Party Abbreviation'] in ["SP","BSP","INC","RLD"]):
            coalitionVotes += row['Total Votes Polled']
        if (row['Party Abbreviation'] == 'BJP'):
            bjpVotes += row['Total Votes Polled']
    totalBjpVotes += bjpVotes
    totalCoalitionVotes += coalitionVotes
    
    if (bjpVotes < coalitionVotes):  
        numberOfSeatsLost += 1
        margin = coalitionVotes-bjpVotes
        #print("BJP LOSES THE SEAT: "+constRow["PC name"]+ " Margin: "+str(margin)+" votes") 
    else:
        numberOfSeatsWon += 1
        margin = bjpVotes-coalitionVotes
        #print("BJP STILL WINS THE SEAT: "+constRow["PC name"]+ " Margin: "+str(margin)+" votes") 
        
print("Lost: " + str(numberOfSeatsLost)+" Won: "+str(numberOfSeatsWon))
bjpVoteShare = totalBjpVotes/totalVotes*100
coalitionVoteShare = totalCoalitionVotes/totalVotes*100
print("Vote Share\nBJP: "+str(bjpVoteShare)+"% INC/SP/BSP/RLD: "+str(coalitionVoteShare)+"%")
"""

c = 0
upaSeatsFromNDA2014 = 0
ndaSeatsFromNDA2014 = 0

nda2014SeatsStatewise=defaultdict(int); #where NDA was first in 2014
ndaSeatsStatewiseFromNDA2014=defaultdict(int); #after grand colition ndaSeats
upaSeatsStatewiseFromNDA2014=defaultdict(int); #after grand coalition upaSeats

for constIndex, constRow in firstNDA.iterrows():
    nda2014SeatsStatewise[constRow["State name"]] += 1;
    selected = df.loc[(df["ST_CODE"] == constRow["ST_CODE"]) & (df["PC Number"] == constRow["PC Number"])]
    upaVotes = 0;
    ndaVotes = 0;
    for index,row in selected.iterrows():
        totalVotesCount += row['Total Votes Polled']
        if (row['Party Abbreviation'] in UPACoalition):
            upaVotes += (upaSwingNotIncumbent/100)*row['Total Votes Polled']
        if (row['Party Abbreviation'] in NDACoalition):
            ndaVotes += (ndaSwingIncumbent/100)*row['Total Votes Polled']
    totalNdaVotesCount += ndaVotes 
    totalUpaVotesCount += upaVotes
    if (ndaVotes > upaVotes):  
        ndaSeatsFromNDA2014 += 1
        margin = ndaVotes-upaVotes
        ndaSeatsStatewiseFromNDA2014[constRow["State name"]] += 1;
    else:
        ndaSeatsFromNDA2014 += 1
        margin = upaVotes-ndaVotes
        ndaSeatsStatewiseFromNDA2014[constRow["State name"]] += 1;

totalNDASeats2014 = upaSeatsFromNDA2014+ndaSeatsFromNDA2014      
print("FROM NDA SEATS ("+str(totalNDASeats2014)+"):\nWon by UPA: " + str(upaSeatsFromNDA2014)+" \nWon by Others: " + str(mgbSeatsFromNDA2014)+" \nStill Won by NDA: "+str(ndaSeatsFromNDA2014))

print('\n')
print("TOTAL WON BY NDA IN 2014 REALITY")
print(nda2014SeatsStatewise)
print('\n')

print("WON BY UPA FROM NDA SEATS IN 2014 AFTER COALITION")
print(upaSeatsStatewiseFromNDA2014)
print('\n') 

print("WON BY NDA FROM NDA SEATS IN 2014 AFTER COALITION")
print(ndaSeatsStatewiseFromNDA2014)
print('\n')
