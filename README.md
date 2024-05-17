# Image Processing Bot

## Overview

The Image Processing Bot is a Telegram bot designed to process images based on user-provided captions. Users can send photos with captions such as 'Blur', 'Rotate', 'Concat', etc., and the bot will apply the corresponding filter to the image and send it back. This README provides an overview of the setup, features, and usage instructions for the bot.

## Features

- **Greet Users**: Responds to messages with 'start', 'hello', or 'hi' with a greeting message.
- **Image Processing**: Supports several image processing functions, including:
  - Blur
  - Contour
  - Rotate
  - Segment
  - Salt and Pepper
  - Concat (concatenates two images)

## Installation

### Prerequisites

- Python 3.6+
- Telegram Bot Token (You can get this by talking to [BotFather](https://core.telegram.org/bots#botfather) on Telegram)
- Flask
- Loguru
- Matplotlib

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/image-processing-bot.git
    cd polybot
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set environment variables:**

    Set the following environment variables with your Telegram bot token and webhook URL.

    ```bash
    export TELEGRAM_TOKEN='your-telegram-bot-token'
    export TELEGRAM_APP_URL='your-app-url'
    ```

4. **Run the bot:**

    ```bash
    python app.py
    ```

## Usage

### Starting the Bot

Send a message with 'start', 'hello', or 'hi' to the bot to receive a greeting message.

### Sending a Photo

Send a photo with one of the following captions to apply the corresponding filter:

- 'Blur'
- 'Contour'
- 'Rotate'
- 'Segment'
- 'Salt and Pepper'
- 'Concat' (requires a second photo, specified in the message)

### Example

1. **Start the bot:**

    ```
    You: start
    Bot: Hi there! I'm your Image Processing Bot. Send me a photo with a caption like 'Blur', 'Rotate', 'Concat', etc., and I'll apply the filter for you!
    ```

2. **Send a photo with a caption:**

    ```
    You: (Send a photo with the caption 'Blur')
    Bot: (Sends back the blurred photo)
    ```

## Code Explanation

### `Bot` Class

- **`__init__`**: Initializes the bot, sets up the webhook.
- **`send_text`**: Sends a text message to a chat.
- **`send_text_with_quote`**: Sends a text message with a quoted message.
- **`is_current_msg_photo`**: Checks if the current message contains a photo.
- **`download_user_photo`**: Downloads the photo sent by the user.
- **`send_photo`**: Sends a photo to a chat.
- **`handle_message`**: Handles incoming messages.

### `QuoteBot` Class

Inherits from `Bot`, handles messages by quoting them.

### `ImageProcessingBot` Class

Inherits from `Bot`, processes images based on captions.

- **`process_image`**: Applies filters to the image based on the caption.

### `Img` Class

Handles image processing operations.

- **`blur`**: Applies a blur filter.
- **`contour`**: Applies a contour filter.
- **`rotate`**: Rotates the image.
- **`segment`**: Segments the image.
- **`salt_n_pepper`**: Applies a salt and pepper noise filter.
- **`concat`**: Concatenates two images.
