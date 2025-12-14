from typing import Dict
from .types import MessageTemplate

USER_MESSAGES: Dict[str, MessageTemplate] = {
    "USER_NOT_FOUND": {
        "id": "USER_NOT_FOUND",
        "messages": {
            "en": "User not found",
            "uz": "Foydalanuvchi topilmadi",
            "ru": "Пользователь не найден",
        },
        "status_code": 404
    },
    "AUTHENTICATION_FAILED": {
        "id": "AUTHENTICATION_FAILED",
        "messages": {
            "en": "Authentication failed",
            "uz": "Autentifikatsiya muvaffaqiyatsiz",
            "ru": "Аутентификация не удалась",
        },
        "status_code": 401
    },
    "INVALID_CREDENTIALS": {
        "id": "INVALID_CREDENTIALS",
        "messages": {
            "en": "Invalid credentials",
            "uz": "Noto'g'ri ma'lumotlar",
            "ru": "Неверные учетные данные",
        },
        "status_code": 401
    },
    "EMAIL_ALREADY_EXISTS": {
        "id": "EMAIL_ALREADY_EXISTS", 
        "messages": {
            "en": "Email already registered",
            "uz": "Email allaqachon ro'yxatdan o'tgan",
            "ru": "Email уже зарегистрирован",
        },
        "status_code": 400
    },
    "USERNAME_ALREADY_EXISTS": {
        "id": "USERNAME_ALREADY_EXISTS",
        "messages": {
            "en": "Username already taken",
            "uz": "Username allaqachon band",
            "ru": "Имя пользователя уже занято", 
        },
        "status_code": 400
    },
}