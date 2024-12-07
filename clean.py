import pandas as pd

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

raw_election_data = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS_2.0.csv")
#print(raw_election_data) #to check
#The function convert(x) below is used to convert the ASSETS and LIABILITIES columns of the raw_election_data DataFrame into numeric values.

def convert(x):
    '''
    Extract the numeric value from the passed string and return it as float
    '''
    if str(x)[0] == 'R':
#         this is to ensure only valid values (and not NaN values) are converted
        return float(str(x).split()[1].replace(",", ""))
    return 0.0 
# default 0
raw_election_data.ASSETS = raw_election_data.ASSETS.apply(convert)
raw_election_data.LIABILITIES = raw_election_data.LIABILITIES.apply(convert)
# convert the ASSETS and LIABILITIES to numeric data

# the above can also be done using lambda function 
#print(raw_election_data.sample(5))
# check if the applied operations were successful
"""
#When the data was analysed later, it was found that the following categories in EDUCATION column would cause some uncertainities in the visualization process. Hence those are updated here itself, for all subsequent DataFrames.
raw_election_data.at[raw_election_data.EDUCATION=="Post Graduate\n", "EDUCATION"]="Post Graduate"
raw_election_data.at[raw_election_data.EDUCATION=="Graduate Professional", "EDUCATION"]="Graduate\nProfessional"
#line giving error"""

#These are holes in the data which must be fixed beforehand to avoid errors later.
raw_election_data.at[192, "WINNER"] = 1
raw_election_data.at[702, "WINNER"] = 1
raw_election_data.at[951, "WINNER"] = 1
raw_election_data.at[1132, "WINNER"] = 1
raw_election_data.at[172, "WINNER"] = 0

#Now we drop the unnecessary columns and create a new DataFrame candidates_df and change some column names for visualization purposes.

#print(raw_election_data.columns)

candidates_df = raw_election_data.drop(['SYMBOL', 'GENERAL\nVOTES', 'POSTAL\nVOTES',
                        'OVER TOTAL ELECTORS \nIN CONSTITUENCY', 'OVER TOTAL VOTES POLLED \nIN CONSTITUENCY'], axis=1)
# take out the unnecessary columns


candidates_df.rename(columns = {"CRIMINAL\nCASES": "CRIMINAL CASES", "TOTAL\nVOTES": "TOTAL VOTES"}, inplace = True)
candidates_df.sort_values(["STATE", "CONSTITUENCY"], inplace = True)
# rename some of the columns and sort the data with respect to State and Constituency columns

#candidates_df.info() #to check all columns

#Converting the data of `CRIMINAL CASES` column to numeric type.
candidates_df["CRIMINAL CASES"] = pd.to_numeric(candidates_df["CRIMINAL CASES"], errors = 'coerce').convert_dtypes()

#print(candidates_df) #to check

#personal details of non-NOTA candidates is extracted and stored in a new DataFrame candidates_personal_df.
candidates_personal_df = candidates_df[candidates_df.NAME != "NOTA"]
candidates_personal_df = candidates_personal_df.drop(["TOTAL VOTES", "TOTAL ELECTORS"], axis = 1)
#print(candidates_personal_df) #to check

print(candidates_personal_df.describe())
# works on only numeric data


#DataFrame winners_df is created which contains the details of only the winning candidates.

winners_df = candidates_df[candidates_df.WINNER == 1].sort_values(["STATE", "CONSTITUENCY"]).reset_index()
# extract the list of winners
winners_df.drop(["index", "WINNER"], axis = 1, inplace = True)
print(winners_df) #to check

print("Number of Parties which fielded at least 1 candidate: ", candidates_df.PARTY.unique().shape[0]-2)
                                                                 # -2 : 1 for independent candidates and 1 for NOTA
#Number of Parties which fielded at least 1 candidate:  131

                                                                
print("Number of Independent Candidates who contested the elections: ", candidates_df[candidates_df.PARTY == 'IND'].shape[0])
#Number of Independent Candidates who contested the elections:  201

print("Number of Parties which won at least 1 seat: ", winners_df.PARTY.unique().shape[0] - 1)
                                                                # -1 : for independent winners
#Number of Parties which won at least 1 seat:  35


print("Number of Independent Winners: ", winners_df[winners_df.PARTY == 'IND'].shape[0])
#Number of Independent Winners:  4


#print(raw_election_data)
