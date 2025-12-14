from typing import Dict
from .types import MessageTemplate

MOVIE_MESSAGES: Dict[str, MessageTemplate] = {
    "MOVIE_NOT_FOUND": {
        "id": "MOVIE_NOT_FOUND",
        "messages": {
            "en": "Movie not found",
            "uz": "Kino topilmadi",
            "ru": "Фильм не найден",
        },
        "status_code": 404
    },
    "PREMIUM_REQUIRED": {
        "id": "PREMIUM_REQUIRED",
        "messages": {
            "en": "Premium subscription required to watch this movie",
            "uz": "Bu kinoni ko'rish uchun premium obuna talab qilinadi",
            "ru": "Для просмотра этого фильма требуется премиум подписка",
        },
        "status_code": 403
    },
    "GENRE_NOT_FOUND": {
        "id": "GENRE_NOT_FOUND",
        "messages": {
            "en": "Genre not found",
            "uz": "Janr topilmadi",
            "ru": "Жанр не найден",
        },
        "status_code": 404
    },
    "ALREADY_RATED": {
        "id": "ALREADY_RATED",
        "messages": {
            "en": "You have already rated this movie",
            "uz": "Siz bu kinoni allaqachon baholagansiz",
            "ru": "Вы уже оценили этот фильм",
        },
        "status_code": 400
    },
    "INVALID_RATING": {
        "id": "INVALID_RATING",
        "messages": {
            "en": "Rating must be between 1 and 10",
            "uz": "Reyting 1 dan 10 gacha bo'lishi kerak",
            "ru": "Оценка должна быть от 1 до 10",
        },
        "status_code": 400
    },
    "COMMENT_NOT_FOUND": {
        "id": "COMMENT_NOT_FOUND",
        "messages": {
            "en": "Comment not found",
            "uz": "Kommentariya topilmadi",
            "ru": "Комментарий не найден",
        },
        "status_code": 404
    },
}