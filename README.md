# Czarbot
Program for automation of Labor Czar related activities at Pearl St. Co-op


## To-Do
- Make Labor Chart Generator

## Structure
- workbook.py: makes the API call to the central labor workbook, will be imported in other files for communication and data read-in
- credentials.json: for authentication. If someone else tries to run this, they would need the Pearl Labor email account password to run it.
- minimal_discord_bot.py: just some testing with reading and sending messages
