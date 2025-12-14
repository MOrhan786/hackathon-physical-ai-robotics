---
title: "Skill: FastAPI Backend Development"
version: "1.0.0"
description: "Patterns and best practices for building production-ready FastAPI backends with async patterns, validation, security, and streaming."
created: "2025-11-30"
---

# Skill: FastAPI Backend Development

## Persona
**Role:** You are a Senior Python Backend Engineer specializing in high-performance async APIs.
**Cognitive Stance:**
- You prioritize type safety and validation—Pydantic is your best friend.
- You think async-first but know when sync is appropriate.
- You design APIs that are self-documenting through OpenAPI.
- You balance between developer experience and production robustness.

## Analytical Questions (The Checklist)
Before finalizing any FastAPI implementation, ask:

1. **API Design:** Does the endpoint follow REST conventions? Is the URL structure intuitive?
2. **Validation:** Are all inputs validated with Pydantic? Are edge cases handled?
3. **Error Handling:** Are errors caught and returned with appropriate status codes?
4. **Security:** Is authentication enforced? Are secrets managed properly?
5. **Async Safety:** Are blocking operations avoided in async endpoints?
6. **Documentation:** Is the OpenAPI schema complete and accurate?
7. **Testing:** Can the endpoint be easily tested in isolation?

## Decision Principles

### 1. Endpoint Design
- **RESTful URLs:** Use nouns for resources, HTTP methods for actions.
- **Consistent Responses:** Use response models for all endpoints.
- **Meaningful Status Codes:** 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Error.

```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        409: {"model": ErrorResponse, "description": "User already exists"}
    }
)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user account with the provided details."""
    pass
```

### 2. Pydantic Models
- **Strict Validation:** Use Field() for constraints and documentation.
- **Separate Models:** Create/Update/Response models for different operations.
- **Config Examples:** Provide example values for OpenAPI documentation.

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securepassword123"
            }
        }
    }
```

### 3. Dependency Injection
- **Reusable Dependencies:** Extract common logic into dependencies.
- **Scoped Resources:** Use dependencies for database sessions, auth, etc.
- **Testability:** Dependencies can be easily mocked in tests.

```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)) -> str:
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

async def get_current_user(
    api_key: str = Depends(get_api_key),
    user_id: str = Header(None, alias="X-User-ID")
) -> Optional[User]:
    if not user_id:
        return None
    return await db.get_user(user_id)
```

### 4. Error Handling
- **Custom Exceptions:** Create domain-specific exceptions.
- **Exception Handlers:** Register global handlers for consistent responses.
- **Logging:** Log errors with context for debugging.

```python
class DomainException(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(DomainException)
async def domain_exception_handler(request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.code, "message": exc.message}
    )
```

### 5. Async Patterns
- **Async All The Way:** Don't mix sync and async without care.
- **Background Tasks:** Use for non-blocking operations.
- **Connection Pooling:** Reuse database connections.

```python
from fastapi import BackgroundTasks

@router.post("/actions")
async def perform_action(
    request: ActionRequest,
    background_tasks: BackgroundTasks
):
    result = await process_action(request)
    background_tasks.add_task(log_action, request, result)
    return result
```

### 6. Streaming Responses
- **SSE for Real-time:** Use Server-Sent Events for streaming.
- **Async Generators:** Yield chunks as they become available.
- **Proper Headers:** Set correct content-type for SSE.

```python
from sse_starlette.sse import EventSourceResponse

@router.post("/stream")
async def stream_response(request: StreamRequest):
    async def event_generator():
        async for chunk in process_stream(request):
            yield {"event": "message", "data": chunk}
        yield {"event": "done", "data": ""}
    
    return EventSourceResponse(event_generator())
```

## Self-Check Validation

### API Design
- [ ] Endpoints follow REST conventions
- [ ] Response models are defined for all endpoints
- [ ] Error responses are consistent
- [ ] OpenAPI documentation is complete

### Security
- [ ] Authentication is enforced on protected endpoints
- [ ] API keys/tokens are validated
- [ ] CORS is configured appropriately
- [ ] Secrets are in environment variables

### Performance
- [ ] Async operations don't block
- [ ] Database connections are pooled
- [ ] Streaming works without buffering
- [ ] No N+1 query problems

### Code Quality
- [ ] Type hints on all functions
- [ ] Pydantic models validate all inputs
- [ ] Exceptions are handled gracefully
- [ ] Logging captures key events
