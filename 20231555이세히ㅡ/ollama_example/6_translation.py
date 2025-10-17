# 6) 번역(Translation) — 스타일 전환 포함
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

# ask 함수 정의
def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[ 
            {"role": "system", "content": system}, 
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']

# 영어 문장
english = """
We propose a lightweight retrieval-augmented pipeline for customer support emails.
The system combines semantic search with local LLM inference to provide accurate responses.
"""

# 번역 프롬프트
prompt = f"""
다음 영어 문단을 '대학 강의노트' 스타일의 한국어로 번역해줘.
필요하면 용어를 각주 형식으로 보충 설명 (각주는 괄호로).
텍스트:
{english}
"""

# ask 함수 호출하여 번역 결과 받기
translated_text = ask('gemma3:4b', prompt, temperature=0.2)

print(translated_text)

# Slack 메시지 전송
try:
    response = client.chat_postMessage(
        channel=channel_name,
        text=translated_text 
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
