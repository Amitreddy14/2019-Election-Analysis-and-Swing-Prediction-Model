#Q5: How many elected MPs have a criminal record and what is their party-wise distribution?

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