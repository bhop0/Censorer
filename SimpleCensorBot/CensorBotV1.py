import json
import os
import re

class CensorBot:
    version = "1.0.0.0_PRE1"
    print("Simple Censor Bot | Made by @bhop0 team | ver.", version, "\nGithub: https://github.com/bhop0 \n")

    def __init__(self, word_list_file="badwords.txt", substitution_file="bypass.json", config_file="config.txt",
                 prc_word_list_file="prc_badwords.txt", prc_strict_file="prc_strict.txt"):
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.external_bad_words = self.load_bad_words(os.path.join(script_dir, "eng_detect", word_list_file))
        self.substitution_dict = self.load_substitution_dict(os.path.join(script_dir, "eng_detect", substitution_file))
        self.load_config(os.path.join(script_dir, config_file))
        self.strict_mode = self.config.get('strict_mode', False)
        self.strict_bad_words = self.load_bad_words(os.path.join(script_dir, "eng_detect", 'strict.txt')) if self.strict_mode else []
        self.prc_external_bad_words = self.load_prc_bad_words(os.path.join(script_dir, "chs_detect", prc_word_list_file))
        self.prc_strict_bad_words = self.load_prc_bad_words(os.path.join(script_dir, "chs_detect", prc_strict_file))

    def load_bad_words(self, word_list_file):
        try:
            with open(word_list_file, "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: File '{word_list_file}' not found.")
            return []

    def load_prc_bad_words(self, prc_word_list_file):
        try:
            with open(prc_word_list_file, "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: File '{prc_word_list_file}' not found.")
            return []

    def load_substitution_dict(self, substitution_file):
        try:
            with open(substitution_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{substitution_file}' not found.")
            return {}

    def load_config(self, config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config_lines = [line.strip() for line in file.readlines()]

                # Split the lines at "#####SPLITLINE#####"
                split_index = config_lines.index("#####SPLITLINE#####")
                general_config_lines = config_lines[:split_index]
                chs_config_lines = config_lines[split_index + 1:]

                # Load general configuration
                self.config = {key: bool(int(value)) for key, value in (line.split(':') for line in general_config_lines)}

                # Load Chinese (chs) configuration (for future use)
                self.chs_config = {key: bool(int(value)) for key, value in (line.split(':') for line in chs_config_lines)}

        except FileNotFoundError:
            print(f"Error: Config file '{config_file}' not found.")
            self.config = {}
            self.chs_config = {}

    def apply_substitutions(self, text):
        for original, substitutions in self.substitution_dict.items():
            for substitution in substitutions:
                text = text.replace(substitution, original)
        return text

    def eng_detector(self, text):
        text_with_substitutions = self.apply_substitutions(text)
        words = re.findall(r'\b\w+\b', text_with_substitutions)

        detected_words = []

        for i in range(len(words)):
            word = words[i]
            word_lower = word.lower()

            if word_lower in self.external_bad_words and self.config.get('enable_detection', True):
                detected_words.append(word_lower)

            if self.strict_mode and word_lower in self.strict_bad_words:
                detected_words.append(word_lower)

        return detected_words

    def get_chinese_pronunciation(self, char, text):
        mapping_table = {}
        script_dir = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(script_dir, "chs_detect", "chr_mapping_table.txt"), "r", encoding="utf-8") as file:
            lines = file.read().splitlines()

            for i in range(1, len(lines), 2):
                query_chars = lines[i].strip()
                if char in query_chars:
                    pronunciation = lines[i - 1].strip()
                    return pronunciation

        # If the character is not found in any sequence, use the original character
        return char

    def chn_prc_detector(self, text):
        pronunciations = [self.get_chinese_pronunciation(char, text) for char in text if self.is_chinese_char(char)]

        pronunciation_string = ' '.join(pronunciations)

        detected_words = []

        for bad_word in self.prc_external_bad_words:
            if bad_word in pronunciation_string and self.config.get('enable_detection', True):
                detected_words.append(bad_word)

        if self.strict_mode:
            for strict_word in self.prc_strict_bad_words:
                if strict_word in pronunciation_string:
                    detected_words.append(strict_word)

        return detected_words


    def is_chinese_char(self, char):
        # Check if the character is a Chinese character
        return '\u4e00' <= char <= '\u9fff'

    def split_chinese_text(self, text):
        # Function to split Chinese text into individual characters
        return [char for char in text if self.is_chinese_char(char) or char.isspace()]

    def detector(self, text):
        eng_detected_words = self.eng_detector(text)
        chn_detected_words= self.chn_prc_detector(text)

        if eng_detected_words:
            return eng_detected_words
        elif chn_detected_words:
            return chn_detected_words
        else:
            return []


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