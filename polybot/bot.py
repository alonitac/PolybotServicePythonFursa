import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/',certificate=open('/home/ubuntu/PolybotServicePythonFursa/polybot/YOURPUBLIC.pem', 'r'), timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

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
            InputFile(img_path)
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
        name = msg['chat']['first_name']
        options = ("Please send a photo, with a caption of the filter you want to apply on it.\n"
                   "- Salt and pepper: Adds random noise the image.\n"
                   "- Blur: Applies a blurring effect to the image.\n"
                   "- Contour: Detects edges of objects in the image.\n"
                   "- Rotate: Rotates the image in clockwise.\n"
                   "- Segment: Divides the image into regions based on similarities.\n"
                   "- Concat: Combines two images either horizontally or vertically.\n"
                   "- Rotate num: Rotates the image in clockwise num times. \n"
                   " - Done: to quit"
                   )
        try:

            chat_id = msg['chat']['id']
            if "text" in msg and msg["text"].lower() == '/start':
                self.send_text(chat_id, f"Hello {name}, Welcome to Ameer images bot.\n")
                self.send_text(chat_id, options)
            elif 'text' in msg and msg['text'].lower() == 'done':
                self.send_text(chat_id, "Good bye, we well be happy to see you again")
            else:
                is_image = self.is_current_msg_photo(msg)
                if is_image:
                    img = Img(self.download_user_photo(msg))
                    filter_option = msg['caption'].strip().split(' ')
                    if len(filter_option) == 1:
                        self.send_text(chat_id, f'{filter_option[0]}...')
                        if filter_option[0].lower() == "blur":
                            img.blur()
                        elif filter_option[0].lower() == "rotate":
                            img.rotate()
                        elif filter_option[0].lower() == "contour":
                            img.contour()
                        elif filter_option[0].lower() == 'segment':
                            img.segment()
                        elif filter_option[0].lower() == 'concat':
                            img2_path = self.download_user_photo(msg)
                            img2 = Img(img2_path)
                            img.concat(img2)
                        else:
                            self.send_text(chat_id, "Invalid filter")
                            return

                    elif len(filter_option) > 1:
                        if filter_option[0].lower() == "salt":
                            self.send_text(chat_id, f'{filter_option[0]} {filter_option[1]} ...')
                            img.salt_n_pepper()
                        elif filter_option[0].lower() == "rotate":
                            self.send_text(chat_id, f'{filter_option[0]} image {filter_option[1]} times..')
                            try:
                                num = int(filter_option[1].strip())
                                for i in range(num):
                                    img.rotate()
                            except:
                                self.send_text(chat_id, "Invalid filter")
                                return
                        else:
                            self.send_text(chat_id, "Invalid filter")
                            return

                    else:
                        self.send_text(chat_id, "invalid filter")
                        return
                    new_path = img.save_img()
                    self.send_photo(chat_id, new_path)
                else:
                    self.send_text(chat_id, options)

        except Exception as e:
            logger.error(f'Error: {e}')
            self.send_text(msg['chat']['id'], 'Something went Wrong, Try Again...\n')
