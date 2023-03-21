import os
import openai
import json
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORG_ID

# MODEL="gpt-3.5-turbo"
# MAX_TOKENS=3096
MODEL="gpt-4"
MAX_TOKENS=4096



def identifyNames(names, teamsFile):
  with open(teamsFile, 'r') as json_file:
    teams = json.load(json_file)
    identified_names = []
    for name in names:
      answer = '{"teamId": "{Team ID Number}", "name": "{Preferred Team Name}"}'
      response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="""
          Review this data which describes the different names that 12 different teams go by:
          '''json
          {teams}
          '''
          
          Categorize {name} as one of the 12 teams.  If the name does not belong to any of the teams, respond with "None". Specify the categorize team name and team id in the following format:
          '''json
          {answer}
          '''
          """.format(teams=teams['teams'], name=name, answer=answer),
        max_tokens=2048,
        temperature=0.5,
        n=1,
      )
      print(response)
      identified_names.append(response['choices'][0]['text']) # type: ignore
    return identified_names
  

def generateTalkingPoints(names):
  print("Here's the names I got:", names)
  talking_points = []
  for name in names:
    # Open the team_rosters.json file, and pull the roster for this team using the team_id
    abbrev_roster = []
    with open('team_rosters.json', 'r') as json_file:
      rosters = json.load(json_file)
      print("it looks like I have", len(rosters), "rosters")
      for team in rosters:
        if int(team['teamId']) != int(name['teamId']):
          print("This team:", team['teamId'], "isn't the team I'm looking for:", name['teamId'])
          continue
        else:
          roster = team['roster']
          print("This is the roster I found:", roster)
          for player in roster:
            abbrev_roster.append(player['name'])
          break

    print("Here is the roster for", name['name'], ":", abbrev_roster)
    if abbrev_roster == []:
      return "I can't seem to find the rosters for those teams...  Please try again later."

    # Make API call to GPT for talking points
    answer = '{"teamId": {Team ID}, "topPerformers": [{"name": "{Top Performers Name}", "reasonForSelection": "{Top Performer Selection Reason}"}], "bottomPerformers": [{"name": "{Bottom Performers Name}", "reasonForSelection": "{Bottom Performer Selection Reason}"}]}'
    response = openai.ChatCompletion.create(
      model=MODEL,
      messages= [
        {"role": "system", "content": "You are an analyst that identifies both positive and negative highlights about a hypothetical baseball team"},
        {
          "role": "user", 
          "content": f"""
            I have a team named {name['name']} that I need evaluate how good of a team they are.  First, review the roster for this team:
            {abbrev_roster}
            
            Please select 3 names from the roster to be the team's best performers on this team and 3 names from the roster to be the team's lowest performers and briefly make up a reason why you think they are the best and worst performers on the team.
            Return your answer as code in the following JSON format:
            {answer}

            Do not give me any other response other than the JSON
            """
        }
      ],
      max_tokens=MAX_TOKENS,
      n=1,
    )
    print(response)

    try:
      response_json = json.loads(response['choices'][0]['message']['content']) # type: ignore
      talking_points.append({"teamId": name['teamId'], "name": name['name'], "talkingPoints": response_json})
    except:
      print("Error parsing json")
      return "I'm sorry... I'm having trouble doing my research on these teams.  Please try again later."
    
  return talking_points



def writePregameHit(talking_points):
  if len(talking_points) != 2:
    return "You gave me more than two names.  They can't all be playing each other today!"
  else:
    # Make API call to GPT for recipe
    response = openai.ChatCompletion.create(
      model=MODEL,
      messages= [
        {"role": "system", "content": "You are an entertaining blog writer for a popular sports blog"},
        {
          "role": "user", 
          "content": f"""
            You are now a blog writer for a popular sports blog.  There is a new baseball league with 12 teams called the Cum Dogs.
            You must write a pregame analysis for the upcoming game between the {talking_points[0]['name']} and the {talking_points[1]['name']} in the league.
            Please write a pregame analysis for these two teams that will go on the front page of ESPN and write the analysis as though you are a commentator for WWE.

            For more context on {talking_points[0]['name']}, choose three talking points from the following data to highlight:
            {talking_points[0]['talkingPoints']}

            For more context on {talking_points[1]['name']}, choose three talking point from the following data to highlight:
            {talking_points[1]['talkingPoints']}

            You are free to reference any other talking points about the teams you'd like, as long as they are true.
            """
        }
      ],
      max_tokens=MAX_TOKENS,
      n=1,
    )
    return response['choices'][0]['message']['content'] # type: ignore
