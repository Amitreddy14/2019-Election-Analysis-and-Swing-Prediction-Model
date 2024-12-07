#karnataka

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Import the election results of the previous election (2014) as base values
df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")

class KarnatakaElectionForecast:
    def __init__(self, coalitions, swings):
        self.coalitions = coalitions
        self.swings = swings

    def data_analysis(self):
        # Load the 2014 election data for Karnataka
        df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")
        karnataka_df = df[df['State name'] == 'Karnataka']

        # Initialize vote counters
        total_votes_count = 0
        total_nda_votes_count = 0
        total_upa_votes_count = 0

        # Calculate NDA and UPA votes
        first_nda = karnataka_df.loc[(karnataka_df['Party Abbreviation'].isin(self.coalitions['NDACoalition'])) & (karnataka_df['Position'] == 1)]
        first_upa = karnataka_df.loc[(karnataka_df['Party Abbreviation'].isin(self.coalitions['UPACoalition'])) & (karnataka_df['Position'] == 1)]

        # Analyze NDA seats
        nda_seats_from_nda2014 = 0
        upa_seats_from_nda2014 = 0

        for const_index, const_row in first_nda.iterrows():
            selected = karnataka_df.loc[(karnataka_df["ST_CODE"] == const_row["ST_CODE"]) & (karnataka_df["PC Number"] == const_row["PC Number"])]
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
            selected = karnataka_df.loc[(karnataka_df["ST_CODE"] == const_row["ST_CODE"]) & (karnataka_df["PC Number"] == const_row["PC Number"])]
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

        print(f"Total NDA Seats in Karnataka 2014: {total_nda_seats_2014}, Total UPA Seats in Karnataka 2014: {total_upa_seats_2014}")

        # Calculate vote shares
        vote_share_nda = total_nda_votes_count / total_votes_count * 100
        vote_share_upa = total_upa_votes_count / total_votes_count * 100

        print(f"NDA Vote Share in Karnataka: {vote_share_nda:.2f}%, UPA Vote Share in Karnataka: {vote_share_upa:.2f}%")

    def machine_learning_component(self):
        # Load the election data for Karnataka
        karnataka_data = pd.DataFrame({
            'Year': [2009, 2013, 2014, 2018],
            'INC': [35.63, 36.59, 41.15, 38.14],
            'BJP': [33.86, 20.09, 43.37, 36.24]
        })

        # Create a linear regression model
        X = karnataka_data[['Year']]
        y = karnataka_data[['INC', 'BJP']]

        model = LinearRegression()
        model.fit(X, y)

        # Predict the vote shares for 2019
        predicted_vote_shares = model.predict([[2019]])

        # Calculate the swings
        inc_swing = predicted_vote_shares[0][0] - 41.15
        bjp_swing = predicted_vote_shares[0][1] - 43.37

        print(f"Predicted INC Swing in Karnataka: {inc_swing:.2f}%, Predicted BJP Swing in Karnataka: {bjp_swing:.2f}%")

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

# Create an instance of the KarnatakaElectionForecast class
forecast = KarnatakaElectionForecast(coalitions, swings)

# Run the data analysis component
forecast.data_analysis()

# Run the machine learning component
forecast.machine_learning_component()


