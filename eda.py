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

print(candidates_personal_df.describe())

# Winners DataFrame
winners_df = candidates_df[candidates_df.WINNER == 1].sort_values(["STATE", "CONSTITUENCY"]).reset_index()
winners_df.drop(["index", "WINNER"], axis=1, inplace=True)
print(winners_df)

# Print statistics
print("Number of Parties which fielded at least 1 candidate: ", candidates_df.PARTY.unique().shape[0] - 2)
print("Number of Independent Candidates who contested the elections: ", candidates_df[candidates_df.PARTY == 'IND'].shape[0])
print("Number of Parties which won at least 1 seat: ", winners_df.PARTY.unique().shape[0] - 1)
print("Number of Independent Winners: ", winners_df[winners_df.PARTY == 'IND'].shape[0])

# Set seaborn style and adjust figure size
sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 12  # Adjust font size
matplotlib.rcParams['figure.figsize'] = (10, 6)  # Adjust figure size for 13-inch laptop
matplotlib.rcParams['figure.facecolor'] = '#00000000'

# Prepare seat distribution data
all_party_seats = winners_df.PARTY.value_counts().sort_values(ascending=False)
others = all_party_seats[all_party_seats < 10].sum()
seat_distribution = pd.concat([all_party_seats[all_party_seats >= 10], pd.Series({"Others": others})])
print(seat_distribution)

# Plot seat share pie chart
plt.figure(figsize=(8, 6))  # Adjusted size for better visibility
plt.title("SEAT SHARE")
plt.pie(seat_distribution, labels=seat_distribution.index,
        colors=['#f97d09', '#00bdfe', '#dc143c', '#0266b4', '#24b44c', '#ff6634', 
                '#203354', '#105e27', '#22409a', '#FFFFFF'],
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.75, 'antialiased': True})

seat_percent = round((seat_distribution / seat_distribution.sum()) * 100, 2)
legend = seat_percent.index + " (" + seat_percent.values.astype(str) + "%) - " + seat_distribution.values.astype(str)

plt.legend(legend , loc="right", bbox_to_anchor=(1.4, 0.5))  # Adjusted legend position
plt.show()
'''As we can see, the BJP was the single largest party with more than 50% of the seats in the House, 
with INC at a distant second.
Other regional parties like DMK, YSRCP, AITC, BJD won some seats in their respective states, 
but no Alliance could pose as an alternative to BJP.'''

# Plot histogram for age of candidates
plt.figure(figsize=(15, 8))  # Adjusted size for better visibility
plt.title("Age of Candidates Contested and Won", fontsize=18)
plt.xlabel("Age", fontsize=15)
plt.ylabel("Number of Candidates", fontsize=15)

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)

# Plot histograms for contested and won candidates
sns.histplot(data=candidates_personal_df, x='AGE', bins=np.arange(20, 100, 5), color='indigo', alpha=0.5)
sns.histplot(data=winners_df, x='AGE', bins=np.arange(20, 100, 5), color='lightgreen', alpha=1)

# Add legend
plt.legend(["Candidates Contested", "Candidates Won"], fontsize=13)

# Add text for statistics
plt.text(84.5, 185, "All Candidates:")
plt.figtext(0.77, 0.63, round(candidates_personal_df.describe().AGE[['mean', 'min', 'max']], 2).to_string())

plt.text(84.5, 140, "Winning Candidates:")
plt.figtext(0.77, 0.5, round(winners_df.describe().AGE[['mean', 'min', 'max']], 2).to_string())

# Show the plot
plt.show()

#youngest and oldest
print("\nYoungest Member of the House:")
print(winners_df[(winners_df.AGE == 25)][["NAME", "PARTY", "STATE", "CONSTITUENCY"]].reset_index(drop = True))
print("\n")
print("Oldest Member of the House:")
print(winners_df[(winners_df.AGE == 86)][["NAME", "PARTY", "STATE", "CONSTITUENCY"]].reset_index(drop = True))
print("\n")
'''As we can see from the Nested Histogram, the age group 55-60 has the maximum number of Candidates, 
and Winners, followed closely by the age group 50-55.
The average age of the house - 54 years also lies in this range. 
A majority of the winners are between the ages 45-70, 
which can be considered as the normal peak years of a Politician.'''

