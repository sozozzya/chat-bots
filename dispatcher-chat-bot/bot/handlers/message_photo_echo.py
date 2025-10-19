from bot.handler import Handler
import bot.telegram_client


class MessagePhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]

    def handle(self, update: dict) -> bool:
        photos = update["message"]["photo"]
        largest_photo = max(photos, key=lambda p: p["file_size"])
        bot.telegram_client.makeRequest(
            "sendPhoto",
            chat_id=update["message"]["chat"]["id"],
            photo=largest_photo["file_id"],
        )
        return False
