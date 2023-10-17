from jwt import encode,decode

def create_token(data: dict):
    token: str=encode(payload=data, key="My_secret_key",algorithm="HS256")
    return token


def validate_token(token:str)->dict:
    data:dict=decode(token,key="My_secret_key",algorithms=['HS256'])
    return data