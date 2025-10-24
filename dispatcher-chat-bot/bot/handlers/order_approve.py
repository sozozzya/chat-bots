import json
import bot.database_client
import bot.telegram_client
from bot.handlers.handler import Handler, HandlerStatus


class OrderApprove(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["approve_yes", "approve_restart"]

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])

        if callback_data == "approve_yes":
            bot.database_client.update_user_state(
                telegram_id, "ORDER_FINISHED")
            bot.telegram_client.deleteMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            )
            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="🎉 Thank you! Your order has been confirmed and is being prepared!",
                reply_markup=json.dumps({"remove_keyboard": True}),
            )
            return HandlerStatus.STOP

        if callback_data == "approve_restart":
            bot.database_client.clear_user_state_and_order(telegram_id)
            bot.database_client.update_user_state(
                telegram_id, "WAIT_FOR_PIZZA_NAME")

            bot.telegram_client.deleteMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            )
            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Let's start over! Please choose pizza name:",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {"text": "Margherita",
                                    "callback_data": "pizza_margherita"},
                                {"text": "Pepperoni",
                                    "callback_data": "pizza_pepperoni"},
                            ],
                            [
                                {"text": "Quatro Stagioni",
                                    "callback_data": "pizza_quatro_stagioni"},
                            ],
                            [
                                {"text": "Diavola", "callback_data": "pizza_diavola"},
                                {"text": "Prosciutto",
                                    "callback_data": "pizza_prosciutto"},
                            ],
                        ],
                    }
                ),
            )
            return HandlerStatus.STOP
