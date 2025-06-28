# 개발 가이드

## 개발 환경 설정

### 사전 요구사항
- Python 3.11 이상
- uv (빠른 Python 패키지 매니저)
- Git

### 프로젝트 설정

```bash
# 저장소 클론
git clone https://github.com/cagojeiger/cli-mcp.git
cd cli-mcp

# uv 설치 (아직 없다면)
pip install uv

# 의존성 설치
uv sync --all-extras --dev

# pre-commit hooks 설치
uv run pre-commit install
```

## 코드 스타일

### Python 스타일 가이드
- **Black**: 코드 포맷팅 (line-length: 100)
- **isort**: import 정렬
- **Ruff**: 린팅 및 코드 품질 검사

### 코딩 규칙
1. **함수형 프로그래밍** 선호
   - 순수 함수 사용
   - 부작용 최소화
   - 고차 함수 활용

2. **타입 힌트** 필수
   ```python
   def process_data(data: list[str]) -> dict[str, int]:
       ...
   ```

3. **Docstring** 스타일: Google Python Style Guide
   ```python
   def example_function(param1: str, param2: int) -> bool:
       """간단한 설명.

       Args:
           param1: 첫 번째 매개변수 설명
           param2: 두 번째 매개변수 설명

       Returns:
           반환값 설명
       """
   ```

## 테스트

### 테스트 실행
```bash
# 모든 테스트 실행
uv run pytest

# 커버리지와 함께 실행
uv run pytest --cov

# 특정 테스트만 실행
uv run pytest tests/test_cli.py

# 느린 테스트 제외
uv run pytest -m "not slow"
```

### 테스트 작성 가이드
1. **AAA 패턴** 사용 (Arrange, Act, Assert)
2. **테스트 격리**: 각 테스트는 독립적으로 실행 가능
3. **의미 있는 테스트 이름**: `test_<what>_<condition>_<expected>`

예시:
```python
def test_version_option_displays_version(runner):
    """--version 옵션이 버전을 표시하는지 확인."""
    # Arrange
    from cli_mcp.cli import app

    # Act
    result = runner.invoke(app, ["--version"])

    # Assert
    assert result.exit_code == 0
    assert "cli-mcp version:" in result.stdout
```

## 브랜치 전략

### 브랜치 명명 규칙
- `feat/`: 새로운 기능
- `fix/`: 버그 수정
- `docs/`: 문서 변경
- `refactor/`: 코드 리팩토링
- `test/`: 테스트 추가/수정
- `chore/`: 빌드, 설정 등

### 워크플로우
1. `main`에서 새 브랜치 생성
2. 변경사항 구현
3. 테스트 작성 및 통과 확인
4. PR 생성
5. 코드 리뷰
6. `main`으로 병합

## 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 사양 준수:

```
<type>(<scope>): <subject>

<body>

<footer>
```

예시:
```
feat(cli): add server list command

- Implement server discovery functionality
- Add --format option for output formatting
- Include basic filtering capabilities

Closes #123
```

## 코드 품질 도구

### Pre-commit 실행
```bash
# 모든 파일에 대해 실행
uv run pre-commit run --all-files

# 특정 훅만 실행
uv run pre-commit run black --all-files
```

### 수동 검사
```bash
# Black 포맷팅
uv run black src tests

# isort 정렬
uv run isort src tests

# Ruff 린팅
uv run ruff check src tests --fix
```

## MCP 서버 개발

### 새 MCP 서버 추가
1. `src/cli_mcp/servers/` 아래에 새 디렉토리 생성
2. 기본 서버 인터페이스 구현
3. 설정 스키마 정의
4. 테스트 작성
5. 문서 업데이트

### 서버 구조 예시
```
src/cli_mcp/servers/my_server/
├── __init__.py
├── server.py       # 메인 서버 구현
├── config.py       # 설정 스키마
├── handlers.py     # 요청 핸들러
└── README.md       # 서버 문서
```

## 디버깅

### 로깅 활용
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("디버그 메시지")
```

### 디버거 사용
```bash
# pytest with pdb
uv run pytest --pdb

# 코드에 중단점 설정
import pdb; pdb.set_trace()
```

## 릴리스 프로세스

1. 모든 테스트 통과 확인
2. CHANGELOG.md 업데이트
3. `main` 브랜치로 병합
4. semantic-release가 자동으로:
   - 버전 결정
   - 태그 생성
   - 패키지 빌드
   - PyPI 배포

## 문제 해결

### 일반적인 문제
1. **의존성 충돌**: `uv sync --refresh` 실행
2. **테스트 실패**: 환경 변수 및 Python 버전 확인
3. **pre-commit 오류**: `uv run pre-commit autoupdate` 실행

### 도움 받기
- GitHub Issues에서 문제 검색/보고
- 개발 가이드라인 준수
- 재현 가능한 최소 예제 제공