#SEAT CATEGORY
#here we calculate the ratio of seats which have a special reservation status for candidates of different backward classes.
seat_category = winners_df.CATEGORY.value_counts()
# winners_df has 1 constituency only 1 time, so analysing its CATEGORY column will give the correct result
print(pd.DataFrame(seat_category))

#pie chart distrubutuion
sns.set_palette(sns.color_palette('Set2'))
plt.figure(figsize=(8,5))
plt.title("Distribution of Seats by Category", size=18, x = 0.52, y =0.95)

plt.pie(seat_category, labels = seat_category.index, autopct = '%1.1f%%', startangle = 45)
plt.show()# percentage of seats shown on the plot


#GENDER
#check gender diversity
gender_group = candidates_personal_df.groupby(["GENDER", "WINNER"]).size()
gender_group = gender_group.unstack()
gender_group = gender_group[[1,0]]
# a2a from stack overflow

# gender with winning condition is extracted as a dataframe

sns.set_palette(sns.color_palette("icefire"))
# color palette set
gender_group.plot(kind = 'barh', figsize = (15,6), title = "Gender Comparison of Contesting and Winning Candidates")
# horizontal bar plot created with Pandas 

plt.legend(["Won", "Lost"])
plt.xlabel("Number of Candidates")
plt.ylabel("Gender")
# legend and labels set

plt.figtext(0.738,0.53, "Contesting Candidates:\n" + 
            round((candidates_personal_df.GENDER.value_counts(normalize=True)*100),2).to_string().replace("\n", "%\n")+"%")

plt.figtext(0.738,0.33, "Winning Candidates:\n" + 
            round((winners_df.GENDER.value_counts(normalize=True)*100),2).to_string().replace("\n", "%\n")+"%")

# Total candidates statistics (percentages) printed on the chart, with some applied String formatting to give the look

win_percent = round((winners_df.GENDER.value_counts()/candidates_personal_df.GENDER.value_counts())*100,2)
plt.figtext(0.395, 0.63, str(round(win_percent.MALE,2)) + "% candidates won")
plt.figtext(0.175, 0.25, str(round(win_percent.FEMALE,2))+ "% candidates won");
plt.show()# percentage of winning, gender-wise printed on the chart

print("No. of male MPs: ", winners_df.GENDER.value_counts()["MALE"])
print("No. of female MPs: ", winners_df.GENDER.value_counts()["FEMALE"])


'''As we can see, the House has 14.4% Female members and 85.6% Male members.
One surprising inference we can draw from the Analysis is that despite a higher 
percentage of Male Candidates contesting the elections than Female (87.2% vs 12.8%), 
the percentage of Female Contestants who won was greater than that of Male Contestants (30.2% vs 26.4%).
This means, a Female Candidate had a greater chance of winning the election than a Male Candidate.
'''


#EDUCATIONAL QUALIFICATIONS

winners_df["EDUCATION"].unique()
education = winners_df.EDUCATION.value_counts()
education = education.reindex(["Illiterate", "Literate", "5th Pass", "8th Pass", "10th Pass", "12th Pass", "Graduate", 
                               "Graduate\nProfessional","Post Graduate", "Doctorate", "Others"])
# arrange the Series in a systematic order
print(education)
#bar grapf for education
plt.figure(figsize=(15,7))
plt.xticks(rotation = 60);
# plot detailing

plt.xlabel("Education Status", fontsize = 15)
plt.ylabel("No. of Candidates", fontsize = 15)
plt.title("EDUCATIONAL QUALIFICATIONS OF WINNERS",fontsize = 18)
# labels and title

sns.barplot(x = education.index, y = education.values);
plt.show()# plotting the barplot

'''We see, contrary to popular belief, most MPs are well educated and have at least a Graduate degree.
There are less than 150 MPs who are 12th Pass or below.'''