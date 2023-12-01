import json
import os
import re

class CensorBot:
    version = "0.3.0_PER4"
    print("Simple Censor Bot | Made by @bhop0 team | ver.", version, "\nGithub: https://github.com/bhop0 \n")

    def __init__(self, word_list_file="badwords.txt", substitution_file="bypass.json", config_file="config.txt"):
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.external_bad_words = self.load_bad_words(os.path.join(script_dir, word_list_file))
        self.substitution_dict = self.load_substitution_dict(os.path.join(script_dir, substitution_file))
        self.load_config(os.path.join(script_dir, config_file))
        self.strict_mode = self.config.get('strict_mode', False)
        self.strict_bad_words = self.load_bad_words(os.path.join(script_dir, 'strict.txt')) if self.strict_mode else []

    def load_bad_words(self, word_list_file):
        try:
            with open(word_list_file, "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: Bad words file '{word_list_file}' not found.")
            return []

    def load_substitution_dict(self, substitution_file):
        try:
            with open(substitution_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Substitution file '{substitution_file}' not found.")
            return {}

    def load_config(self, config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config_lines = [line.strip() for line in file.readlines()]
                self.config = {key: bool(int(value)) for key, value in (line.split(':') for line in config_lines)}
        except FileNotFoundError:
            print(f"Error: Config file '{config_file}' not found.")
            self.config = {}

    def apply_substitutions(self, text):
        for original, substitutions in self.substitution_dict.items():
            for substitution in substitutions:
                text = text.replace(substitution, original)
        return text

    def detector(self, text):
        text_with_substitutions = self.apply_substitutions(text)
        words = re.findall(r'\b\w+\b', text_with_substitutions)

        detected_words = []

        for i in range(len(words)):
            word = words[i]
            word_lower = word.lower()

            # Combine single letters separated by spaces
            while i + 1 < len(words) and len(word) == 1 and word.isalpha() and len(words[i + 1]) == 1 and words[i + 1].isalpha():
                word += words[i + 1]
                i += 1

            if word_lower in self.external_bad_words and self.config.get('enable_detection', True):
                detected_words.append(word_lower)

            if self.strict_mode and word_lower in self.strict_bad_words:
                detected_words.append(word_lower)

        return detected_words

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
