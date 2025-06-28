# MCP 서버 개발 가이드

## MCP (Model Context Protocol) 소개

MCP는 LLM 애플리케이션이 외부 시스템과 통신하기 위한 표준화된 프로토콜입니다. AI 애플리케이션을 위한 USB-C 포트라고 생각하면 됩니다.

## 핵심 개념

### 1. Resources (리소스)
- GET 엔드포인트와 유사
- LLM 컨텍스트에 정보를 로드하는 데 사용
- 예: 파일 내용, 데이터베이스 레코드, API 응답

### 2. Tools (도구)
- POST 엔드포인트와 유사
- 코드 실행이나 부작용을 생성하는 데 사용
- 예: 파일 쓰기, API 호출, 시스템 명령 실행

### 3. Prompts (프롬프트)
- LLM 상호작용을 위한 재사용 가능한 템플릿
- 일관된 사용자 경험 제공

## 빠른 시작

### 1. 기본 MCP 서버 구현

```python
from mcp.server.fastmcp import FastMCP
from typing import Any

# MCP 서버 초기화
mcp = FastMCP("my-server")

# Resource 정의
@mcp.resource("config://settings")
async def get_settings() -> str:
    """현재 설정을 반환합니다."""
    return "Current settings: debug=true"

# Tool 정의
@mcp.tool()
async def calculate_sum(a: int, b: int) -> int:
    """두 숫자의 합을 계산합니다."""
    return a + b

# 서버 실행
if __name__ == "__main__":
    mcp.run()
```

### 2. 전송 방식

#### stdio (로컬 통신)
```python
# stdio 전송 사용 (기본값)
mcp.run(transport="stdio")
```

#### SSE (HTTP 통신)
```python
# HTTP/SSE 전송 사용
mcp.run(transport="sse", port=8080)
```

## 보안 모범 사례

### 1. 입력 검증
```python
@mcp.tool()
async def read_file(path: str) -> str:
    # 경로 검증
    safe_path = Path(path).resolve()
    if not safe_path.is_relative_to(ALLOWED_DIR):
        raise ValueError("접근이 허용되지 않은 경로입니다")

    return safe_path.read_text()
```

### 2. 인증 및 권한
```python
# HTTP 전송 시 인증 구현
@mcp.middleware
async def authenticate(request):
    token = request.headers.get("Authorization")
    if not validate_token(token):
        raise Unauthorized("유효하지 않은 토큰")
```

### 3. 속도 제한
```python
from functools import lru_cache
import time

@mcp.tool()
@rate_limit(calls=10, period=60)  # 분당 10회 제한
async def expensive_operation():
    # 리소스 집약적인 작업
    pass
```

## 고급 패턴

### 1. 비동기 처리
```python
import asyncio

@mcp.tool()
async def batch_process(items: list[str]) -> list[str]:
    """여러 항목을 동시에 처리합니다."""
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)
```

### 2. 에러 처리
```python
from mcp.errors import ToolError

@mcp.tool()
async def risky_operation(data: str) -> str:
    try:
        result = await external_api_call(data)
        return result
    except ExternalAPIError as e:
        raise ToolError(f"외부 API 오류: {e}")
```

### 3. 세션 관리
```python
from typing import Dict
import uuid

sessions: Dict[str, Any] = {}

@mcp.tool()
async def create_session() -> str:
    """새 세션을 생성합니다."""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"created_at": time.time()}
    return session_id
```

## 테스트

### 단위 테스트
```python
import pytest
from mcp.testing import MCPTestClient

@pytest.mark.asyncio
async def test_calculate_sum():
    async with MCPTestClient(mcp) as client:
        result = await client.call_tool("calculate_sum", {"a": 5, "b": 3})
        assert result == 8
```

### 통합 테스트
```python
@pytest.mark.asyncio
async def test_full_workflow():
    async with MCPTestClient(mcp) as client:
        # 리소스 확인
        settings = await client.get_resource("config://settings")
        assert "debug=true" in settings

        # 도구 사용
        result = await client.call_tool("process_data", {"input": "test"})
        assert result["status"] == "success"
```

## 배포 고려사항

### 1. 환경 변수
```python
import os
from dotenv import load_dotenv

load_dotenv()

MCP_PORT = int(os.getenv("MCP_PORT", 8080))
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
```

### 2. 로깅
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
async def monitored_operation(data: str) -> str:
    logger.info(f"작업 시작: {data[:20]}...")
    result = await process(data)
    logger.info(f"작업 완료: {len(result)} bytes")
    return result
```

### 3. 헬스체크
```python
@mcp.resource("health://status")
async def health_check() -> dict:
    """서버 상태를 확인합니다."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": __version__
    }
```

## 커뮤니티 리소스

- [MCP 공식 문서](https://modelcontextprotocol.io)
- [Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [MCP 서버 예제](https://github.com/modelcontextprotocol/servers)

## 다음 단계

1. 간단한 MCP 서버 구현으로 시작
2. 보안 및 에러 처리 추가
3. 테스트 작성
4. 프로덕션 배포 준비

이 가이드는 MCP 서버 개발의 기초를 다룹니다. 실제 구현 시에는 프로젝트의 특정 요구사항에 맞게 조정하세요.
