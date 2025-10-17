# 14) Chain of Thought (CoT) 프롬프팅 - 단계별 추론
import ollama


def compare_with_without_cot(model, question):
    """CoT 사용 여부에 따른 답변 비교"""
    print("\n" + "=" * 80)
    print(f"질문: {question}")
    print("=" * 80)
    
    # 1. 일반 프롬프트 (CoT 없음)
    print("\n[1] 일반 프롬프트 (CoT 없음)")
    print("-" * 80)
    response1 = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": question}],
        options={"temperature": 0.3}
    )
    print(response1['message']['content'])
    
    # 2. CoT 프롬프트 (단계별 추론 요청)
    print("\n[2] CoT 프롬프트 (단계별 추론)")
    print("-" * 80)
    cot_prompt = f"""{question}

단계별로 생각해봅시다:"""
    
    response2 = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": cot_prompt}],
        options={"temperature": 0.3}
    )
    print(response2['message']['content'])
    
    print("\n" + "=" * 80)


# ============================================================================
# 1. 수학 문제 - CoT의 가장 효과적인 사용 사례
# ============================================================================
print("\n🔢 수학 문제 해결 - CoT 비교")

compare_with_without_cot(
    'gemma3:1b',
    "한 가게에 사과가 23개 있었습니다. 아침에 16개를 팔고, 점심에 29개를 새로 들여왔습니다. 오후에 12개를 더 팔았다면 현재 몇 개의 사과가 남았을까요?"
)


# ============================================================================
# 2. 논리 문제
# ============================================================================
print("\n🧩 논리 문제 - CoT 비교")

compare_with_without_cot(
    'gemma3:1b',
    "모든 새는 날 수 있다. 펭귄은 새다. 따라서 펭귄은 날 수 있다. 이 논리에 문제가 있나요?"
)


# ============================================================================
# 3. Few-Shot CoT - 예시를 통한 학습
# ============================================================================
print("\n\n📚 Few-Shot CoT - 예시를 통한 학습")
print("=" * 80)

few_shot_cot_prompt = """다음과 같이 단계별로 생각하여 문제를 풀어주세요.

예시 1:
질문: 버스에 탑승객이 15명 있었습니다. 정류장에서 7명이 내리고 8명이 탔습니다. 현재 몇 명인가요?
단계별 풀이:
1. 초기 탑승객: 15명
2. 내린 사람: 7명 → 15 - 7 = 8명
3. 탄 사람: 8명 → 8 + 8 = 16명
답: 16명

예시 2:
질문: 상자에 빨간 공 12개와 파란 공 18개가 있습니다. 빨간 공 5개를 빼고 파란 공 7개를 더 넣었습니다. 전체 공은 몇 개인가요?
단계별 풀이:
1. 초기 공: 12 + 18 = 30개
2. 빨간 공 제거: 30 - 5 = 25개
3. 파란 공 추가: 25 + 7 = 32개
답: 32개

이제 다음 문제를 같은 방식으로 풀어주세요:

질문: 도서관에 소설책 45권, 과학책 38권, 역사책 27권이 있습니다. 오늘 소설책 12권과 역사책 8권을 대출했고, 과학책 15권을 새로 구입했습니다. 현재 전체 책은 몇 권인가요?"""

print(few_shot_cot_prompt)
print("\n응답:")
print("-" * 80)

response = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": few_shot_cot_prompt}],
    options={"temperature": 0.3, "num_predict": 300}
)
print(response['message']['content'])
print("=" * 80)


# ============================================================================
# 4. Zero-Shot CoT - "Let's think step by step"
# ============================================================================
print("\n\n🎯 Zero-Shot CoT - 마법의 문구")
print("연구 결과: 'Let's think step by step'만 추가해도 성능 향상!")
print("=" * 80)

questions = [
    "12 x 13 + 8 x 7을 계산해주세요.",
    "만약 내일이 어제였다면, 모레는 무슨 요일일까요? (오늘이 수요일이라면)",
    "3명이 3분 동안 3개의 사과를 먹는다면, 9명이 9개의 사과를 먹는데 몇 분이 걸릴까요?"
]

for i, q in enumerate(questions, 1):
    print(f"\n질문 {i}: {q}")
    print("-" * 80)
    
    # Zero-Shot CoT
    zero_shot_cot = f"{q}\n\nLet's think step by step:"
    
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": zero_shot_cot}],
        options={"temperature": 0.3}
    )
    print(response['message']['content'])
    print("-" * 80)


# ============================================================================
# 5. 복잡한 추론 문제 - CoT의 진가
# ============================================================================
print("\n\n🧠 복잡한 추론 문제")
print("=" * 80)

