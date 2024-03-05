import json
import requests

# Define the API key for Google Cloud Generative Language API
API_KEY = "AIzaSyBE9CIN4RMUKl0qUcSScFr3avWbEUjUOos"

# Define the conversation state
conversation_state = {}

def generate_response(prompt):
  """Generates a response to a prompt using the Google Cloud Generative Language API,
  considering the conversation state.

  Args:
    prompt: The prompt to send to the API, including the previous user input.

  Returns:
    The response from the API.
  """

  # Construct the API request URL
  url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}'

  # Set the content type header for JSON
  headers = {'Content-Type': 'application/json'}
  data = {
    "contents": [
        {
            "parts": [{"text": f"{prompt}"}]
        }
    ]
}

  # Prepare the request data, incorporating previous user input
#   data = {
#       "contents": [
#           {
#               "parts": [
#                   {
#                       "text": f"{prompt}"
#                   }
#               ]
#           }
#       ]
#   }
  data = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": "你知道王建民嗎？"}]
        },
        {
            "role": "model",
            "parts": [{"text": "我知道王建民。王建民，1980年3月31日出生於台灣台中市，是一位前台灣棒球選手，司職投手。他曾效力於中華職棒的興農牛隊，美國職棒的紐約洋基隊、華盛頓國民隊和芝加哥白襪隊，以及中國棒球聯賽的北京猛虎隊。\n\n王建民是台灣史上第一位大聯盟先發勝投破百的投手，也是第一位入選大聯盟全明星賽的台灣選手。他在2006年締造19勝6敗、 防禦率3.63的優異成績，並在季後賽拿下3勝0敗的戰績，幫助洋基隊奪得世界大賽冠軍。王建民也因此成為台灣的棒球英雄，並獲得「台灣之光」的稱號。\n\n然而，王建民在2008年季初因傷缺陣，並在2009年進行了韌帶移植手術。此後，他的成績大幅下滑，並在2012年離開了大聯盟。王建民於2013年回歸中華職棒，效力於義大犀牛隊。2016年，他宣布正式退休。\n\n王建民的職業生涯戰績為127勝72敗， 防禦率3.92，三振數1718次。他是台灣棒球史上最成功的投手之一，也是台灣人民的驕傲。"}]
        },
        {
            "role": "user",
            "parts": [{"text": "他現在在哪裡？"}]
        },
    ]
}

  # Send a POST request to the API using the requests library
  response = requests.post(url, headers=headers, json=data)

  # Parse the JSON response from the API and prettify it for better readability
  json_response = json.dumps(response.json(), indent=4, ensure_ascii=False)

  return json_response

def model_response(text):
  data = {
    "role": "model",
    "parts": [{"text": f"{text}"}] 
    }
  return data

def user_input(text):
  data = {
    "role": "user",
    "parts": [{"text": f"{text}"}] 
    }
  return data

# Start the conversation loop
while True:
  # Get the user's input
  user_input = input("請問您想說什麼？\n")

  # Update the conversation state
  conversation_state["previous_input"] = user_input

  # Generate a response to the user's input
  response = generate_response(user_input)

  # Parse the response from the API
  response_data = json.loads(response)

  # Get the generated text from the response
  generated_text = response_data["candidates"][0]['content']['parts'][0]['text']

  # Print the generated text
  print(f"Bard：{generated_text}")
