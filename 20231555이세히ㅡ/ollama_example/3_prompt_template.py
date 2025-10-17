# 3) 프롬프트 템플릿화 (함수로 래핑)
import ollama
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

def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


print(ask('gemma3:4b', "대한민국을을 한 문장으로 설명해줘."))

try:
# chat_postMessage API 호출
    response = client.chat_postMessage(
    channel=channel_name,
    text=(ask('gemma3:4b', "대한민국을을 한 문장으로 설명해줘."))
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    # API 호출 실패 시 에러 코드를 확인합니다.
    # 에러 원인: 토큰이 유효하지 않거나, 봇이 채널에 없거나, 권한이 부족한 경우 등
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
