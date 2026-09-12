import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_public_route_no_token():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.get("/public/info")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_protected_route_without_token():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.get("/protected/profile")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.get(
            "/protected/profile",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "SecurePass123!"},
        )
        # 201 if new, 400 if already exists
        assert response.status_code in (201, 400)


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as client:
        response = await client.post("/auth/logout")
        assert response.status_code == 204
