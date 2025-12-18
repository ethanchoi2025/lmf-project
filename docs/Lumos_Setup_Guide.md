# Lumos (Slack x Cursor) 연동 가이드

Cursor의 AI를 통해 슬랙을 직접 제어하기 위한 설정 가이드입니다.

## 1. 슬랙 봇 토큰 발급 (Bot User OAuth Token)

1. **Slack API 접속**: [https://api.slack.com/apps](https://api.slack.com/apps) 로 이동합니다.
2. **새 앱 생성**:
   - `Create New App` 클릭 -> `From scratch` 선택.
   - **App Name**: `Lumos` (또는 원하는 이름)
   - **Workspace**: 봇을 사용할 워크스페이스 선택.
3. **권한(Scopes) 설정**:
   - 좌측 메뉴 **OAuth & Permissions** 클릭.
   - 스크롤을 내려 **Scopes** > **Bot Token Scopes** 섹션에서 `Add an OAuth Scope`를 클릭하여 아래 권한들을 추가합니다:
     - `channels:history` (채널 메시지 읽기)
     - `channels:read` (채널 목록 보기)
     - `chat:write` (메시지 보내기)
     - `files:write` (파일 업로드)
     - `users:read` (사용자 정보 보기)
4. **워크스페이스 설치**:
   - 같은 페이지 상단으로 올라가 **Install to Workspace** 버튼 클릭 -> `Allow` 클릭.
5. **토큰 복사**:
   - **Bot User OAuth Token** (`xoxb-`로 시작하는 값)을 복사하여 안전한 곳에 두세요.

---

## 2. Cursor에 MCP 서버 추가

Cursor가 슬랙을 제어할 수 있도록 MCP 서버를 등록합니다.

1. **Cursor 설정 열기**:
   - `Cmd + ,` (Mac) 또는 `Ctrl + ,` (Windows)를 눌러 설정 창을 엽니다.
   - **Features** > **MCP Servers** 메뉴로 이동합니다.

2. **새 서버 추가**:
   - `+ Add New MCP Server` 버튼을 클릭합니다.
   - 다음 정보를 입력합니다:
     - **Name**: `Slack`
     - **Type**: `command`
     - **Command**:
       ```bash
       npx -y @modelcontextprotocol/server-slack
       ```
     - **Environment Variables** (환경 변수 섹션 클릭 후 추가):
       - Key: `SLACK_BOT_TOKEN`
       - Value: `xoxb-....` (아까 복사한 토큰을 붙여넣으세요)

3. **저장 및 확인**:
   - 저장 후 초록색 불(Connected)이 들어오는지 확인합니다.

---

## 3. 사용 방법 (Cursor Chat)

이제 Cursor 채팅창(Cmd + L)에서 다음과 같이 명령할 수 있습니다.

- "@Slack #marketing 채널에 최근 올라온 메시지 요약해줘"
- "@Slack #general 채널에 'Lumos 봇이 연결되었습니다'라고 인사해줘"
- "@Slack 방금 만든 이미지 파일(ad_test.png)을 #design 채널에 업로드해줘"

