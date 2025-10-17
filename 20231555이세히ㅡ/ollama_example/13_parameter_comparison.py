import ollama
import time
import json
import pandas as pd
from typing import List
import numpy as np
import faiss
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)
channel_name = "C09KT7G94F4"  # [수정] 전송할 채널명 확인
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)
def compare_responses(model, prompt, configs, title=""):
    """여러 설정으로 같은 프롬프트를 실행하고 결과 비교"""
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80)
    print(f"프롬프트: {prompt}")
    print("-" * 80)
    results = []
    for config in configs:
        print(f"\n[설정: {config['name']}]")
        for key, value in config['options'].items():
            print(f"  {key}: {value}")
        start_time = time.time()
        resp = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options=config['options']
        )
        elapsed = time.time() - start_time
        result = resp['message']['content']
        print(f"\n응답 (소요시간: {elapsed:.2f}초):")
        print(result)
        print("-" * 80)
        results.append({
            'name': config['name'],
            'result': result,
            'time': elapsed
        })
    return results
# [추가] Slack 메시지 포맷팅을 위한 헬퍼 함수
def format_results_for_slack(title: str, prompt: str, results: List[dict]) -> str:
    """하나의 비교 섹션 결과를 Slack 메시지 형식으로 만듭니다."""
    parts = []
    # Slack 마크다운을 사용하여 제목과 프롬프트를 강조합니다.
    if "Temperature" in title:
        parts.append(":온도계: *" + title + "*")
    elif "Top-P" in title:
        parts.append(":다트: *" + title + "*")
    elif "Top-K" in title:
        parts.append(":맨_위: *" + title + "*")
    elif "Repeat Penalty" in title:
        parts.append(":반복: *" + title + "*")
    elif "Num Predict" in title:
        parts.append(":자: *" + title + "*")
    elif "복합 설정" in title:
        parts.append(":톱니바퀴: *" + title + "*")
    elif "Num CTX" in title:
        parts.append(":플로피_디스크: *" + title + "*")
    else:
        parts.append(f"*{title}*")
    parts.append(f"_*프롬프트:* {prompt}_\n")
    parts.append("=" * 40)
    for res in results:
        parts.append(f"\n*[{res['name']}]*")
        parts.append(f"_(소요시간: {res['time']:.2f}초)_")
        # 응답 내용은 코드 블록(```)으로 감싸 가독성을 높입니다.
        parts.append(f"```{res['result']}```")
        parts.append("-" * 40)
    return "\n".join(parts)
