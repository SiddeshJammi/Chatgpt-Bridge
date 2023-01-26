import os 
from dotenv import load_dotenv
import discord
import openai

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
global msg_log
msg_log = []

def get_response(msg_log):
    query = ''.join(msg_log)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= query,
    temperature=0.0,
    max_tokens=350,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    )
    return response


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global msg_log
    if message.content.startswith('$question'):
        msg = message.content.replace('$question','')
        msg_log.append(' '+str(message.author.id)+': '+msg)
        try:
            resp = get_response(msg_log)
            reply = resp['choices'][0]['text'].replace(str(resp),"")
            reply = reply.replace('Ai:','')
            msg_log.append(' Ai: '+reply)
            await message.channel.send(reply)
        except(openai.APIError):
            await message.channel.send(":robot: -> beepboop, currently overloaded, try again later")

    if message.content.startswith('$code'):
        msg = message.content.replace('$code','')
        msg_log.append(' '+str(message.author.id)+': '+msg)
        try:
            resp = get_response(msg)
            reply = resp['choices'][0]['text'].replace(str(resp),"")
            reply = reply.replace('Ai:','')
            msg_log.append(' Ai: '+reply)
            await message.channel.send('`' + reply + '`')
        except:
            await message.channel.send(":robot: -> beepboop, currently overloaded, try again later ")
    
    if message.content.startswith('$clear'):
        if msg_log == []:
            await message.channel.send('Nothing to see here :eyes:')
        else:
            msg_log = []
            await message.channel.send('Cleared all messages  :leaves: :leaves: :broom:')

token  = os.getenv("TOKEN")
client.run(token)   