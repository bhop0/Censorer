# SimpleCensorBot

**Version:** 0.1.0

Simple Censor Bot is an open-source bad words detector written in Python. It is designed to identify and filter out offensive language from text. This project is not just a library but a standalone application.

## Table of Contents
- [Introduction](#simple-censor-bot)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **External Bad Words List:** Utilizes an external bad words list from a specified file (`badwords.txt` by default).
- **Substitution Handling:** Can detect words even when substituted with characters, leveraging a substitution dictionary from a JSON file (`bypass.json` by default).
- **Hardcoded Bad Words:** Includes a hardcoded list of bad words for enhanced detection accuracy.
- **User-friendly Output:** Provides a clear indication of detected bad words in the input text.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bhop0/simple-censor-bot.git
   cd simple-censor-bot
   ```

2. Ensure you have Python installed. The project is compatible with Python 3.x.

3. Run the example script:

   ```bash
   python censor_bot.py
   ```

## Usage

The `CensorBot` class can be utilized in your Python projects for detecting and handling offensive language. The example script demonstrates a simple interactive use case where the user can input text, and the bot detects and outputs any detected bad words.

```python
if __name__ == "__main__":
    SimpleCensorBot = CensorBot()

    while True:
        text = input("Enter a text (type 'exit' to end the program): ")

        if text.lower() == 'exit':
            print("Exiting the program.")
            break

        detected_words = SimpleCensorBot.detector(text)
        if detected_words:
            print("Detected bad words:", detected_words, "\n")
        else:
            print("No bad words detected.\n")
```

Feel free to integrate the `CensorBot` class into your projects for content moderation or use it as a starting point for building more advanced text filtering systems.

## Contributing

Contributions are welcome! If you find issues or have suggestions for improvements, please create an issue or submit a pull request. Follow the [contribution guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
