import pytest
from app.services.auth import create_access_token, decode_access_token


@pytest.mark.asyncio
async def test_decode_access_token_valid():
    data = {"sub": "123"}
    token = create_access_token(data=data)

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "123"


@pytest.mark.asyncio
async def test_decode_access_token_invalid():

    bad_token = "not.a.valid.jwt"

    payload = decode_access_token(bad_token)

    assert payload is None
