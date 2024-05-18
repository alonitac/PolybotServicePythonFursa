# Image Processing Telegram Bot

This Telegram bot allows users to process images with various filters and transformations.

## Getting Started

### Prerequisites

- Python 3.x
- [Flask](https://pypi.org/project/Flask/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)
- [loguru](https://pypi.org/project/loguru/)

### Installation

1. Clone this repository:

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```
### Create a Telegram Bot

1. <a href="https://desktop.telegram.org/" target="_blank">Download</a> and install Telegram Desktop (you can use your phone app as well).
2. Once installed, create your own Telegram Bot by following <a href="https://core.telegram.org/bots/features#botfather">this section</a> to create a bot. Once you have your telegram token you can move to the next step.

**Never** commit your telegram token in Git repo, even if the repo is private.
For now, we will provide the token as an environment variable to your chat app. 
Later on in the course we will learn better approaches to store sensitive data.

### Running the Telegram bot locally

The Telegram app is a flask-based service that responsible for providing a chat-based interface for users to interact with your image processing functionality. 
It utilizes the Telegram Bot API to receive user images and respond with processed images. 

The code skeleton for the bot app is already given to you under `polybot/app.py`.
In order to run the server, you have to [provide 2 environment variables](https://www.jetbrains.com/help/objc/add-environment-variables-and-program-arguments.html#add-environment-variables):

1. `TELEGRAM_TOKEN` which is your bot token.
2. `TELEGRAM_APP_URL` which is your app public URL provided by Ngrok (will be discussed soon).

Implementing bot logic involves running a local Python script that listens for updates from Telegram servers.
When a user sends a message to the bot, Telegram servers forward the message to the Python app using a method called **webhook** (**long-polling** and **websocket** are other possible methods which wouldn't be used in this project).
The Python app processes the message, executes the desired logic, and may send a response back to Telegram servers, which then delivers the response to the user.

The webhook method consists of simple two steps:

Setting your chat app URL in Telegram Servers:

Once the webhook URL is set, Telegram servers start sending HTTPS POST requests to the specified webhook URL whenever there are updates, such as new messages or events, for the bot. 

You've probably noticed that setting `localhost` URL as the webhook for a Telegram bot can be problematic because Telegram servers need to access the webhook URL over the internet to send updates.
As `localhost` is not accessible externally, Telegram servers won't be able to reach the webhook, and the bot won't receive any updates.

[Ngrok](https://ngrok.com/) can solve this problem by creating a secure tunnel between the local machine (where the bot is running) and a public URL provided by Ngrok.
It exposes the local server to the internet, allowing Telegram servers to reach the webhook URL and send updates to the bot.

Sign-up for the Ngrok service (or any another tunneling service to your choice), then install the `ngrok` agent as [described here](https://ngrok.com/docs/getting-started/#step-2-install-the-ngrok-agent). 

Authenticate your ngrok agent. You only have to do this once:

```bash
ngrok config add-authtoken <your-authtoken>
```

Since the telegram bot service will be listening on port `8443`, start ngrok by running the following command:

```bash
ngrok http 8443
```

Your bot public URL is the URL specified in the `Forwarding` line (e.g. `https://16ae-2a06-c701-4501-3a00-ecce-30e9-3e61-3069.ngrok-free.app`).
Don't forget to set the `TELEGRAM_APP_URL` env var to your URL. 

In the next step you'll finally run your bot app.

### Usage

1. Set up environment variables:
    - `TELEGRAM_TOKEN`: Your Telegram bot token.
    - `TELEGRAM_APP_URL`: Your application URL.

2. Run the Flask app:

    ```sh
    python app.py
    ```

   3. Start chatting with your Telegram bot! Send an image along with a caption specifying the filter or transformation you want to apply.

       **Examples:**
       - Applying /start command:

           ![Screenshot from 2024-05-18 10-42-58](https://github.com/abd129-0/PolybotServicePythonFursa/assets/75143506/f962be9b-a4e0-4bef-9d10-e6b26e21b613)

    
       - Applying the blur filter:
    
           ![Screenshot from 2024-05-18 10-44-55](https://github.com/abd129-0/PolybotServicePythonFursa/assets/75143506/9a371d3b-bda0-4b81-88d0-4b34fd7e1a8c)

        
       - Applying the segment filter:
    
           ![segment](https://github.com/abd129-0/PolybotServicePythonFursa/assets/75143506/3d2d5926-fd97-4692-8e3c-1477cde065e7)

         

        

    <!-- Add more examples as needed -->

## File Structure

- `app.py`: Flask application handling Telegram webhook and routing.
- `img_proc.py`: Image processing utilities including filters and transformations.
- `bot.py`: Base class and subclasses for different types of Telegram bots.

## Supported Filters/Transformations

- Blur
- Contour
- Rotate
- Salt and Pepper
- Segment
- Concatenation (horizontal/vertical)
