from fastapi import FastAPI, Request
from webexteamssdk import WebexTeamsAPI
from modules.parse_manager import load_yaml_config
import json


def send_message(message):
   
   var = load_yaml_config('config/config.yaml')
   TOKEN = var.get('WEBEX_TOKEN')
   recipient = var.get('RECIPIENT')
   webex = WebexTeamsAPI(TOKEN)
   webex.messages.create(markdown=message,toPersonEmail=recipient)
   print(f'Message sent!')

app = FastAPI()

@app.post('/webhook')
async def webhook(request: Request):

   try:
      payload = await request.json()
      message = json.dumps(payload)
      _ = send_message(message)

   except:
      _ = send_message('No payload!')

   return {'ack': True}
