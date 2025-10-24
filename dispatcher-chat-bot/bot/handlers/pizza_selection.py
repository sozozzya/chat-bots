import json
import bot.database_client
import bot.telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class PizzaSelection(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace(
            "pizza_", "").replace("_", "").title()

        bot.database_client.update_user_order_json(
            telegram_id, {"pizza_name": pizza_name})

        bot.database_client.update_user_state(
            telegram_id, "WAIT_FOR_PIZZA_SIZE")

        bot.telegram_client.answerCallbackQuery(
            update["callback_query"]["id"])

        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=f"Great choice! 🍕 \nYou selected {pizza_name}.\nNow choose your pizza size 📏",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "🍕 Small (25cm)",
                                "callback_data": "size_small"},
                            {"text": "🍕➡️ Medium (30cm)",
                             "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "🍕🍕 Large (35cm)",
                             "callback_data": "size_large"},
                            {"text": "🍕🍕👑 Extra Large (40cm)",
                             "callback_data": "size_extra_large"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