# ============================================================================
# 1. Temperature 비교
# ============================================================================
print("\n:온도계:  TEMPERATURE 비교 - 창의성과 일관성의 균형")
# ... (설명 print문 생략) ...
temp_configs = [
    {"name": "Temperature 0.0 (최소)", "options": {"temperature": 0.0, "num_predict": 100}},
    {"name": "Temperature 0.5 (보통)", "options": {"temperature": 0.5, "num_predict": 100}},
    {"name": "Temperature 1.0 (높음)", "options": {"temperature": 1.0, "num_predict": 100}},
    {"name": "Temperature 1.5 (매우 높음)", "options": {"temperature": 1.5, "num_predict": 100}},
]
temp_prompt = "혁신적인 스마트폰 앱 아이디어를 하나 제안해줘."
temp_title = "Temperature 비교 - 창의성 테스트"
temp_results = compare_responses(
    'gemma3:4b',
    temp_prompt,
    temp_configs,
    temp_title
)
# ============================================================================
# 2. Top-P (Nucleus Sampling) 비교
# ============================================================================
print("\n\n:다트: TOP-P 비교 - 토큰 선택 범위")
# ... (설명 print문 생략) ...
top_p_configs = [
    {"name": "Top-P 0.1 (매우 집중)", "options": {"top_p": 0.1, "temperature": 0.8}},
    {"name": "Top-P 0.5 (보통)", "options": {"top_p": 0.5, "temperature": 0.8}},
    {"name": "Top-P 0.9 (기본값)", "options": {"top_p": 0.9, "temperature": 0.8}},
    {"name": "Top-P 1.0 (최대)", "options": {"top_p": 1.0, "temperature": 0.8}},
]
top_p_prompt = "AI의 미래에 대해 짧게 설명해줘."
top_p_title = "Top-P 비교"
top_p_results = compare_responses(
    'gemma3:4b',
    top_p_prompt,
    top_p_configs,
    top_p_title
)
# ============================================================================
# 3. Top-K 비교
# ============================================================================
print("\n\n:맨_위: TOP-K 비교 - 고려할 토큰 개수")
# ... (설명 print문 생략) ...
top_k_configs = [
    {"name": "Top-K 5 (매우 제한)", "options": {"top_k": 5, "temperature": 0.8}},
    {"name": "Top-K 20 (제한적)", "options": {"top_k": 20, "temperature": 0.8}},
    {"name": "Top-K 40 (기본값)", "options": {"top_k": 40, "temperature": 0.8}},
    {"name": "Top-K 100 (넓음)", "options": {"top_k": 100, "temperature": 0.8}},
]
top_k_prompt = "클라우드 컴퓨팅의 장점 3가지를 나열해줘."
top_k_title = "Top-K 비교"
top_k_results = compare_responses(
    'gemma3:4b',
    top_k_prompt,
    top_k_configs,
    top_k_title
)
# ============================================================================
# 4. Repeat Penalty 비교 - 반복 방지
# ============================================================================
print("\n\n:반복: REPEAT PENALTY 비교 - 반복 억제")
# ... (설명 print문 생략) ...
repeat_configs = [
    {"name": "Repeat Penalty 1.0 (없음)", "options": {"repeat_penalty": 1.0, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.1 (기본값)", "options": {"repeat_penalty": 1.1, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.3 (강함)", "options": {"repeat_penalty": 1.3, "temperature": 0.8}},
    {"name": "Repeat Penalty 1.5 (매우 강함)", "options": {"repeat_penalty": 1.5, "temperature": 0.8}},
]
repeat_prompt = "Python의 장점을 설명해줘. 특히 'Python'이라는 단어를 여러 번 사용해서."
repeat_title = "Repeat Penalty 비교"
repeat_results = compare_responses(
    'gemma3:4b',
    repeat_prompt,
    repeat_configs,
    repeat_title
)
# ============================================================================
# 5. Num Predict 비교 - 응답 길이 제한
# ============================================================================
print("\n\n:자: NUM PREDICT 비교 - 생성 토큰 수 제한")
# ... (설명 print문 생략) ...
num_predict_configs = [
    {"name": "50 토큰 (짧음)", "options": {"num_predict": 50, "temperature": 0.3}},
    {"name": "100 토큰 (보통)", "options": {"num_predict": 100, "temperature": 0.3}},
    {"name": "200 토큰 (길음)", "options": {"num_predict": 200, "temperature": 0.3}},
    {"name": "500 토큰 (매우 길음)", "options": {"num_predict": 500, "temperature": 0.3}},
]
num_predict_prompt = "머신러닝과 딥러닝의 차이를 자세히 설명해줘."
num_predict_title = "Num Predict 비교"
num_predict_results = compare_responses(
    'gemma3:4b',
    num_predict_prompt,
    num_predict_configs,
    num_predict_title
)
# ============================================================================
# 6. 복합 설정 비교 - 실전 사용 예시
# ============================================================================
print("\n\n:톱니바퀴:  복합 설정 비교 - 실전 시나리오")
complex_configs = [
    {"name": "정확한 사실 답변용", "options": {"temperature": 0.1, "top_p": 0.9, "top_k": 20, "repeat_penalty": 1.1, "num_predict": 200}},
    {"name": "창의적 글쓰기용", "options": {"temperature": 1.0, "top_p": 0.95, "top_k": 100, "repeat_penalty": 1.3, "num_predict": 300}},
    {"name": "간결한 요약용", "options": {"temperature": 0.3, "top_p": 0.9, "top_k": 30, "repeat_penalty": 1.2, "num_predict": 100}},
    {"name": "브레인스토밍용", "options": {"temperature": 1.3, "top_p": 0.95, "top_k": 80, "repeat_penalty": 1.4, "num_predict": 250}}
]
prompt_for_scenario = "전자상거래 플랫폼을 개선할 수 있는 방법을 제안해줘."
scenario_title = "복합 설정 비교 - 목적별 최적화"
scenario_results = compare_responses(
    'gemma3:4b',
    prompt_for_scenario,
    complex_configs,
    scenario_title
)
# ============================================================================
# 7. 컨텍스트 윈도우 비교 - 메모리/처리 속도
# ============================================================================
print("\n\n:플로피_디스크: NUM_CTX 비교 - 컨텍스트 윈도우 크기")
# ... (설명 print문 생략) ...
ctx_configs = [
    {"name": "2048 토큰 (작음)", "options": {"num_ctx": 2048, "temperature": 0.3}},
    {"name": "4096 토큰 (기본)", "options": {"num_ctx": 4096, "temperature": 0.3}},
    {"name": "8192 토큰 (큼)", "options": {"num_ctx": 8192, "temperature": 0.3}},
]
long_text = """
인공지능(AI)은 컴퓨터 과학의 한 분야로, 기계가 인간의 지능적인 행동을 모방하도록 만드는 기술입니다.
최근 딥러닝의 발전으로 이미지 인식, 자연어 처리, 음성 인식 등 다양한 분야에서 획기적인 성과를 내고 있습니다.
특히 대규모 언어 모델(LLM)의 등장으로 챗봇, 번역, 코드 생성 등의 작업에서 인간 수준의 성능을 보이고 있습니다.
"""
ctx_prompt = f"다음 텍스트를 한 문장으로 요약해줘:\n\n{long_text}"
ctx_title = "Num CTX 비교"
ctx_results = compare_responses(
    'gemma3:4b',
    ctx_prompt,
    ctx_configs,
    ctx_title
)
# ============================================================================
# 파라미터 가이드 요약 (이 부분은 콘솔에만 출력됩니다)
# ============================================================================
print("\n\n" + "=" * 80)
print(":책: 파라미터 가이드 요약")
print("=" * 80)
guide = """
... (가이드 내용) ...
"""
print(guide)
print("=" * 80)
# ============================================================================
# [수정] Slack으로 모든 비교 결과(1~7번)를 나누어 전송
# ============================================================================
try:
    print("Slack으로 비교 결과 전송을 시작합니다...")
    # 전송할 모든 결과 세트를 리스트로 묶습니다.
    all_results_to_send = [
        (temp_title, temp_prompt, temp_results),
        (top_p_title, top_p_prompt, top_p_results),
        (top_k_title, top_k_prompt, top_k_results),
        (repeat_title, repeat_prompt, repeat_results),
        (num_predict_title, num_predict_prompt, num_predict_results),
        (scenario_title, prompt_for_scenario, scenario_results),
        (ctx_title, ctx_prompt, ctx_results)
    ]
    # 시작 메시지 전송
    client.chat_postMessage(
        channel=channel_name,
        text=f":로봇_얼굴: *Ollama 파라미터 비교 결과 (총 {len(all_results_to_send)}개)*\n(결과를 섹션별로 나누어 전송합니다.)"
    )
    time.sleep(1) # Slack API 속도 제한 방지
    # 각 섹션을 별도의 메시지로 전송
    for title, prompt, results in all_results_to_send:
        # 헬퍼 함수를 사용해 메시지 본문 생성
        section_message = format_results_for_slack(title, prompt, results)
        client.chat_postMessage(
            channel=channel_name,
            text=section_message
        )
        print(f"'{title}' 섹션 전송 완료.")
        time.sleep(1) # Slack API 속도 제한 방지
    print("모든 비교 결과를 Slack으로 성공적으로 전송했습니다.")
    # [선택 사항] 마지막 가이드 요약도 보내고 싶다면 이 코드의 주석을 해제하세요.
    # print("파라미터 가이드 요약 전송 중...")
    # client.chat_postMessage(
    #     channel=channel_name,
    #     text=f":책: *파라미터 가이드 요약*\n```{guide}```"
    # )
    # print("가이드 요약 전송 완료.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
except NameError as e:
    # results 변수 중 하나라도 정의되지 않았을 경우
    print(f"코드 오류: 필요한 결과 변수가 정의되지 않았습니다. ({e})")
except Exception as e:
    print(f"예상치 못한 오류가 발생했습니다: {e}")
