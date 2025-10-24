import json
import bot.database_client
import bot.telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class DrinkSelection(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink = callback_data.replace("drink_", "").replace("_", " ").title()
        if drink == "None":
            drink = "No drinks"

        order_json["drink"] = drink

        bot.database_client.update_user_order_json(telegram_id, order_json)
        bot.database_client.update_user_state(
            telegram_id, "WAIT_FOR_ORDER_APPROVE")

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        order_summary = (
            f"Your order summary:\n"
            f"🍕 Pizza: {order_json.get('pizza_name', '-')}\n"
            f"📏 Size: {order_json.get('pizza_size', '-')}\n"
            f"🥤 Drink: {order_json.get('drink', '-')}"
        )

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
        )

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Do you confirm your order?",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Confirm", "callback_data": "approve_yes"},
                            {"text": "❌ Start Over",
                                "callback_data": "approve_restart"},
                        ]
                    ],
                }
            ),
        )
        return HandlerStatus.STOP
