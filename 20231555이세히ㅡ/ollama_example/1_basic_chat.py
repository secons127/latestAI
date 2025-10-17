# 1) "헬로 LLM" — 가장 기본 대화
import ollama
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)
# WebClient 인스턴스 생성
client = WebClient(token=slack_token)
# 2. 메시지를 보낼 채널 ID 또는 채널 이름을 입력합니다.
channel_name = "C09KT7G94F4" # 예: "#general", "#random" 등


resp = ollama.chat(
    model='gemma3:4b',
    messages=[
        {"role": "system", "content": "You are a concise Korean assistant."},
        {"role": "user", "content": "LangChain의 필요성을 한 문장으로 설명해줘."}
    ]
)


try:
# chat_postMessage API 호출
    response = client.chat_postMessage(
    channel=channel_name,
    text=resp['message']['content']
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    # API 호출 실패 시 에러 코드를 확인합니다.
    # 에러 원인: 토큰이 유효하지 않거나, 봇이 채널에 없거나, 권한이 부족한 경우 등
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
