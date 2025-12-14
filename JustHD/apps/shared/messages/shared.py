from typing import Dict
from .types import MessageTemplate

SHARED_MESSAGES: Dict[str, MessageTemplate] = {
    "SUCCESS_MESSAGE": {
        "id": "SUCCESS_MESSAGE",
        "messages": {
            "en": "Operation completed successfully",
            "uz": "Operatsiya muvaffaqiyatli yakunlandi",
            "ru": "Операция успешно завершена",
        },
        "status_code": 200
    },
    "CREATED": {
        "id": "CREATED",
        "messages": {
            "en": "Resource created successfully",
            "uz": "Resurs muvaffaqiyatli yaratildi",
            "ru": "Ресурс успешно создан",
        },
        "status_code": 201
    },
    "UPDATED": {
        "id": "UPDATED",
        "messages": {
            "en": "Resource updated successfully",
            "uz": "Resurs muvaffaqiyatli yangilandi",
            "ru": "Ресурс успешно обновлен",
        },
        "status_code": 200
    },
    "DELETED": {
        "id": "DELETED",
        "messages": {
            "en": "Resource deleted successfully",
            "uz": "Resurs muvaffaqiyatli o'chirildi",
            "ru": "Ресурс успешно удален",
        },
        "status_code": 200
    },
    "VALIDATION_ERROR": {
        "id": "VALIDATION_ERROR",
        "messages": {
            "en": "Invalid input data",
            "uz": "Noto'g'ri ma'lumot kiritildi",
            "ru": "Неверные входные данные",
        },
        "status_code": 400
    },
    "NOT_FOUND": {
        "id": "NOT_FOUND",
        "messages": {
            "en": "Resource not found",
            "uz": "Resurs topilmadi",
            "ru": "Ресурс не найден",
        },
        "status_code": 404
    },
    "PERMISSION_DENIED": {
        "id": "PERMISSION_DENIED",
        "messages": {
            "en": "You don't have permission to perform this action",
            "uz": "Sizda bu amalni bajarish uchun ruxsat yo'q",
            "ru": "У вас нет прав для выполнения этого действия",
        },
        "status_code": 403
    },
    "UNAUTHORIZED": {
        "id": "UNAUTHORIZED",
        "messages": {
            "en": "Authentication required",
            "uz": "Autentifikatsiya talab qilinadi",
            "ru": "Требуется аутентификация",
        },
        "status_code": 401
    },
    "INTERNAL_SERVER_ERROR": {
        "id": "INTERNAL_SERVER_ERROR",
        "messages": {
            "en": "Internal server error occurred",
            "uz": "Ichki server xatosi yuz berdi",
            "ru": "Произошла внутренняя ошибка сервера",
        },
        "status_code": 500
    },
}