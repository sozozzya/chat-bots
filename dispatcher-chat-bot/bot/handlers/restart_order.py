import json
import bot.database_client
import bot.telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class RestartOrder(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"].lower() in ["/restart", "start over"]
        )

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        bot.database_client.clear_user_state_and_order(telegram_id)
        bot.database_client.update_user_state(
            telegram_id, "WAIT_FOR_PIZZA_NAME")

        bot.telegram_client.sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text="Order restarted! Please choose pizza name 🍕",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "🍅 Margherita",
                                "callback_data": "pizza_margherita"},
                            {"text": "🔥 Pepperoni",
                                "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {
                                "text": "🌿 Quatro Stagioni",
                                "callback_data": "pizza_quatro_stagioni"
                            },
                        ],
                        [
                            {"text": "🌶️ Diavola", "callback_data": "pizza_diavola"},
                            {"text": "🥓 Prosciutto",
                                "callback_data": "pizza_prosciutto"},
                        ],
                    ],
                }
            ),
        )
        return HandlerStatus.STOP
