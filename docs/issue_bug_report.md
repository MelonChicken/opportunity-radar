# 이슈: UI/UX 버그 리포트 (복사 버튼, 칩 스타일, 패딩)

## 1. Copy 버튼 작동 불량

**증상:**
프롬프트 상세 섹션의 "Copy" 버튼을 클릭해도 클립보드에 텍스트가 복사되지 않습니다. 버튼 애니메이션은 작동하지만, 실제 클립보드 내용에는 변화가 없습니다.

**위치:** `src/ui/components.py` (자바스크립트 주입 부분)

**기술적 분석:**
- 현재 구현은 `navigator.clipboard.writeText`를 사용하고 있는 것으로 추정됩니다.
- **원인:** `navigator.clipboard` API는 **보안 컨텍스트(HTTPS 또는 localhost)**에서만 사용할 수 있습니다. 만약 애플리케이션이 HTTP(원격 IP)로 호스팅되고 있거나, Streamlit iframe 샌드박스 정책에 의해 차단된 경우 이 API는 실패합니다.
- 대안으로 사용된 `document.execCommand('copy')` 방식 또한 Streamlit iframe 내의 포커스 문제로 인해 실패하고 있을 가능성이 큽니다.

**제안된 해결책:**
- iframe 포커스를 명확히 처리하는 강력한 대체 수단(fallback)을 구현해야 합니다.
- 실패 원인을 파악하기 위한 콘솔 로그를 추가해야 합니다.
- Streamlit 컴포넌트를 사용하거나, Shadow DOM 또는 활성 프레임 내에서 `document.body.appendChild`를 사용하여 임시 `textarea`를 생성하고, 포커스 및 선택 후 복사를 실행하는 보다 신뢰할 수 있는 순수 JS 솔루션을 고려해야 합니다.

---

## 2. Try Option 칩 스타일 (검은 배경에 검은 글씨)

**증상:**
"Popular Searches" (Try Option) 칩이 검은 배경(또는 매우 어두운 회색)에 검은 글씨로 표시되어 가독성이 매우 떨어집니다.

**위치:** `src/ui/styles/chips.py` 및 `src/ui/layout.py`

**기술적 분석:**
- `chips.py`의 CSS는 명시적인 색상(`color: #2563EB`, `background: #EFF6FF`)을 설정하고 있지만, 이 스타일이 덮어씌워지고 있습니다.
- **원인:**
    - **다크 모드 강제:** Streamlit의 네이티브 다크 모드가 더 높은 명시도(specificity)를 가진 스타일이나 변수를 주입하여, `!important` 규칙과 충돌하거나 선택자가 정확히 일치하지 않아 발생할 수 있습니다.
    - **DOM 구조 변경:** Streamlit v1.40+ 업데이트로 `st.pills`의 DOM 구조가 변경되었을 수 있습니다. `div[data-testid="stPills"] button` 선택자가 더 이상 텍스트 색상을 보유한 실제 요소를 가리키지 않을 수 있습니다 (중첩된 div나 span으로 변경 등).
    - **충돌:** 검증된 CSS에 `!important`가 있음에도 적용되지 않는다면, 선택자 불일치가 가장 유력한 원인입니다.

**제안된 해결책:**
- 브라우저 개발자 도구로 `st.pills`의 정확한 클래스명이나 data-testid를 확인해야 합니다.
- `src/ui/styles/chips.py`를 업데이트하여 텍스트 색상을 실제로 담당하는 내부 `div`나 `span`을 타겟팅해야 합니다.
- `load_chips_css()`가 테마 주입 *이후*에 호출되도록 보장해야 합니다.

---

## 3. 프롬프트 컨테이너 패딩 문제

**증상:**
사용자 프롬프트 코드 블록 내부의 패딩이 불충분하여 텍스트가 경계선에 너무 붙어 보입니다. CSS 수정이 적용되지 않는 것으로 보입니다.

**위치:** `src/ui/styles/dialogs.py`

**기술적 분석:**
- **상태:** 패딩을 `24px+`로 늘리는 수정을 시도했으나, 사용자로부터 "적용되지 않는다"는 피드백을 받았습니다.
- **원인:**
    - **CSS 주입 타이밍:** `st.dialog`는 React Portal을 생성합니다. 메인 앱(`layout.py`)에서 주입된 스타일은 보통 전체 페이지에 영향을 주지만, 때때로 Streamlit 자체의 모달 스타일과 명시도 경쟁이 발생할 수 있습니다.
    - **캐싱:** Streamlit은 `st.markdown` 문자열을 캐싱합니다. 문자열 내용이 충분히 변경되지 않았거나, 브라우저가 CSS 클래스 정의를 캐싱하고 있다면 렌더링에 반영되지 않을 수 있습니다.
    - **선택자 명시도:** Streamlit의 마크다운 렌더러가 pre/code 블록을 기본 패딩/마진 재정의가 포함된 다른 컨테이너로 감싸는 경우, `.prompt-text` 선택자가 너무 일반적일 수 있습니다.

**제안된 해결책:**
- 명시도 높이기: `div[data-testid="stDialog"] .prompt-text` (이미 수행했으나 재확인 필요).
- 컨테이너 div뿐만 아니라 `pre`와 `code` 태그에 직접 `padding: ... !important`를 추가합니다.
- `components.py`의 HTML 구조가 CSS 선택자와 정확히 일치하는지 확인합니다.
