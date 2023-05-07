import os
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from flask_app.config.helper import initFirstGlanceBot
from flask_app import server
from flask import request

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

app = App(token=SLACK_BOT_TOKEN)

handler = SlackRequestHandler(app)

BotTypes = {
    'first-glance': initFirstGlanceBot
    # 'full-analysis': initFullAnalysisBot
}

def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return print(response["user_id"])
    except SlackApiError as e:
        print(f"Error: {e}")

# @app.event("app_mention")
# def event_test(event, say):
#     say("What's up?")
    
@app.event("app_mention")
def handle_mentions(body, say):
    
    text = body["event"]["text"]

    # Remove bot mention from the text
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()
    
    # Check request type and remove it from the text
    bot_type = text.split()[0]
    text = text.replace(bot_type, "").strip()

    response = BotTypes[bot_type](text, say)
    
    say(response)


@server.route('/slack/events', methods=['POST'])
def slack_events():
    return handler.handle(request)