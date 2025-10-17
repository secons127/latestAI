# 2) 파라미터 맛보기 (온도/토큰/컨텍스트)
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


options = {
    "temperature": 0.2,   # 창의성/일관성
    "num_ctx": 4096,      # 컨텍스트 윈도(메모리/VRAM 영향)
    "num_predict": 256    # 생성 토큰 제한
}

resp = ollama.chat(
    model='gemma3:4b',
    messages=[{"role": "user", "content": "한 문단짜리 한국어 격언을 창의적으로 지어줘."}],
    options=options
)
print(resp['message']['content'])

# 팁: temperature 낮추면 사실 중심/일관성이, 높이면 창의성이 올라갑니다.

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