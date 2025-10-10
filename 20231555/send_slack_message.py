import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()
# 1. SLACK_BOT_TOKEN 이라는 이름의 환경 변수에서 토큰을 불러옵니다.
# 보안을 위해 코드에 직접 토큰을 입력하는 것은 권장하지 않습니다.
#try:
# slack_token = os.environ["SLACK_BOT_TOKEN"]
#except KeyError:
# print("오류: SLACK_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
# print("스크립트 실행 전 토큰을 설정해주세요. 예: export
#SLACK_BOT_TOKEN='xoxb- .'")
# exit(1)
# .env 환경 변수에서 토큰을 불러옵니다.
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)
# WebClient 인스턴스 생성
client = WebClient(token=slack_token)
# 2. 메시지를 보낼 채널 ID 또는 채널 이름을 입력합니다.
channel_name = "C09KT7G94F4" # 예: "#general", "#random" 등
# 3. 보낼 메시지 내용을 입력합니다.
message_text = "안녕하세요! Slack API를 통해 보내는 테스트 메시지입니다. [byjslee82]"
try:
# chat_postMessage API 호출
    response = client.chat_postMessage(
    channel=channel_name,
    text=message_text
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
# API 호출 실패 시 에러 코드를 확인합니다.
# 에러 원인: 토큰이 유효하지 않거나, 봇이 채널에 없거나, 권한이 부족한 경우 등
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")