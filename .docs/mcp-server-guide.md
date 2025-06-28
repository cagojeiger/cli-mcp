# MCP 서버 개발 가이드

## MCP (Model Context Protocol) 개요

MCP는 AI 모델과 외부 도구/리소스 간의 표준화된 통신 프로토콜입니다. 이 가이드는 cli-mcp를 사용하여 MCP 서버를 개발하는 방법을 설명합니다.

## MCP 서버 기본 구조

### 필수 컴포넌트

1. **서버 클래스**: MCP 프로토콜 구현
2. **핸들러**: 요청 처리 로직
3. **도구(Tools)**: 실행 가능한 기능
4. **리소스(Resources)**: 제공할 데이터
5. **프롬프트(Prompts)**: 미리 정의된 프롬프트 템플릿

### 디렉토리 구조
```
src/cli_mcp/servers/my_server/
├── __init__.py
├── server.py           # 메인 서버 구현
├── config.py          # 설정 스키마
├── handlers/          # 요청 핸들러
│   ├── __init__.py
│   ├── tools.py      # 도구 핸들러
│   └── resources.py  # 리소스 핸들러
├── tools/            # 도구 구현
│   └── __init__.py
├── resources/        # 리소스 구현
│   └── __init__.py
└── README.md         # 서버 문서
```

## 서버 구현 예시

### 1. 기본 서버 클래스

```python
# server.py
from typing import Any, Dict
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

class MyMCPServer(Server):
    """커스텀 MCP 서버 구현."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("my-server")
        self.config = config
        self._setup_handlers()

    def _setup_handlers(self):
        """핸들러 등록."""
        # 도구 핸들러
        @self.list_tools()
        async def list_tools():
            return [
                {
                    "name": "example_tool",
                    "description": "예시 도구",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            ]

        @self.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]):
            if name == "example_tool":
                query = arguments.get("query", "")
                return {"result": f"Processed: {query}"}
            raise ValueError(f"Unknown tool: {name}")

async def main():
    """서버 실행."""
    server = MyMCPServer({})
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 도구 구현

```python
# tools/search.py
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class SearchTool:
    """검색 도구 구현."""

    name = "search"
    description = "웹 검색 도구"

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 쿼리"
                },
                "limit": {
                    "type": "integer",
                    "description": "결과 개수",
                    "default": 10
                }
            },
            "required": ["query"]
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """도구 실행."""
        query = arguments["query"]
        limit = arguments.get("limit", 10)

        # 실제 검색 로직 구현
        results = await self._perform_search(query, limit)

        return {
            "results": results,
            "count": len(results)
        }

    async def _perform_search(self, query: str, limit: int):
        # 검색 구현
        pass
```

### 3. 리소스 구현

```python
# resources/database.py
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class DatabaseResource:
    """데이터베이스 리소스."""

    uri = "db://example"
    name = "Example Database"
    description = "예시 데이터베이스 접근"

    async def read(self, path: str) -> Dict[str, Any]:
        """리소스 읽기."""
        # 데이터베이스 쿼리 로직
        return {
            "data": [],
            "metadata": {
                "path": path,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }

    async def list(self) -> List[str]:
        """사용 가능한 리소스 목록."""
        return [
            "tables/users",
            "tables/products",
            "views/summary"
        ]
```

## 설정 관리

### 설정 스키마 정의

```python
# config.py
from pydantic import BaseModel, Field
from typing import Optional

class ServerConfig(BaseModel):
    """서버 설정 스키마."""

    host: str = Field(default="localhost", description="서버 호스트")
    port: int = Field(default=8080, description="서버 포트")
    api_key: Optional[str] = Field(default=None, description="API 키")
    timeout: int = Field(default=30, description="요청 타임아웃(초)")

    class Config:
        env_prefix = "MY_SERVER_"  # 환경 변수 접두사
```

## 테스트 작성

### 서버 테스트

```python
# tests/test_my_server.py
import pytest
from cli_mcp.servers.my_server import MyMCPServer

@pytest.mark.asyncio
async def test_list_tools():
    """도구 목록 테스트."""
    server = MyMCPServer({})
    tools = await server.list_tools()

    assert len(tools) > 0
    assert tools[0]["name"] == "example_tool"

@pytest.mark.asyncio
async def test_call_tool():
    """도구 실행 테스트."""
    server = MyMCPServer({})
    result = await server.call_tool(
        "example_tool",
        {"query": "test"}
    )

    assert result["result"] == "Processed: test"
```

## 서버 등록

### CLI에 서버 추가

1. `src/cli_mcp/servers/__init__.py`에 서버 등록:

```python
from .my_server import MyMCPServer

AVAILABLE_SERVERS = {
    "my-server": {
        "class": MyMCPServer,
        "description": "나의 MCP 서버",
        "config_schema": ServerConfig
    }
}
```

2. CLI 명령어로 실행:

```bash
# 서버 시작
cli-mcp server start my-server

# 설정과 함께 시작
cli-mcp server start my-server --config config.json
```

## 배포 준비

### 1. 문서 작성
- README.md: 서버 사용법
- API 문서: 도구와 리소스 설명
- 예시 설정 파일

### 2. 패키징
```python
# pyproject.toml에 추가
[project.entry-points."cli_mcp.servers"]
my-server = "cli_mcp.servers.my_server:MyMCPServer"
```

### 3. 테스트 확인
```bash
# 단위 테스트
uv run pytest tests/servers/test_my_server.py

# 통합 테스트
uv run cli-mcp server test my-server
```

## 모범 사례

### 1. 오류 처리
```python
try:
    result = await dangerous_operation()
except SpecificError as e:
    return {"error": str(e), "code": "SPECIFIC_ERROR"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal server error", "code": "INTERNAL_ERROR"}
```

### 2. 비동기 프로그래밍
- `async/await` 일관되게 사용
- 블로킹 작업은 스레드풀 활용
- 동시성 제한 설정

### 3. 보안
- 입력 검증 필수
- 민감한 정보 로깅 금지
- API 키 안전하게 관리

### 4. 성능
- 연결 풀링 사용
- 결과 캐싱 고려
- 리소스 정리 확실히

## 디버깅 팁

### 로깅 설정
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 프로토콜 디버깅
```bash
# 상세 로그와 함께 실행
cli-mcp server start my-server --debug

# 프로토콜 메시지 추적
cli-mcp server start my-server --trace-protocol
```

## 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/anthropics/mcp-python)
- [예시 서버 구현](https://github.com/anthropics/mcp-servers)
