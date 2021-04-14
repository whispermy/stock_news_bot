# import os
# # Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# # WebClient insantiates a client that can call API methods
# # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
# client = WebClient(token=os.environ.get("xoxb-1949658563270-1953364834789-Rxavpb60oLgZl1ma2LS3el8v"))
# # ID of channel you want to post message to
# channel_id = "#general"

# try:
#     # Call the conversations.list method using the WebClient
#     result = client.chat_postMessage(
#         channel=channel_id,
#         text="Hello world!"
#         # You could also use a blocks[] array to send richer content
#     )
#     # Print result, which includes information about the message (like TS)
#     print(result)

# except SlackApiError as e:
#     print(f"Error: {e}")

import requests
import json
from datetime import datetime
import time
import locale 

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    # data={"channel": channel,"text": text}
    # print(data)
    print(response)
 
# def post_message2(token, diction):
#     response = requests.post("https://slack.com/api/chat.postMessage",
#         headers={"Authorization": "Bearer "+token},
#         data=diction
#     )
#     # print("dictionary")
#     # print(json.dumps(diction))
#     print(response)
 

myToken = "slack-bot-token"
# dic = {'channel': '#general', 'text': ['hello\nhelllll\nhi']}
# dic['text'].append(0000)

# print(dic)

print(locale.getlocale())
locale.setlocale(locale.LC_ALL, '')
print(locale.getlocale())

today = datetime.now().date()
print(today)
print(today.strftime('%Y. %m. %d.'))
print(today.strftime('%Y년 %m월 %d일 %A'))

# print(today.strftime('%Y년 %m월 %d일 %A'.encode('unicode-escape').decode()
#     ).encode().decode('unicode-escape')
# )

# news_list = ['news1','nes3','1235g','1231241rf','dsfasdasdgasdg']
# val = '123124'
# # news_list.append('asdf'+now)
# slack_msg = ''

# for n in news_list:
#     slack_msg = slack_msg+'\n'+n
# print(slack_msg)

# post_message(myToken,'#general',slack_msg)

# post_message2(myToken,dic)


