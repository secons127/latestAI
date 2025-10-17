import ollama
from sys import stdout
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)

client = WebClient(token=slack_token)

channel_name = "C09KT7G94F4"

# 스트리밍 요청
stream = ollama.chat(
    model='gemma3:4b',  
    messages=[{"role": "user", "content": "생성형 AI의 장단점을 항목별로 정리해줘."}],
    stream=True,  # 스트리밍
    options={"temperature": 0.3}
)

buf = []
for chunk in stream:
    token = chunk['message']['content']
    buf.append(token)
    stdout.write(token)
stdout.flush()

# 전체 응답 출력
full_response = "".join(buf)
print("\n\n전체 응답:", full_response)

# Slack 메시지 전송
try:
    response = client.chat_postMessage(
        channel=channel_name,
        text=full_response  
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
