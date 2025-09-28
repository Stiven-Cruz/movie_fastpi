import jwt

def create_token(data: dict):
    token: str = jwt.encode(payload=data, key="mi_secret", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = jwt.decode(jwt=token, key="mi_secret", algorithms=["HS256"])
    return data