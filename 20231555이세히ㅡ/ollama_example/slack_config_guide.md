# Slack 메시지 전송 설정 가이드

mission.py에서 Slack으로 결과를 전송하는 방법을 안내합니다.

## 📝 설정 방법

### 1️⃣ mission.py 상단 설정 변경

```python
# ============================================================================
# Slack 설정 (메시지 전송용)
# ============================================================================
SLACK_ENABLED = True  # Slack 전송 활성화
SLACK_CHANNEL = "C01234567"  # 실제 채널 ID로 변경
```

### 2️⃣ 채널 ID 찾기

#### 방법 A: 채널 이름으로 찾기
```python
# mission.py 실행 전에 채널 ID를 먼저 확인하세요
import sys
sys.path.append('.')  # 현재 디렉토리를 경로에 추가

# 채널 찾기 (예시)
# result = mcp_mcp_hub_slack_cafe24.find_channel_by_name("ai-mission-results")
# print(result)
# channel_id = result['channel']['id']  # 이 ID를 SLACK_CHANNEL에 입력
```

#### 방법 B: Slack 웹에서 직접 확인
1. Slack 웹 브라우저로 접속
2. 원하는 채널 클릭
3. URL 확인: `https://app.slack.com/client/T.../C01234567`
4. `C01234567` 부분이 채널 ID

### 3️⃣ mission.py의 주석 해제

`send_slack_summary` 함수에서 주석을 해제하세요:

```python
def send_slack_summary(mission_name, summary_data):
    """미션 완료 후 요약 정보를 Slack으로 전송"""
    if not SLACK_ENABLED:
        print(f"ℹ️ Slack 전송 비활성화됨: {mission_name}")
        return
    
    try:
        blocks = [...]
        
        # 이 부분의 주석을 해제하세요 ↓
        # mcp_mcp_hub_slack_cafe24.post_block_message(
        #     channel_id=SLACK_CHANNEL,
        #     blocks=blocks,
        #     text=mission_name,
        #     auto_join=True
        # )
        
    except Exception as e:
        print(f"⚠️ Slack 전송 실패: {e}")
```

## 📊 Slack 메시지 형식

각 미션 완료 시 다음과 같은 형식으로 전송됩니다:

### 미션 1: 영화 리뷰 분석
```
🎉 미션 1: 영화 리뷰 분석 완료!

📊 총 영화 수        4편
⭐ 평균 평점        4.05/5.0
👍 추천 영화        3편 (75.0%)
🎬 고평점 영화       3편
💾 생성 파일        • movie_reviews.json
                  • recommended_movies.json

━━━━━━━━━━━━━━━━━━━━━━━━
Mission.py에서 자동 생성된 보고서
```

### 미션 2: 코드 리뷰 자동화
```
🎉 미션 2: 코드 리뷰 자동화 완료!

👥 평가 대상        4명
📊 평균 점수        14.3/20
🏆 등급 분포        A: 2명
                  B: 1명
                  C: 1명
🌟 우수 학생        학생 D, 학생 B
💾 생성 파일        • code_evaluations.json
                  • code_evaluation_summary.json

━━━━━━━━━━━━━━━━━━━━━━━━
Mission.py에서 자동 생성된 보고서
```

### 미션 3: CoT 답변 검증
```
🎉 미션 3: CoT 답변 검증 완료!

🔢 총 문제 수       7개
✅ 정답 개수        6개 (85.7%)
📊 평균 점수        8.3/10
🎯 추론 품질        Excellent: 3개
                  Good: 4개
💾 생성 파일        • cot_verification.json
                  • cot_verification_summary.json

━━━━━━━━━━━━━━━━━━━━━━━━
Mission.py에서 자동 생성된 보고서
```

## 🔧 테스트 방법

### 1. 시뮬레이션 모드로 실행 (현재 상태)
```bash
python mission.py
```

출력 예시:
```
📨 [Slack 전송 시뮬레이션]
   채널: ai-mission-results
   제목: 미션 1: 영화 리뷰 분석
   필드 수: 5
   ✅ 실제 전송하려면 위 주석을 해제하세요
```

### 2. 실제 Slack 전송
1. 위의 설정 방법대로 SLACK_CHANNEL 설정
2. send_slack_summary 함수의 주석 해제
3. mission.py 실행

## 🚫 Slack 전송 비활성화

Slack 전송을 원하지 않는 경우:

```python
SLACK_ENABLED = False  # 이렇게 설정하면 전송하지 않음
```

## 💡 팁

1. **채널 권한**: 봇이 채널에 접근 권한이 있어야 합니다
2. **auto_join=True**: 봇이 자동으로 채널에 참여합니다
3. **Block Kit**: 더 복잡한 메시지는 [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)에서 디자인 가능

## 🐛 문제 해결

### 에러: "channel_not_found"
- 채널 ID가 올바른지 확인
- 봇이 해당 채널에 초대되었는지 확인

### 에러: "not_authed"
- Slack 토큰이 올바르게 설정되었는지 확인
- MCP 설정이 올바른지 확인

### 전송되지 않음
- SLACK_ENABLED가 True인지 확인
- 주석 해제를 제대로 했는지 확인
- 콘솔 출력에서 에러 메시지 확인

## 📚 참고 자료

- [Slack Block Kit](https://api.slack.com/block-kit)
- [Slack API 문서](https://api.slack.com/)

