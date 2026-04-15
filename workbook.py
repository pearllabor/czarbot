from __future__ import annotations

# This import lets us check whether files like "token.json" already exist.
import os

# "Any" is used here because the Google API client returns a service object
# with a complicated type, and using Any keeps the type hints simple.
from typing import Any

# This is used to refresh an expired login token automatically,
# so the user does not have to sign in every single time.
from google.auth.transport.requests import Request

# This represents OAuth credentials for a signed-in Google user.
from google.oauth2.credentials import Credentials

# This handles the browser-based OAuth login flow.
# When the script runs for the first time, this will open a browser window
# and ask the user to sign in with their Google account.
from google_auth_oauthlib.flow import InstalledAppFlow

# This builds the actual Google Sheets API service object
# that we use to send requests to Google Sheets.
from googleapiclient.discovery import build

from datetime import datetime
import pandas as pd

# SCOPES tells Google what permissions this script is requesting.
#
# This scope gives full read/write access to Google Sheets.
# That means this script can both read cell values and change them.
#
# If you only wanted read-only access, you would use:
# "https://www.googleapis.com/auth/spreadsheets.readonly"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
address = "1Bxmu2iIqNMdsGEVOVE_Loyym3WMRQOPzfU1bzL9uGhg"


def get_sheets_service() -> Any:
    """
    Create and return an authenticated Google Sheets API service object.

    What this function does:
    1. Look for a saved login token in token.json.
    2. If token.json exists, load those saved credentials.
    3. If the credentials are expired, try to refresh them automatically.
    4. If there are no credentials yet, start the OAuth login flow in a browser.
    5. Save the new credentials to token.json for future runs.
    6. Build and return the Sheets API service object.
    """

    # Start with no credentials loaded.
    creds = None

    # token.json is created after the first successful login.
    # It stores the user's access token and refresh token.
    #
    # If this file already exists, we can load it and avoid asking the user
    # to sign in again.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # At this point, there are three possibilities:
    #
    # 1. creds is None
    #    -> The user has never logged in before.
    #
    # 2. creds exists but is invalid
    #    -> The saved token is no longer usable as-is.
    #
    # 3. creds exists and is valid
    #    -> We can use it immediately.
    #
    # If we do NOT have valid credentials, we need to fix that.
    if not creds or not creds.valid:

        # Case: we do have credentials, but they are expired,
        # and they include a refresh token.
        #
        # In that situation, Google lets us refresh the credentials
        # automatically without opening the browser again.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Otherwise, we must do the full OAuth sign-in flow.
        else:
            # credentials.json must come from Google Cloud Console.
            # It contains your OAuth client information.
            #
            # This file identifies your application to Google.
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )

            # This starts a local web server and opens a browser window.
            # The user signs into Google and grants permission.
            #
            # After successful login, Google redirects back to the local server,
            # and we get usable credentials.
            creds = flow.run_local_server(port=0)

        # After either refreshing or signing in, save the credentials
        # so future runs can reuse them.
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    # Build the Google Sheets API service object.
    #
    # "sheets" means we want the Google Sheets API.
    # "v4" is the API version.
    # "credentials=creds" tells the client to use the authenticated user.
    return build("sheets", "v4", credentials=creds)


def read_sheet(spreadsheet_id: str, cell_range: str) -> list[list[str]]:
    """
    Read values from a Google Sheet and return them as a list of rows.

    Parameters
    ----------
    spreadsheet_id : str
        The unique ID of the Google Sheet.
        This comes from the sheet URL.

    cell_range : str
        The range to read, in A1 notation.
        Example: "Sheet1!A1:C10"

    Returns
    -------
    list[list[str]]
        A list of rows.
        Each row is itself a list of cell values.
        Example:
        [
            ["Alice", "24"],
            ["Bob", "31"]
        ]
    """

    # Get an authenticated Sheets API service object.
    service = get_sheets_service()

    # Send a request to Google Sheets:
    #
    # service.spreadsheets()
    #   -> work with spreadsheet-level resources
    #
    # .values()
    #   -> specifically work with cell values
    #
    # .get(...)
    #   -> request cell values from a given spreadsheet and range
    #
    # .execute()
    #   -> actually send the request to Google and get the response
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=cell_range)
        .execute()
    )

    # The response is a dictionary.
    # The actual cell data is usually stored under the key "values".
    #
    # If that key is missing, return an empty list instead of crashing.
    return result.get("values", [])


def write_sheet(spreadsheet_id: str, cell_range: str, values: list[list[str]]) -> dict:
    """
    Write values into a Google Sheet.

    Parameters
    ----------
    spreadsheet_id : str
        The unique ID of the Google Sheet.

    cell_range : str
        The starting range where data should be written.
        Example: "Sheet1!A1:B3"

    values : list[list[str]]
        The values to write.
        Each inner list is one row.
        Example:
        [
            ["Name", "Age"],
            ["Alice", "24"],
            ["Bob", "31"]
        ]

    Returns
    -------
    dict
        The API response dictionary from Google Sheets,
        which includes information such as how many cells were updated.
    """

    # Get an authenticated Sheets API service object.
    service = get_sheets_service()

    # Google expects the values to be wrapped inside a dictionary
    # with the key "values".
    body = {"values": values}

    # Send an update request to Google Sheets.
    #
    # spreadsheetId=spreadsheet_id
    #   -> which spreadsheet to modify
    #
    # range=cell_range
    #   -> where to write the data
    #
    # valueInputOption="RAW"
    #   -> write the values exactly as provided
    #      (Google will not reinterpret them as formulas unless you provide formulas)
    #
    # body=body
    #   -> the actual data being written
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=cell_range,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    # Return Google's response so the caller can inspect it if needed.
    return result

