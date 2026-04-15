import workbook
import pandas as pd
from datetime import datetime

address = "1Bxmu2iIqNMdsGEVOVE_Loyym3WMRQOPzfU1bzL9uGhg"

# 1) Read in the data from the Labor Preference Form

# 2) Read in the memebership database, and match each person to a labor preference form
     # filter to only have the most recent form

# 3) Read in the current available labor slots and times, and match each person to a slot based on their preferences and availability. 
# This will be the most difficult part; want to maximize the score of the matches, where a person's score is based on how high their preferences 
# are and how well they match with the available slots.

# have a reference of shifts that people have to be in (officers, elected labor, head chefs, etc.)

# 4) Input those names to the sheet after the labor chart is finalized


labor_chart = workbook.read_sheet(address, "Labor Chart!A1:Z200")
preferences = workbook.read_sheet(address, "Labor Preferences!A3:AB200")
shift_database = workbook.read_sheet(address, "Shift Database!A2:G100")
membership_database = workbook.read_sheet(address, "Membership Database!A3:A200")
names = [row[0] for row in membership_database]
names.remove("supershow this week")


# turn preferences into a dataframe
preferences_df = pd.DataFrame(preferences[1:], columns=preferences[0])
preferences_dict = dict.fromkeys(names, [])

# populate preferences_dict with each person's preferences, only keeping the most recent form for each person
for name in names:
    preferences_dict[name] = dict.fromkeys(preferences_df.columns[4:], 0)
    for index, row in preferences_df.iterrows():
        if row['Name'] == name:
            # only keep the most recent form for each person, so overwrite the previous one if there are multiple forms
            if preferences_dict[name]['Time/Exempt'] == 0:
                for column in preferences_df.columns[4:]:
                    preferences_dict[name][column] = row[column]
            elif datetime.strptime(row['Time/Exempt'], "%m/%d/%Y %H:%M:%S") > datetime.strptime(preferences_dict[name]['Time/Exempt'], "%m/%d/%Y %H:%M:%S"):
                for column in preferences_df.columns[4:]:
                    preferences_dict[name][column] = row[column]

print(preferences_dict['Adam Hanus']['Thursday'])