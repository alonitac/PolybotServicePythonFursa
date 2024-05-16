import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from polybot.img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        self.prev_path = ""

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text,timeout=5)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id, timeout= 5)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path),
            timeout=5
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ImageProcessingBot(Bot):

    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        try:
            if self.is_current_msg_photo(msg):
                self.handle_message_photo(msg)
            else:
                self.handle_message_text(msg)
        except Exception as e:
            print("error accord", e)
            self.send_text_with_quote(msg['chat']['id'], "error please try agin", quoted_msg_id=msg["message_id"])

    def handle_message_text(self,msg):
        option_list = [
            'hi', 'hello', 'whats up',
            'how are you', 'help'
        ]
        text = msg["text"].lower()
        index = option_list.index(text)
        if 0 <= index <= 4:
            self.send_text(msg['chat']['id'], "Hi How can I help you")
        else:
            self.send_text_with_quote(msg['chat']['id'], "error please try agin",
                                      quoted_msg_id=msg["message_id"])

    def handle_message_photo(self, msg):
        option_list = [
            'blur', 'contour', 'rotate',
            'salt and pepper', 'concat', 'segment'
        ]
        if self.is_current_msg_photo(msg):
            path = self.download_user_photo(msg)
            image = Img(path)
            if self.prev_path == "":
                caption = msg["caption"].lower()
            else:
                caption = "concat"
            index = option_list.index(caption)
            # option to choose
            match index:
                case 0:
                    image.blur()
                case 1:
                    image.contour()
                case 2:
                    image.rotate()
                case 3:
                    image.salt_n_pepper()
                case 4:
                    if self.prev_path == "":
                        self.prev_path = path
                        return
                    else:
                        image_2 = Img(self.prev_path)
                        self.prev_path = ""
                        image.concat(image_2)
                case 5:
                    image.segment()
                case _:
                    raise Exception("Sorry, option are invalid")
            new_path = image.save_img()
            self.send_photo(msg['chat']['id'], new_path)
        else:
            self.send_text_with_quote(msg['chat']['id'], "msg are not photo please try agin",
                                      quoted_msg_id=msg["message_id"])
