import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class TamilNaduElectionForecast:
    def __init__(self, coalitions, swings):
        self.coalitions = coalitions
        self.swings = swings

    def data_analysis(self):
        # Load the 2014 election data for Tamil Nadu
        df = pd.read_csv(r"C:\Users\harshwardhan\OneDrive\Desktop\fds proj\LS2014Candidate.csv")
        tamilnadu_df = df[df['State name'] == 'Tamil Nadu']

        # Initialize vote counters
        total_votes_count = 0
        total_dmk_votes_count = 0
        total_admk_votes_count = 0
        total_bjp_votes_count = 0

        # Calculate votes for each alliance
        first_dmk = tamilnadu_df.loc[(tamilnadu_df['Party Abbreviation'].isin(self.coalitions['DMKAlliance'])) & (tamilnadu_df['Position'] == 1)]
        first_admk = tamilnadu_df.loc[(tamilnadu_df['Party Abbreviation'].isin(self.coalitions['ADMKAlliance'])) & (tamilnadu_df['Position'] == 1)]
        first_bjp = tamilnadu_df.loc[(tamilnadu_df['Party Abbreviation'].isin(self.coalitions['BJPAlliance'])) & (tamilnadu_df['Position'] == 1)]

        # Analyze seats
        def analyze_seats(first_alliance, alliance_name):
            seats_won = 0
            seats_lost = 0

            for const_index, const_row in first_alliance.iterrows():
                selected = tamilnadu_df.loc[(tamilnadu_df["ST_CODE"] == const_row["ST_CODE"]) & (tamilnadu_df["PC Number"] == const_row["PC Number"])]
                alliance_votes = 0
                other_votes = 0

                for index, row in selected.iterrows():
                    total_votes_count += row['Total Votes Polled']
                    if row['Party Abbreviation'] in self.coalitions[alliance_name]:
                        alliance_votes += (1 + self.swings[f'{alliance_name}_swing'] / 100) * row['Total Votes Polled']
                    else:
                        other_votes += row['Total Votes Polled']

                if alliance_votes > other_votes:
                    seats_won += 1
                else:
                    seats_lost += 1

            return seats_won, seats_lost

        # Calculate seats for each alliance
        dmk_seats = analyze_seats(first_dmk, 'DMKAlliance')
        admk_seats = analyze_seats(first_admk, 'ADMKAlliance')
        bjp_seats = analyze_seats(first_bjp, 'BJPAlliance')

        print(f"DMK Alliance Seats: {dmk_seats[0]}, ADMK Alliance Seats: {admk_seats[0]}, BJP Alliance Seats: {bjp_seats[0]}")

    def machine_learning_component(self):
        # Load historical election data for Tamil Nadu
        tamilnadu_data = pd.DataFrame({
            'Year': [2009, 2011, 2014, 2016],
            'DMK': [25.1, 22.4, 23.6, 31.6],
            'ADMK': [22.9, 38.4, 44.3, 40.8],
            'BJP': [2.3, 2.2, 5.5, 2.8]
        })

        # Create linear regression models for each party
        X = tamilnadu_data[['Year']]
        y = tamilnadu_data[['DMK', 'ADMK', 'BJP']]

        model = LinearRegression()
        model.fit(X, y)

        # Predict vote shares for 2019
        predicted_vote_shares = model.predict([[2019]])

        print(f"Predicted DMK Vote Share: {predicted_vote_shares[0][0]:.2f}%")
        print(f"Predicted ADMK Vote Share: {predicted_vote_shares[0][1]:.2f}%")
        print(f"Predicted BJP Vote Share: {predicted_vote_shares[0][2]:.2f}%")

# Define coalitions and swings for Tamil Nadu
coalitions = {
    'DMKAlliance': ["DMK", "INC", "VCK", "IUML", "KDMK", "IJK"],
    'ADMKAlliance': ["ADMK", "PMK", "DMDK", "PT", "TMC(M)", "PNK"],
    'BJPAlliance': ["BJP", "INDI"]
}

swings = {
    'DMKAlliance_swing': 5,
    'ADMKAlliance_swing': -2,
    'BJPAlliance_swing': 1
}

# Create an instance of the TamilNaduElectionForecast class
forecast = TamilNaduElectionForecast(coalitions, swings)

# Run the data analysis component
forecast.data_analysis()

# Run the machine learning component
forecast.machine_learning_component()