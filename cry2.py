#PREDICTION FOR GUJURAT
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Import the election results of the previous election (2014) as base values
# df = pd.read_csv("election-results-csv/LS2014Candidate.csv")
df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")

class LokSabhaElectionForecast:
    def __init__(self, coalitions, swings):
        self.coalitions = coalitions
        self.swings = swings

    def data_analysis(self):
        # Load the 2014 election data
        df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")

        # Initialize vote counters
        total_votes_count = 0
        total_nda_votes_count = 0
        total_upa_votes_count = 0

        # Calculate NDA and UPA votes
        first_nda = df.loc[(df['Party Abbreviation'].isin(self.coalitions['NDACoalition'])) & (df['Position'] == 1)]
        first_upa = df.loc[(df['Party Abbreviation'].isin(self.coalitions['UPACoalition'])) & (df['Position'] == 1)]

        # Analyze NDA seats
        nda_seats_from_nda2014 = 0
        upa_seats_from_nda2014 = 0

        for const_index, const_row in first_nda.iterrows():
            selected = df.loc[(df["ST_CODE"] == const_row["ST_CODE"]) & (df["PC Number"] == const_row["PC Number"])]
            upa_votes = 0
            nda_votes = 0

            for index, row in selected.iterrows():
                total_votes_count += row['Total Votes Polled']
                if row['Party Abbreviation'] in self.coalitions['UPACoalition']:
                    upa_votes += (1 + self.swings['UPA_swing_non_incumbent'] / 100) * row['Total Votes Polled']
                if row['Party Abbreviation'] in self.coalitions['NDACoalition']:
                    nda_votes += (1 + self.swings['NDA_swing_non_incumbent'] / 100) * row['Total Votes Polled']

            if nda_votes > upa_votes:
                nda_seats_from_nda2014 += 1
            else:
                upa_seats_from_nda2014 += 1

        # Analyze UPA seats
        upa_seats_from_upa2014 = 0
        nda_seats_from_upa2014 = 0

        for const_index, const_row in first_upa.iterrows():
            selected = df.loc[(df["ST_CODE"] == const_row["ST_CODE"]) & (df["PC Number"] == const_row["PC Number"])]
            upa_votes = 0
            nda_votes = 0

            for index, row in selected.iterrows():
                total_votes_count += row['Total Votes Polled']
                if row['Party Abbreviation'] in self.coalitions['UPACoalition']:
                    upa_votes += (1 + self.swings['UPA_swing_incumbent'] / 100) * row['Total Votes Polled']
                if row['Party Abbreviation'] in self.coalitions['NDACoalition']:
                    nda_votes += (1 + self.swings['NDA_swing_incumbent'] / 100) * row['Total Votes Polled']

            if upa_votes > nda_votes:
                upa_seats_from_upa2014 += 1
            else:
                nda_seats_from_upa2014 += 1

        # Final results
        total_nda_seats_2014 = nda_seats_from_nda2014 + upa_seats_from_nda2014
        total_upa_seats_2014 = upa_seats_from_upa2014 + nda_seats_from_upa2014

        print(f"Total NDA Seats in 2014: {total_nda_seats_2014}, Total UPA Seats in 2014: {total_upa_seats_2014}")

        # Calculate vote shares
        vote_share_nda = total_nda_votes_count / total_votes_count * 100
        vote_share_upa = total_upa_votes_count / total_votes_count * 100

        print(f"NDA Vote Share: {vote_share_nda:.2f}%, UPA Vote Share: {vote_share_upa:.2f}%")

    def machine_learning_component(self):
        # Load the election data for Gujarat
        gujarat_data = pd.DataFrame({
            'Year': [2009, 2012, 2014, 2017],
            'INC': [43.38, 38.93, 33.45, 41.4],
            'BJP': [46.52, 47.85, 60.11, 49.1]
        })

        # Create a linear regression model
        X = gujarat_data[['Year']]
        y = gujarat_data[['INC', 'BJP']]

        model = LinearRegression()
        model.fit(X, y)

        # Predict the vote shares for 2019
        predicted_vote_shares = model.predict([[2019]])

        # Calculate the swings
        inc_swing = predicted_vote_shares[0][0] - 33.45
        bjp_swing = predicted_vote_shares[0][1] - 60.11

        print(f"Predicted INC Swing: {inc_swing:.2f}%, Predicted BJP Swing: {bjp_swing:.2f}%")

# Define coalitions and swings
coalitions = {
    'NDACoalition': ["BJP", "SHS", "TDP", "LJP", "SAD", "BLSP", "SWP", "AD", "PMK", "AINRC", "NPF", "NPEP"],
    'UPACoalition': ["INC", "NCP", "RJD", "IUML", "JMM", "KEC(M)", "RSP"]
}

swings = {
    'NDA_swing_incumbent': 93,
    'NDA_swing_non_incumbent': 97,
    'UPA_swing_incumbent': 103,
    'UPA_swing_non_incumbent': 107
}

# Create an instance of the LokSabhaElectionForecast class
forecast = LokSabhaElectionForecast(coalitions, swings)

# Run the data analysis component
forecast.data_analysis()

# Run the machine learning component
forecast.machine_learning_component()