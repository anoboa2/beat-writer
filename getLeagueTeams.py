import os
import json
import requests
import openai
from dotenv import load_dotenv
load_dotenv()

ESPN_S2 = os.getenv("ESPN_S2")
ESPN_LEAGUE_ID = os.getenv("ESPN_LEAGUE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORG_ID

# Call the ESPN API endpoint, transform the data, and select the Teams subset
def getLatestLeagueTeams(abbrev=False):
  res = requests.get(
    url=f"https://fantasy.espn.com/apis/v3/games/flb/seasons/2023/segments/0/leagues/{ESPN_LEAGUE_ID}?view=mTeam",
    headers={
      "content-type": "application/json"
    },
    cookies={
      "espn_s2": str(ESPN_S2)
    },
  )

  data = res.json()
  teams = data["teams"]
  
  # Subset the data further to return a concise list of teams
  abbrev_team_names = []
  for team in teams:
    abbrev_team_names.append({
      "name": team["name"],
      "owner": {
        "espn_id": team["owners"][0],
        "name": data["members"][team["owners"][0]]["displayName"]
      },
    })

  # Return the list of teams as specified by the abbrev flag
  if abbrev:
    return abbrev_team_names
  else:
    return teams


def compareTeams(latest_teams):
  #####################################
  # NEEDS TO BE UPDATED           #####
  #####################################

  # Compare the team names to what is saved in the leagueTeams.json file
  with open('leagueTeams.json', 'r') as json_file:
    cached_teams = json.load(json_file)
    compare = []
    for team in latest_teams['teams']:
      compare.append({
        "name": team["name"],
        "owner": {
          "espn_id": team["owner_id"],
          "name": team["owner_name"]
        }
      })
    if compare == cached_teams:
      print("No changes to the teams")
    else:
      # update the existing contents of the JSON file with the new "espn_team_name" value and updated the modified data metadata
      print("Needs to be updated")
  