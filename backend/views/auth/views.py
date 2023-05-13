import datetime
import logging
from os import getenv
from cryptography.hazmat.primitives import serialization
from backend.dtos import Login, LoginRequestModel, LoginResponseModel, BaseResponse
import jwt

from backend.models import Profile


def login(request):
    data = LoginRequestModel(
        username=request.POST.get("username", ""),
        password=request.POST.get("password", "")
    )
    profile = Profile.objects.select_related("user").get(user__username__exact=data.username)
    if data.password == profile.user.password:
        login_model = Login(
            id=profile.id,
            username=profile.user.username,
            email=profile.user.email,
            full_name=f"{profile.user.last_name} {profile.user.first_name}",
        )
        try:
            token = generate_token(login_model)
            return LoginResponseModel(
                token=token,
                full_name=login_model.full_name,
                message="Login Successful",
                status=True
            ).__dict__
        except Exception as ex:
            return BaseResponse(
                message=str(ex),
                status=False
            ).__dict__


def generate_token(payload: Login) -> str:
    try:
        exp = datetime.datetime.now() + datetime.timedelta(seconds=float(getenv("EXPIRY_TIME")))
        iss = getenv("ISS")
        aud = getenv("AUD")
        iat = datetime.datetime.now()
        algorithm = getenv("ALGORITHM")
        key = getenv("SECRET_KEY")
        data = payload.__dict__
        token = jwt.encode(payload={
            "data": data,
            "exp": exp,
            "iss": iss,
            "aud": aud,
            "iat": iat
        }, algorithm=algorithm, key=key)
        return f"Bearer {token}"
    except (OSError, Exception) as ex:
        logging.error(f"{ex} occurred while generating token")
        raise ex


def decode(token: str = None, request=None) -> Login:
    try:
        if not token:
            token = get_token(request)
        audience = getenv("AUD")
        secret = getenv("SECRET_KEY")
        algorithm = getenv("ALGORITHM")
        data = jwt.decode(token, key=secret, audience=audience, options={
            "require": ["exp", "iss", "aud", "iat"], "verify_signature": True
        }, algorithms=algorithm)
        user_info = data["data"]
        user = Login(
            id=user_info["id"],
            full_name=user_info["full_name"],
            email=user_info["email"],
            username=user_info["username"],
        )
        return user
    except OSError as error:
        print(error)
    except jwt.exceptions.DecodeError as ex:
        logging.error(f"{ex} occurred while generating token")
        raise ex


def get_payload(request) -> dict:
    token: str = get_token(request)
    data = jwt.decode(token, options={"verify_signature": False})
    return data["data"]


def get_token(request):
    token: str = request.headers.get("Authorization", "")
    if token != "":
        token = token.split(" ")[-1]
        return token
    return None


def __get_key(is_private: bool = True):
    if is_private:
        path = getenv("PATH_TO_PRI")
        key = open(path, "r").read()
        passphrase = getenv("PASSPHRASE")
        return serialization.load_ssh_private_key(key.encode(), password=passphrase.encode())
    else:
        path = getenv("PATH_TO_PUB")
        key = open(path, "r").read()
        return serialization.load_ssh_public_key(key.encode())
