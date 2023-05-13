from django.contrib.auth.models import User
from backend.models import Profile
from backend.dtos import Profile as ProfileDto
from typing import Tuple
from password_validator import PasswordValidator


def register(request):
    data = __get_data_from_request(request)
    if not any(getattr(data, field) is None for field in data.__annotations__):
        return {
            "status": False,
            "message": "Ensure you fill all the fields"
        }
    if not __validate_password(data.password, data.confirm_password):
        return {
            "status": False,
            "message": "Password Validation Error"
        }
    result, message = __create_profile(data)
    if not result:
        return {
            "status": False,
            "message": message
        }
    return {
        "status": True,
        "message": "User Created"
    }


def __get_data_from_request(request) -> ProfileDto:
    return ProfileDto(
        first_name=request.POST.get("first_name", None),
        last_name=request.POST.get("last_name", None),
        email=request.POST.get("email", None),
        phone_number=request.POST.get("phone_number", None),
        address=request.POST.get("address", None),
        username=request.POST.get("email", None),
        occupation=request.POST.get("occupation", None),
        password=request.POST.get("password", None),
        confirm_password=request.POST.get("confirm_password", None)
    )


def __create_profile(data: ProfileDto) -> Tuple[bool, str]:
    try:
        # create user
        user = User()
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.email = data.email
        user.username = data.username
        user.password = data.password
        user.objects.create()

        # set up profile
        profile = Profile()
        profile.user = user
        profile.address = data.address
        profile.occupation = data.occupation
        profile.phone_number = data.phone_number
        return True, ""
    except Exception as e:
        return False, str(e)


def __validate_password(password: str, confirm_password: str) -> bool:
    if password != confirm_password:
        return False
    # Create a schema
    schema = PasswordValidator()
    # Add properties to it
    schema \
        .min(8) \
        .max(100) \
        .has().digits() \
        .letters() \
        .has().no().spaces()
    return schema.validate(password)
