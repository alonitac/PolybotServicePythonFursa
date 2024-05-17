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
        try:
            logger.info(f'Incoming message: {msg}')

            choices_msg = ('- Blur\n'
                           '- Contour\n'
                           '- Rotate [number of rotations]\n'
                           '- Salt and pepper\n'
                           '- Segment\n'
                           '- Concat')
            usage_msg = ('Welcome to the Image Processing Bot!\n'
                         'Please send a photo along with a caption specifying the filter you want to apply.\n'
                         'Supported filters:\n'
                         f'{choices_msg}')

            # Check if the message is the /start command
            if "text" in msg and msg["text"].strip().lower() == '/start':
                self.send_text(msg['chat']['id'],
                               'Hello! I am your Image Processing Bot. How can I assist you today?')
                self.send_text(msg['chat']['id'], usage_msg)
                return

            is_photo = self.is_current_msg_photo(msg)

            if is_photo:
                self.send_text(msg['chat']['id'], 'processing the image...')
                # Download the photo sent by the user
                photo_path = self.download_user_photo(msg)
                caption = msg.get('caption', '').lower()

                # Process the photo according to the caption
                processed_path = self.process_image(photo_path, caption, msg)
                # Send the processed image back to the user
                self.send_photo(msg['chat']['id'], processed_path)
            else:
                # Inform user to send a photo.
                self.send_text(msg['chat']['id'], "Please send a photo.")
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_text(msg['chat']['id'], "Error: Please try again later.")

    class ImageProcessingBot(Bot):
        def handle_message(self, msg):
            try:
                logger.info(f'Incoming message: {msg}')
                options_msg = ('- Blur\n'
                               '- Contour\n'
                               '- Rotate [number of rotations]\n'
                               '- Salt and pepper\n'
                               '- Segment\n'
                               '- Concat')
                usage_msg = ('Welcome to the Image Processing Bot!\n'
                             'Please send a photo along with a caption specifying the filter you want to apply.\n'
                             'Supported filters:\n'
                             f'{options_msg}')

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
                    processed_path = self.process_image(photo_path, caption, msg)
                    self.send_photo(msg['chat']['id'], processed_path)
                else:
                    self.send_text(msg['chat']['id'], "Please send a photo.")
            except Exception as e:
                logger.error(f"Error: {e}")
                self.send_text(msg['chat']['id'], "Error: Please try again later.")

        def process_image(self, photo_path, caption, msg):
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
            elif caption == 'concat':
                second_photo_path = msg.get('second_photo_path')
                if second_photo_path:
                    second_img = Img(second_photo_path)
                    img.concat(second_img)
                else:
                    raise ValueError("For 'Concat' caption, information about the second image is required.")
            else:
                raise ValueError(
                    f"Invalid caption: {caption}. Supported captions are: ['blur', 'contour', 'rotate', 'segment', "
                    f"'salt and pepper', 'concat']"
                )
            processed_path = img.save_img()
            return processed_path


