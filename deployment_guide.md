# IP Formatter Chatbot 배포 가이드

## 1. GitHub에 업로드 (Private도 OK! 👌)

**Q. Private(비공개)로 올려도 되나요?**
네, 상관없습니다! Streamlit Cloud는 Private 저장소도 연결할 수 있습니다. 개인적인 도구라면 Private을 추천합니다.

### 업로드 순서

1.  **GitHub 저장소 생성**
    *   GitHub에 로그인하고 [새 저장소 만들기](https://github.com/new) 페이지로 이동합니다.
    *   Repository name을 `ip_formatter_bot` 등으로 입력합니다.
    *   **Private**을 선택하고 "Create repository"를 클릭합니다.

2.  **프로젝트 업로드 (터미널 명령어)**
    *   VS Code 터미널을 열고 다음 명령어를 **한 줄씩** 입력하세요.
    *   (이미 `C:\Users\User\Documents\ip address` 폴더에 있다고 가정합니다)

    ```powershell
    # 1. 깃 초기화
    git init
    
    # 2. 모든 파일 담기 (.gitignore 덕분에 비밀키는 안 담깁니다)
    git add .
    
    # 3. 설명 적어서 포장하기
    git commit -m "IP 봇 초기 버전"
    
    # 4. 가지 이름 정리
    git branch -M main
    
    # 5. 내 깃허브 주소와 연결 (아래 주소를 본인 저장소 주소로 꼭 바꾸세요!)
    git remote add origin https://github.com/사용자아이디/저장소이름.git
    
    # 6. 밀어넣기
    git push -u origin main
    ```

---

## 2. Streamlit Cloud 배포

1.  **Streamlit Cloud 접속**
    *   [share.streamlit.io](https://share.streamlit.io/)에 접속하여 로그인합니다.
    *   "New app" 버튼을 클릭합니다.

2.  **앱 설정**
    *   "Use existing repo"를 선택합니다.
    *   **Repository**: 방금 올린 저장소 (`ip_formatter_bot`)를 선택합니다.
    *   **Branch**: `main`
    *   **Main file path**: `app.py`
    *   "Deploy!" 버튼을 클릭합니다.

---

## 3. 비밀키(API Key) 설정 (필수!)

**로컬에서 잘 되던 앱이 클라우드에서는 안 될 수 있습니다. API 키를 클라우드에도 알려줘야 해요.**

1.  배포된 앱 화면 오른쪽 하단의 **Manage app** 메뉴를 클릭합니다.
2.  오른쪽 상단의 점 3개 메뉴(`...`) -> **Settings** -> **Secrets** 탭으로 이동합니다.
3.  아래 내용을 복사해서 붙여넣고 저장하세요. (`ip address/.streamlit/secrets.toml` 파일 내용과 같습니다)

    ```toml
    GOOGLE_API_KEY = "여기에_당신의_구글_API_키를_넣으세요"
    ```

4.  이제 앱을 새로고침하면 끝! 고생하셨습니다! 🚀
