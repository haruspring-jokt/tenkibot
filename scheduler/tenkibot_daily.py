from slackclient import SlackClient
import os

slack_token = os.environ['SLACKBOT_API_TOKEN']

sc = SlackClient(slack_token)

# for channel in data['channels']:
#     print(channel['id'], channel['name'])
