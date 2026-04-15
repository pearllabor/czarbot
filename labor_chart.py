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


labor_chart = workbook.labor_chart()
print('Finished reading labor chart')

preferences = workbook.labor_preferences()
print('Finished reading labor preferences')

shift_database = workbook.shift_database()
print('Finished reading shift database')


print(shift_database['Lunch Cook'])
