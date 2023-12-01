# SimpleCensorBot

Simple Censor Bot is an open-source bad words detector written in Python. It is designed to identify and filter out offensive language from text. This project is not just a library but a standalone application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bhop0/SimpleCensorBot.git
   cd SimpleCensorBot
   ```

2. Ensure you have Python installed. The project is compatible with Python 3.x.

3. Import this file into you project:

   ```bash
   python CensorBotV1.py
   ```

## Usage

The `CensorBot` class can be utilized in your Python projects for detecting and handling offensive language. The example demonstrates a simple interactive use case where the user can input text, and the bot detects and outputs any detected bad words.

```python
from SimpleCensorBot.CensorBotV1 import CensorBot

if __name__ == "__main__":
    bot = CensorBot()

    while True:
        text = input("Enter a text (type 'exit' to end the program): ")

        if text.lower() == 'exit':
            print("Exiting the program.")
            break

        detected_words = bot.detector(text)
        if detected_words:
            print("Detected bad words:", detected_words)
        else:
            print("No bad words detected.")
```

Feel free to integrate the `CensorBot` class into your projects for content moderation or use it as a starting point for building more advanced text filtering systems.

## Contributing

Contributions are welcome! If you find issues or have suggestions for improvements, please create an issue or submit a pull request. Follow the [contribution guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Showcases

![image](https://github.com/bhop0/SimpleCensorBot/assets/146635994/cc3a6aae-11b4-4565-ab1e-bfa1b4cc98ec)

![image](https://github.com/bhop0/SimpleCensorBot/assets/146635994/f5bcf551-0829-4b27-8784-4321afc4a057)