def labor_preferences():
    membership_database = read_sheet(address, "Membership Database!A3:A200")
    names = [row[0] for row in membership_database]
    names.remove("supershow this week")




    # ========== LABOR PREFERENCES ========== #
    preferences = read_sheet(address, "Labor Preferences!A3:AB200")
    preferences_dict = dict.fromkeys(names, [])
    # turn preferences into a dataframe
    preferences_df = pd.DataFrame(preferences[1:], columns=preferences[0])
    # remove certain columns that we don't need
    preferences_df = preferences_df.drop(columns=['Hours', 'Name Update', 'Notes', 'Medical Conditions', 'Context'])
    # populate preferences_dict with each person's preferences, only keeping the most recent form for each person
    for name in names:
        preferences_dict[name] = dict.fromkeys(preferences_df.columns, 0)
        for index, row in preferences_df.iterrows():
            if row['Name'] == name:
                # only keep the most recent form for each person, so overwrite the previous one if there are multiple forms
                if preferences_dict[name]['Time/Exempt'] == 0:
                    for column in preferences_df.columns[2:]:
                        preferences_dict[name][column] = row[column]
                elif datetime.strptime(row['Time/Exempt'], "%m/%d/%Y %H:%M:%S") > datetime.strptime(preferences_dict[name]['Time/Exempt'], "%m/%d/%Y %H:%M:%S"):
                    for column in preferences_df.columns[2:]:
                        preferences_dict[name][column] = row[column]

    return preferences_dict

def shift_database():
    shift_database = read_sheet(address, "Shift Database!A2:O100")

    # make a shift database dictionary with the shift name as the key and the shift time and type of labor as the values
    shift_database_dict = dict.fromkeys([row[0] for row in shift_database], [])
    for row in shift_database:
        shift_database_dict[row[0]] = {'Category': row[1], 'Hours': row[2], 'Start': row[3]}


    return shift_database_dict

def labor_chart():
    labor_sheet = read_sheet(address, "Labor Chart!A1:Z300")
    # find the cells labeled Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday and store their coordinates in a dictionary
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_coordinates = {}
    for i in range(len(labor_sheet)):
        for j in range(len(labor_sheet[i])):
            if labor_sheet[i][j] in days:
                day_coordinates[labor_sheet[i][j]] = (i+1, j)


    # find start and end rows associated with the labor on each day, and store the coordinates of the cells in a dictionary with the labor as the key and the coordinates as the value
    labor_coordinates = {}
    for day, coordinates in day_coordinates.items():
        start_row = coordinates[0] + 2
        end_row = start_row
        while end_row < len(labor_sheet) and labor_sheet[end_row][coordinates[1]] not in day_coordinates.keys():
            end_row += 1
        labor_coordinates[day] = (start_row, end_row)

    labor_chart_dict = {}
    for day, coordinates in labor_coordinates.items():
        shifts = read_sheet(address, f"Labor Chart!A{coordinates[0]}:A{coordinates[1]}")
        shifts = [shift[0] for shift in shifts]
        day_dict = dict.fromkeys(shifts, 0)
        # values are the number of each kind of labor for that shift
        for shift in shifts:
            day_dict[shift] += 1
        labor_chart_dict[day] = day_dict

    return labor_chart_dict



# if __name__ == "__main__":
    # This is the ID of the spreadsheet you want to access.
    # You can find it in the Google Sheets URL.
    #
    # Example URL:
    # https://docs.google.com/spreadsheets/d/1Bxmu2iIqNMdsGEVOVE_Loyym3WMRQOPzfU1bzL9uGhg/edit#gid=0
    #
    # The spreadsheet ID is the long string between /d/ and /edit.
    # spreadsheet_id = "1Bxmu2iIqNMdsGEVOVE_Loyym3WMRQOPzfU1bzL9uGhg"

    # This is the exact range to read, using A1 notation.
    #
    # "Membership Database" is the sheet tab name.
    # "A3:A84" means:
    # - start at column A, row 3
    # - end at column A, row 84
    #cell_range = "Membership Database!A3:A84"

    # Read the values from the specified sheet and range.
    # values = read_sheet(spreadsheet_id, cell_range)

    # # If Google returned no values, print a helpful message.
    # if not values:
    #     print("No data found.")

    # # Otherwise, print each row one by one.
    # else:
    #     for row in values:
    #         print(row)

    # write to the sheet
    #name = 'Lance Kessler'
    #write_sheet(spreadsheet_id, "Membership Database!A86", [[name]])