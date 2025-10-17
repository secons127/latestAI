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


def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


student_answer = ask('gemma3:4b', "RAG의 정의를 한 문장으로 설명해줘.", temperature=0)

rubric = """
채점 기준:
1) 정의의 정확성(0~4)
2) 간결성(0~3)
3) 핵심 용어 사용(0~3)
총점=10, JSON으로만 출력: {"score": <0-10>, "feedback": "<한줄 피드백>"}
학생 답변:
""" + student_answer

grade = ollama.chat(
    model='gemma3:4b',  
    messages=[{"role": "user", "content": rubric}],
    format='json',
    options={"temperature": 0}
)

# 학생 답변과 채점 결과 출력
print("학생 답변:", student_answer)
print("\n채점 결과:")
grading_result = json.loads(grade['message']['content'])
print(json.dumps(grading_result, indent=2, ensure_ascii=False))

# Slack 메시지 전송
try:
    response = client.chat_postMessage(
        channel=channel_name,
        text=grade['message']['content']  # grade에서 받은 채점 결과를 전송
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