complex_problem = """한 회사에서 프로젝트 일정을 계획하고 있습니다:
- 설계 단계: 5일 소요
- 개발 단계: 설계 완료 후 시작, 12일 소요
- 테스트 단계: 개발의 50% 완료 시점부터 시작 가능, 8일 소요
- 배포 준비: 테스트와 개발이 모두 완료된 후 시작, 3일 소요

월요일에 시작한다면, 배포 준비가 완료되는 날은 언제인가요?
(주말 작업 없음, 토일요일 제외)

단계별로 자세히 계산해주세요."""

print(complex_problem)
print("\n응답:")
print("-" * 80)

response = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": complex_problem}],
    options={"temperature": 0.3, "num_predict": 500}
)
print(response['message']['content'])
print("=" * 80)


# ============================================================================
# 6. 실전 활용: 코드 디버깅
# ============================================================================
print("\n\n💻 실전 활용: 코드 디버깅 with CoT")
print("=" * 80)

debug_problem = """다음 Python 코드에 버그가 있습니다:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

scores = [85, 90, 78, 92, 88]
print(calculate_average(scores))

empty_scores = []
print(calculate_average(empty_scores))  # 에러 발생!
```

단계별로 분석해주세요:
1. 어떤 문제가 있나요?
2. 왜 에러가 발생하나요?
3. 어떻게 수정해야 하나요?
4. 수정된 코드를 제시해주세요."""

print(debug_problem)
print("\n응답:")
print("-" * 80)

response = ollama.chat(
    model='gemma3:1b',
    messages=[{"role": "user", "content": debug_problem}],
    options={"temperature": 0.3, "num_predict": 400}
)
print(response['message']['content'])
print("=" * 80)


# ============================================================================
# 7. Self-Consistency - 여러 추론 경로 비교
# ============================================================================
print("\n\n🔄 Self-Consistency - 여러 번 추론 후 가장 일관된 답 선택")
print("=" * 80)

problem = """한 농장에 닭과 토끼가 총 20마리 있습니다. 
다리 개수를 세어보니 총 56개였습니다.
닭은 다리가 2개, 토끼는 다리가 4개입니다.
닭과 토끼는 각각 몇 마리인가요?

단계별로 풀어주세요."""

print(f"문제: {problem}\n")
print("같은 문제를 3번 풀어서 결과 비교:")
print("-" * 80)

answers = []
for i in range(3):
    print(f"\n[추론 {i+1}]")
    response = ollama.chat(
        model='gemma3:1b',
        messages=[{"role": "user", "content": problem}],
        options={"temperature": 0.5}  # 약간의 변동성 허용
    )
    answer = response['message']['content']
    print(answer)
    answers.append(answer)
    print("-" * 40)

print("\n💡 Self-Consistency를 사용하면 여러 추론 경로 중 가장 자주 나오는 답을 선택합니다.")


# ============================================================================
# CoT 사용 가이드
# ============================================================================
print("\n\n" + "=" * 80)
print("📚 Chain of Thought (CoT) 사용 가이드")
print("=" * 80)

guide = """
🎯 **Chain of Thought (CoT)란?**
AI 모델이 최종 답을 내기 전에 중간 추론 단계를 생성하도록 유도하는 기법

📊 **CoT의 종류**

1. **Zero-Shot CoT**
   - "Let's think step by step" 추가
   - 예시 없이도 단계별 추론 유도
   - 가장 간단하고 효과적

2. **Few-Shot CoT**
   - 단계별 추론 예시 제공
   - 더 복잡한 문제에 효과적
   - 예시의 품질이 중요

3. **Self-Consistency**
   - 같은 문제를 여러 번 풀기
   - 가장 일관된 답 선택
   - 정확도 향상 (시간 더 소요)

✅ **CoT가 효과적인 경우**
• 수학 문제
• 논리 추론
• 복잡한 계산
• 다단계 문제 해결
• 코드 디버깅
• 의사결정 과정

❌ **CoT가 불필요한 경우**
• 단순 사실 질문
• 정의 요청
• 짧은 번역
• 간단한 분류

💡 **효과적인 CoT 프롬프트 작성법**

1. 명확한 지시:
   "단계별로 생각해봅시다"
   "Let's think step by step"
   "다음 단계로 문제를 풀어주세요"

2. 구체적 요청:
   "1단계: 문제 파악"
   "2단계: 필요한 정보 정리"
   "3단계: 계산 수행"
   "4단계: 최종 답 도출"

3. 예시 제공 (Few-Shot):
   좋은 예시 2-3개 제공
   각 예시에 명확한 단계 표시

⚙️ **CoT와 함께 사용할 파라미터**
• temperature: 0.3 (정확성 중시)
• top_p: 0.9
• num_predict: 충분히 크게 (300-500)

🚀 **실전 팁**
1. 복잡한 문제일수록 CoT 효과 큽니다
2. Few-Shot은 3-5개 예시가 적당합니다
3. Self-Consistency는 3-5번 반복이 적당합니다
4. temperature를 낮춰 일관성을 높이세요
"""

print(guide)
print("=" * 80)

