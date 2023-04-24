from fastapi import FastAPI, Request
from webexteamssdk import WebexTeamsAPI
import os


def send_message(message):
   TOKEN = os.environ.get('WEBEX_TOKEN')
   recipient = 'rgomezbe@cisco.com'
   webex = WebexTeamsAPI(TOKEN)
   webex.messages.create(markdown=message,toPersonEmail=recipient)
   print(f'Message sent!')

app = FastAPI()

@app.post('/webhook')
async def webhook(request: Request):

   try:
      payload = await request.json()
      data = [f'{k} : {v}' for k,v in payload.items()]
      message = '\n'.join(data)
      _ = send_message(message)

   except Exception as e:
      _ = send_message('Error processing message from vManage!')
      print(e)

   return {'ack': True}
