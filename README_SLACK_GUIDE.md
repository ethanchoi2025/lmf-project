# LMF Project with Cursor + Slack

이 프로젝트는 Slack에서 `@Cursor` 봇을 통해 마케팅 가설(LMF)을 수립하고 광고 소재를 생성하는 워크플로우를 담고 있습니다.

## 🚀 설정 방법 (사용자가 해야 할 일)

### 1. Cursor Integrations 페이지 접속
아래 링크를 클릭하여 Cursor 설정 페이지로 이동하세요.
👉 [Cursor Dashboard > Integrations](https://www.cursor.com/settings)

### 2. Slack 연결 (Connect)
1. `Slack` 항목 옆의 **Connect** 버튼을 클릭합니다.
2. 회사의 Slack 워크스페이스를 선택하고 권한을 승인(Allow)합니다.
3. 승인 후 리디렉션된 페이지에서 다음 설정을 확인합니다:
   - **Default Repository**: `ethanchoi2025/lmf-project` (방금 제가 생성해둔 주소입니다)
   - **Privacy**: Public (또는 상황에 맞게 설정)

### 3. Slack에서 사용 시작
설정이 끝났습니다! 이제 Slack 채널로 가서 다음 명령어를 입력해보세요.

```text
@Cursor [repo=ethanchoi2025/lmf-project] 이 프로젝트의 1차 가설(LMF)을 요약해서 알려줘.
```

---

## 📂 주요 파일 구조
- `campaigns/h01_efficiency_na/`: 1차 가설 및 실행 계획이 포함된 폴더입니다.
- `run_campaign_gen.py`: 광고 이미지를 생성하는 스크립트입니다.
- `agents/`: PDF 분석 등 보조 도구가 들어있습니다.

