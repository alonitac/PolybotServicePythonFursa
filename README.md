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
    
       - Applying the blur filter:
    
           ![Blur Example](/path/to/blur_example.png)
        
       - Applying the contour filter:
   
         ![Segment Example](/home/abdallah/Pictures/Screenshots/segment.png)

        

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
