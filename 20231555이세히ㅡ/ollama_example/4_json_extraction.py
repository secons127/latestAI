# 4) 구조화 출력(JSON)로 정보추출
import ollama
import json
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


# ============================================================================
# 1️⃣ 주문 JSON 추출
# ============================================================================
text = """
주문 3건:
1) 상품: 무선마우스, 수량 2, 가격 25,000원
2) 상품: 기계식 키보드, 수량 1, 가격 89,000원
3) 상품: USB-C 케이블, 수량 3, 가격 9,900원
총 배송지는 서울시 강남구 테헤란로 1
"""

prompt = f"""
아래 텍스트에서 주문 항목을 JSON으로 추출해.
스키마:
{{
  "orders":[{{"item":str,"qty":int,"price_krw":int}}],
  "shipping_address": str,
  "total_price_krw": int
}}
텍스트:
{text}
반드시 JSON만 출력.
"""

resp = ollama.chat(
    model='gemma3:4b',
    messages=[{"role": "user", "content": prompt}],
    format='json',
    options={"temperature": 0}
)

data = json.loads(resp['message']['content'])
print(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================================
# 2️⃣ 영화 리뷰 분석 (인터스텔라)
# ============================================================================
print("\n" + "="*80)
print("🎬 [미션] 영화 리뷰 분석")
print("="*80)

review_text = """
크리스토퍼 놀란 감독의 '인터스텔라'는 SF 장르의 걸작이다.
시각 효과가 정말 환상적이고, 한스 짐머의 음악이 영화와 완벽하게 어우러진다.
스토리도 감동적이며 과학적 고증도 뛰어나다.
다만 러닝타임이 169분으로 너무 길고, 일부 과학 설명이 일반 관객에게는 어렵게 느껴질 수 있다.
그럼에도 불구하고 꼭 봐야 할 영화다. 5점 만점에 4.5점을 주고 싶다.
"""

review_prompt = f"""
아래 영화 리뷰 텍스트에서 정보를 추출하여 JSON으로 출력해줘.

스키마:
{{
  "title": str,
  "director": str,
  "genre": str,
  "rating": float,
  "pros": [str],
  "cons": [str],
  "recommended": bool
}}

리뷰 텍스트:
{review_text}

반드시 JSON만 출력하고, 텍스트에서 유추 가능한 모든 정보를 포함해줘.
"""

review_resp = ollama.chat(
    model='gemma3:4b',
    messages=[{"role": "user", "content": review_prompt}],
    format='json',
    options={"temperature": 0}
)

review_data = json.loads(review_resp['message']['content'])
print("\n📊 추출된 영화 정보:")
print(json.dumps(review_data, indent=2, ensure_ascii=False))

print("\n" + "-"*80)
print(f"🎬 영화: {review_data.get('title', 'N/A')}")
print(f"🎥 감독: {review_data.get('director', 'N/A')}")
print(f"🎭 장르: {review_data.get('genre', 'N/A')}")
print(f"⭐ 평점: {review_data.get('rating', 'N/A')}/5.0")
print(f"👍 추천: {'예' if review_data.get('recommended', False) else '아니오'}")

print(f"\n✅ 장점:")
for i, pro in enumerate(review_data.get('pros', []), 1):
    print(f"  {i}. {pro}")

print(f"\n❌ 단점:")
for i, con in enumerate(review_data.get('cons', []), 1):
    print(f"  {i}. {con}")

print("="*80)


# ============================================================================
# 3️⃣ 추가 연습 과제 수행 (기생충, 아바타)
# ============================================================================
extra_reviews = [
    {
        "title_hint": "기생충",
        "text": """봉준호 감독의 '기생충'은 블랙 코미디 스릴러로,
        계급 갈등을 예리하게 그려냈다. 연출이 탁월하고 메시지가 깊다.
        다만 잔인한 장면이 일부 불쾌할 수 있다. 평점은 4.8점."""
    },
    {
        "title_hint": "아바타",
        "text": """제임스 카메론 감독의 '아바타'는 판타지 액션 영화로,
        시각효과와 3D 기술이 혁신적이다. 스토리는 단순하지만 감동적이다.
        평점은 4.3점."""
    }
]

extra_results = []

for r in extra_reviews:
    prompt = f"""
아래 영화 리뷰 텍스트에서 정보를 추출하여 JSON으로 출력해줘.

스키마:
{{
  "title": str,
  "director": str,
  "genre": str,
  "rating": float,
  "pros": [str],
  "cons": [str],
  "recommended": bool
}}

리뷰 텍스트:
{r['text']}

반드시 JSON만 출력하고, 텍스트에서 유추 가능한 모든 정보를 포함해줘.
"""

    print(f"\n🎬 '{r['title_hint']}' 리뷰 분석 중...")
    resp = ollama.chat(
        model='gemma3:4b',
        messages=[{"role": "user", "content": prompt}],
        format='json',
        options={"temperature": 0}
    )
    parsed = json.loads(resp['message']['content'])
    extra_results.append(parsed)
    print(f"✅ {parsed.get('title', r['title_hint'])} 분석 완료")


# ============================================================================
# 4️⃣ Slack으로 결과 전송 (추가 리뷰만)
# ============================================================================
summary_lines = []
for r in extra_results:
    title = r.get('title', 'N/A')
    rating = r.get('rating', 'N/A')
    rec = "추천 👍" if r.get('recommended', False) else "비추천 👎"
    summary_lines.append(f"🎬 *{title}* — ⭐ {rating}/5.0 — {rec}")

summary_text = "\n".join(summary_lines)

try:
    response = client.chat_postMessage(
        channel=channel_name,
        text=f"*🎯 추가 영화 리뷰 분석 결과*\n{summary_text}"
    )
    print("✅ 추가 리뷰 결과가 Slack으로 전송되었습니다.")
except SlackApiError as e:
    print(f"❌ Slack 전송 실패: {e.response['error']}")
