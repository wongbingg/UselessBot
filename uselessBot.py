
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

#conda activate py38 로 가상환경을 만들어주고 시작
# 환경변수 값을 가져옵니다.
load_dotenv()
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")
print('slack_bot_token : ' + slack_bot_token)
print('slack_app_token : ' + slack_app_token)

# 앱을 초기화 합니다.
app = App(token=slack_bot_token)

@app.event("message")
def handle_message_event(event, say):

    if 'subtype' in event and event['subtype'] == 'bot_message':
        return
    
    # 원본 메세지를 가져옵니다.
    user_message = event['text']

    # 새로운 메시지를 만듭니다.
    response_message = f"CustomBOT : {user_message}"

    # 메세지를 보낸 채널에 응답 메시지를 보냅니다.
    say(response_message)

if __name__ == "__main__":
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()

# 종료 Ctrl + C
