import ollama
import pandas as pd
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


paragraphs = [
    "전자상거래에서는 고객지원 자동화가 중요한 과제로 부상했다. AI 챗봇과 검색 시스템이 핵심이다.",
    "검색결합형(RAG) 접근은 내부 문서를 참조하여 최신 정보를 제공한다. 기업 도입이 증가하고 있다.",
    "로컬 추론은 개인정보와 기밀문서 보호에 유리하다. Ollama 같은 도구가 이를 가능하게 한다."
]

rows = []
for i, p in enumerate(paragraphs, start=1):
    out = ask('gemma3:4b', f"두 문장으로 요약하고 핵심 키워드 3개를 해시태그로: {p}", temperature=0.2)
    rows.append({"id": i, "summary": out})

df = pd.DataFrame(rows)
print(df)

try:
    # chat_postMessage API 호출
    response = client.chat_postMessage(
        channel=channel_name,
        text=df.to_string(index=False)  
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    # API 호출 실패 시 에러 코드를 확인합니다.
    # 에러 원인: 토큰이 유효하지 않거나, 봇이 채널에 없거나, 권한이 부족한 경우 등
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
