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

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
