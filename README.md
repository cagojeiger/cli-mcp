# cli-mcp

MCP (Model Context Protocol) 서버 관리를 위한 현대적인 Python CLI 도구

## 빠른 시작

### 설치

#### pipx 사용 (권장)

```bash
# pipx가 없다면 먼저 설치
pip install pipx
pipx ensurepath

# cli-mcp 설치
pipx install cli-mcp
```

#### 소스에서 설치

```bash
# 소스 코드 클론
git clone https://github.com/cagojeiger/cli-mcp.git
cd cli-mcp

# 개발 모드로 설치
pipx install -e . --force
```

### 기본 사용법

```bash
# 버전 확인
cli-mcp --version

# 도움말
cli-mcp --help
```

## 개발

### 의존성 설치

```bash
# uv 설치 (아직 없다면)
pip install uv

# 개발 의존성 포함 설치
uv sync --all-extras --dev
```

### 테스트 실행

```bash
# 전체 테스트 실행
uv run pytest

# 커버리지와 함께 실행
uv run pytest --cov
```

### 코드 품질

```bash
# Pre-commit hooks 설치
uv run pre-commit install

# 모든 파일에 대해 pre-commit 실행
uv run pre-commit run --all-files
```

## 프로젝트 구조

```
cli-mcp/
├── src/cli_mcp/         # 메인 소스 코드
│   ├── cli.py          # CLI 진입점
│   └── servers/        # MCP 서버들
├── tests/              # 테스트 코드
├── config/             # 설정 파일들
└── .github/workflows/  # CI/CD 워크플로우
```

## 라이선스

MIT License - [LICENSE](LICENSE) 파일 참조
