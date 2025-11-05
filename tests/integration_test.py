import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import get_db
from tests.init_test_db import init_test_db
from app.schemas.userschema import UserCreate, UserLogin


@pytest_asyncio.fixture
async def client():
    engine, SessionLocal = await init_test_db()

    async def get_test_db():
        async with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await engine.dispose()


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"message": "OK, API is up and running"}


async def test_register(client):
    new_user = UserCreate(
        email="test@example.com", name="Test User", password="password123"
    )
    result = await client.post("/api/auth/register", json=new_user.model_dump())

    return result


@pytest.mark.asyncio
async def test_login(client):
    await test_register(client)

    login_data = UserLogin(email="test@example.com", password="password123")
    res_login = await client.post("/api/auth/login", params=login_data.model_dump())

    assert res_login.status_code == 200
    data_login = res_login.json()
    assert data_login.get("email") == "test@example.com"
    assert data_login.get("name") == "Test User"


@pytest.mark.asyncio
async def test_register_same_user_again(client):
    await test_register(client)

    same_user_reg_again = UserCreate(
        email="test@example.com", name="Test User", password="password123"
    )
    result = await client.post(
        "/api/auth/register", json=same_user_reg_again.model_dump()
    )

    assert result.status_code == 400
    data = result.json()
    assert data["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_register_and_login_with_bad_pw(client):
    await test_register(client)

    login_data = UserLogin(email="test@example.com", password="password345")
    res_login = await client.post("/api/auth/login", params=login_data.model_dump())
    data = res_login.json()

    assert res_login.status_code == 401
    assert data["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_register_and_login_with_bad_email(client):
    await test_register(client)

    login_data = UserLogin(email="badtest@example.com", password="password123")
    res_login = await client.post("/api/auth/login", params=login_data.model_dump())
    data = res_login.json()

    assert res_login.status_code == 401
    assert data["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_register_and_get_token(client):
    await test_register(client)

    res_token = await client.post(
        "/api/auth/token",
        data={"username": "test@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response_data = res_token.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"
    token = response_data["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_register_and_try_to_get_token_with_bad_email(client):
    await test_register(client)

    res_token = await client.post(
        "/api/auth/token",
        data={"username": "badtest@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    data = res_token.json()
    assert res_token.status_code == 401
    assert data["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_me_endpoint(client):
    await test_register(client)

    res_token = await client.post(
        "/api/auth/token",
        data={"username": "test@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res_token.status_code == 200
    token = res_token.json()["access_token"]

    result = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert result.status_code == 200
    response_data = result.json()
    assert response_data["user_email"] == "test@example.com"
    assert response_data["user_name"] == "Test User"


@pytest.mark.asyncio
async def test_failed_me_endpoint(client):
    await test_register(client)

    res_token = await client.post(
        "/api/auth/token",
        data={"username": "test@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res_token.status_code == 200
    bad_token = "This is bad token"

    result = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {bad_token}"}
    )

    assert result.status_code == 401
