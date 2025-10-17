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

reviews = [
    "배송이 빠르고 포장도 안전했어요.",
    "설명과 다른 제품이 왔고 반품 진행이 너무 느렸습니다.",
    "가격은 좋지만 내구성이 아쉽네요."
]

label_set = ["positive", "neutral", "negative"]

# 리뷰 분류 후 Slack 메시지 전송
for r in reviews:
    prompt = f"""
    아래 리뷰를 {label_set} 중 하나로 분류하고, 한 문장 근거를 제시해.
    JSON만 출력:
    {{"label": <label>, "reason": <string>}}
    리뷰: "{r}"
    """
    
    # Ollama API 호출하여 리뷰 분류 결과 받기
    out = ollama.chat(
        model='gemma3:4b',
        messages=[{"role": "user", "content": prompt}],
        format='json',
        options={"temperature": 0}
    )
    
    result = out['message']['content']
    print(f"Review: '{r}' -> {result}")

    # Slack 메시지 전송
    try:
        response = client.chat_postMessage(
            channel=channel_name,
            text=result  
        )
        print("메시지가 성공적으로 전송되었습니다.")
    except SlackApiError as e:
        print(f"메시지 전송에 실패했습니다: {e.response['error']}")
