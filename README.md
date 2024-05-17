# PolybotServicePython

## Overview

PolybotServicePython is a Python-based service designed to process images via a Telegram bot. Users can send images to the bot, which then applies various filters and returns the processed images.

Here is a short demonstration:

![app demo](.github/python_project_demo.gif)

## Features

- **Image Filters**: Apply filters such as Blur, Contour, Rotate, Segment, Salt and Pepper, and Concat.
- **Telegram Bot Integration**: Interact with the service via a Telegram bot.
- **Flexible and Extensible**: Easily add new filters and extend bot functionality.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mohmmad-amer/PolybotServicePythonFursa.git
   cd PolybotServicePythonFursa
   ```
2. **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
   ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt 
   ```
## Usage
### Running the Bot
1. **Create a Telegram Bot**    
- <a href="https://desktop.telegram.org/" target="_blank">Download</a> and install Telegram Desktop (you can use your phone app as well).
- Once installed, create your own Telegram Bot by following <a href="https://core.telegram.org/bots/features#botfather">this section</a> to create a bot. Once you have your telegram token you can move to the next step.

2. **Set Up Environment Variables**:
    1. `TELEGRAM_TOKEN` Your Telegram bot token.
    2. `TELEGRAM_APP_URL` The public URL for your bot (use Ngrok for local development).
```bash
export TELEGRAM_TOKEN='your-telegram-token'
export TELEGRAM_APP_URL='your-ngrok-url'
```
3. **Run the Bot**:

```bash
python polybot/app.py
```
### Applying Filters
- Blur: Blurs the image.
- Contour: Adds a contour effect to the image.
- Rotate: Rotates the image.
- Segment: Segments the image into regions.
- Salt and Pepper: Adds noise to the image.
- Concat: Concatenates two images side by side.

## Test your filters locally

Under `polybot/test` you'll find unittests for each filter.

For example, to execute the test suite for the `concat()` filter, run the below command from the root dir of your repo:

```bash
python -m polybot.test.test_concat
```

## Extending Functionality
You can extend the bot by adding new filters or enhancing existing ones. Implement additional methods in the Img class and update the ImageProcessingBot class to support these new filters.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### Contact
For any questions or suggestions, feel free to open an issue.
