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
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60, certificate=open('YOURPUBLIC.pem', 'r'))
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
    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.pending_images = {}

    def handle_message(self, msg):
        try:
            logger.info(f'Incoming message: {msg}')

            choices_msg = ('- Blur\n'
                           '- Contour\n'
                           '- Rotate\n'
                           '- Salt and pepper\n'
                           '- Segment\n'
                           '- Concat [horizontal/vertical]')
            usage_msg = ('Welcome to the Image Processing Bot!\n'
                         'Please send a photo along with a caption specifying the filter you want to apply.\n'
                         'Supported filters:\n'
                         f'{choices_msg}')

            if "text" in msg and msg["text"].strip().lower() == '/start':
                self.send_text(msg['chat']['id'],
                               'Hello! I am your Image Processing Bot. How can I assist you today?')
                self.send_text(msg['chat']['id'], usage_msg)
                return

            is_photo = self.is_current_msg_photo(msg)

            if is_photo:
                self.send_text(msg['chat']['id'], 'Processing the image...')
                photo_path = self.download_user_photo(msg)
                caption = msg.get('caption', '').lower()

                if caption.startswith('concat'):
                    if msg['chat']['id'] not in self.pending_images:
                        self.pending_images[msg['chat']['id']] = {'first_image': photo_path}
                        self.send_text(msg['chat']['id'], 'Please send the second image for concatenation.')
                    else:
                        self.pending_images[msg['chat']['id']]['second_image'] = photo_path
                        concat_direction = 'horizontal' if 'horizontal' in caption else 'vertical'
                        processed_path = self.process_image(self.pending_images[msg['chat']['id']]['first_image'],
                                                            caption, concat_direction,
                                                            self.pending_images[msg['chat']['id']]['second_image'])
                        self.send_photo(msg['chat']['id'], processed_path)
                        del self.pending_images[msg['chat']['id']]
                else:
                    processed_path = self.process_image(photo_path, caption)
                    self.send_photo(msg['chat']['id'], processed_path)
            else:
                self.send_text(msg['chat']['id'], "Please send a photo.")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_text(msg['chat']['id'], "Error: Please try again later.")

    def process_image(self, photo_path, caption, concat_direction=None, second_photo_path=None):
        img = Img(photo_path)

        if caption == 'blur':
            img.blur()
        elif caption == 'contour':
            img.contour()
        elif caption == 'rotate':
            img.rotate()
        elif caption == 'segment':
            img.segment()
        elif caption == 'salt and pepper':
            img.salt_n_pepper()
        elif caption.startswith('concat'):
            if second_photo_path:
                second_img = Img(second_photo_path)
                img.concat(second_img, direction=concat_direction)
            else:
                raise ValueError("Second image path is required for concatenation.")
        else:

            raise ValueError(
                f"Invalid caption: {caption}. Supported captions are: ['blur', 'contour', 'rotate', 'segment', "
                f"'salt and pepper', 'concat horizontal', 'concat vertical']"
            )

        processed_path = img.save_img()
        return processed_path
