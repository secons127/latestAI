# 12) Few-shot Learning — 예시로 패턴 학습시키기
import ollama


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


print("=" * 60)
print("예제 1: 감정 분석 (Few-shot)")
print("=" * 60)

# Zero-shot (예시 없이)
zero_shot = """
다음 리뷰의 감정을 분석해줘:
"배송이 너무 늦어서 실망했어요."
"""
print("\n[Zero-shot 결과]")
print(ask('gemma3:1b', zero_shot, temperature=0))

# Few-shot (예시 제공)
few_shot = """
다음 예시를 참고해서 리뷰의 감정을 분석해줘:

예시1:
리뷰: "제품이 기대 이상이에요! 강력 추천합니다."
감정: 긍정 (positive)
강도: 매우 강함 (5/5)

예시2:
리뷰: "가격은 괜찮은데 품질이 별로예요."
감정: 부정 (negative)
강도: 중간 (3/5)

예시3:
리뷰: "그냥 보통이에요. 특별한 건 없네요."
감정: 중립 (neutral)
강도: 약함 (2/5)

이제 다음 리뷰를 분석해줘:
리뷰: "배송이 너무 늦어서 실망했어요."
감정: 
강도:
"""
print("\n[Few-shot 결과]")
print(ask('gemma3:1b', few_shot, temperature=0))


print("\n" + "=" * 60)
print("예제 2: 데이터 정규화 (Few-shot)")
print("=" * 60)

normalization_prompt = """
다음 예시를 보고 전화번호를 표준 형식으로 변환해줘:

예시:
입력: 010-1234-5678 → 출력: +82-10-1234-5678
입력: 01012345678 → 출력: +82-10-1234-5678
입력: 010 1234 5678 → 출력: +82-10-1234-5678
입력: 02-123-4567 → 출력: +82-2-123-4567

이제 다음을 변환해줘:
입력: 0312345678
출력:
"""
print(ask('gemma3:1b', normalization_prompt, temperature=0))


print("\n" + "=" * 60)
print("예제 3: 코드 스타일 변환 (Few-shot)")
print("=" * 60)

code_style_prompt = """
다음 예시를 보고 함수 이름을 camelCase에서 snake_case로 변환해줘:

예시:
getUserName() → get_user_name()
calculateTotalPrice() → calculate_total_price()
isValidEmail() → is_valid_email()

이제 다음을 변환해줘:
getOrderItemList()
"""
print(ask('gemma3:1b', code_style_prompt, temperature=0))


print("\n" + "=" * 60)
print("예제 4: 엔티티 추출 (Few-shot with JSON)")
print("=" * 60)

entity_extraction = """
다음 예시를 보고 텍스트에서 엔티티를 추출해줘:

예시1:
텍스트: "김철수 부장은 2024년 3월 15일에 서울 본사에서 회의를 진행했다."
{
  "이름": "김철수",
  "직급": "부장",
  "날짜": "2024-03-15",
  "장소": "서울 본사",
  "행동": "회의 진행"
}

예시2:
텍스트: "이영희 과장이 부산 지점에서 10월 1일 프레젠테이션을 발표했다."
{
  "이름": "이영희",
  "직급": "과장",
  "날짜": "10-01",
  "장소": "부산 지점",
  "행동": "프레젠테이션 발표"
}

이제 다음 텍스트를 분석해줘 (JSON만 출력):
텍스트: "박민수 대리는 2024년 5월 20일 대전 사무실에서 교육을 실시했다."
"""
result = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": entity_extraction}],
    format='json',
    options={"temperature": 0}
)
print(result['message']['content'])


print("\n" + "=" * 60)
print("예제 5: 멀티턴 Few-shot (대화 이력 활용)")
print("=" * 60)

# 메시지 배열로 Few-shot 구성
messages = [
    {"role": "system", "content": "너는 고객 문의에 친절하고 전문적으로 답변하는 AI 어시스턴트야."},
    
    # Few-shot 예시 1
    {"role": "user", "content": "배송이 언제 되나요?"},
    {"role": "assistant", "content": "주문하신 상품은 평균 2-3일 내 배송됩니다. 주문번호를 알려주시면 정확한 배송 상태를 확인해드리겠습니다."},
    
    # Few-shot 예시 2
    {"role": "user", "content": "환불하고 싶어요."},
    {"role": "assistant", "content": "환불을 도와드리겠습니다. 구매일로부터 30일 이내 제품은 무료 환불이 가능합니다. 주문번호와 환불 사유를 알려주시면 처리해드리겠습니다."},
    
    # 실제 질문
    {"role": "user", "content": "교환은 어떻게 하나요?"}
]

response = ollama.chat(
    model='gemma3:1b',
    messages=messages,
    options={"temperature": 0.3}
)
print(response['message']['content'])


print("\n" + "=" * 60)
print("예제 6: Chain-of-Thought Few-shot (단계적 사고)")
print("=" * 60)

cot_prompt = """
다음 예시를 보고 단계별로 문제를 풀어줘:

예시:
문제: 사과 3개에 2,000원이면 사과 7개는 얼마인가?
풀이:
1단계: 사과 1개 가격 계산 → 2,000 ÷ 3 = 약 667원
2단계: 사과 7개 가격 계산 → 667 × 7 = 4,669원
답: 약 4,669원

이제 다음 문제를 같은 방식으로 풀어줘:
문제: 책 5권에 45,000원이면 책 12권은 얼마인가?
풀이:
"""
print(ask('gemma3:1b', cot_prompt, temperature=0))


print("\n" + "=" * 60)
print("예제 7: 카테고리 분류 Few-shot")
print("=" * 60)

category_prompt = """
다음 예시를 보고 상품을 카테고리로 분류해줘:

"무선 마우스" → 전자제품 > 컴퓨터 주변기기
"운동화" → 패션/의류 > 신발
"노트북" → 전자제품 > 컴퓨터
"청바지" → 패션/의류 > 하의
"이어폰" → 전자제품 > 오디오

이제 다음 상품을 분류해줘:
"기계식 키보드" →
"등산화" →
"무선 충전기" →
"""
print(ask('gemma3:1b', category_prompt, temperature=0))


print("\n" + "=" * 60)
print("예제 8: 동적 Few-shot (예시를 변수로 관리)")
print("=" * 60)

# Few-shot 예시를 데이터로 관리
examples = [
    {"input": "매우 좋아요!", "output": "긍정"},
    {"input": "최악이에요.", "output": "부정"},
    {"input": "그냥 그래요.", "output": "중립"}
]

# 동적으로 프롬프트 생성
def create_few_shot_prompt(examples, new_input):
    prompt = "다음 예시를 보고 감정을 분류해줘:\n\n"
    for ex in examples:
        prompt += f'"{ex["input"]}" → {ex["output"]}\n'
    prompt += f'\n이제 분류해줘:\n"{new_input}" → '
    return prompt

test_inputs = ["완전 만족합니다!", "돈 아까워요", "보통입니다"]

for test in test_inputs:
    prompt = create_few_shot_prompt(examples, test)
    result = ask('gemma3:1b', prompt, temperature=0)
    print(f'"{test}" → {result}')


print("\n" + "=" * 60)
print("Few-shot Learning 완료!")
print("=" * 60)

