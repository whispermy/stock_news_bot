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
 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
        #data=json.dumps(dict_val)
    )
    print(response)
 
myToken = "xoxb-1949658563270-1953364834789-44sDT2LqthWpa8gD6qHquIUH"
dic = {'channel': '#general', 'text': 'jocoding'}
#dic['text'].append(0000)

print(dic)


# post_message(myToken,dic)
post_message(myToken,'#general',"textetetet")




