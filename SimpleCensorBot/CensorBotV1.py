import json
import re
import os

class CensorBot:
    version = "0.1.2"
    print("Simple Censor Bot | Made by @bhop0 team | ver.", version, "\nGithub: https://github.com/bhop0 \n")

    def __init__(self, word_list_file="badwords.txt", substitution_file="bypass.json"):
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.external_bad_words = self.load_badwords(os.path.join(script_dir, word_list_file))
        self.substitution_dict = self.load_bypass_dict(os.path.join(script_dir, substitution_file))

        # Hardcoded bad words
        self.hardcoded_bad_words = ["niggas", "negus", "nigga", "niggas'", "nigga's"]

    def load_badwords(self, word_list_file):
        try:
            with open(word_list_file, "r", encoding="utf-8") as file:
                return [line.strip().lower() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: Bad words file '{word_list_file}' not found.")
            return []

    def load_bypass_dict(self, substitution_file):
        try:
            with open(substitution_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Substitution file '{substitution_file}' not found.")
            return {}

    def bypass_detect(self, text):
        for original, substitutions in self.substitution_dict.items():
            for substitution in substitutions:
                text = text.replace(substitution, original)
        return text

    def detector(self, text):
        text_without_spaces = text.replace(" ", "") # Remove spaces
        text_without_spaces = text_without_spaces.replace("\n", "")  # Remove newline characters
        text_with_substitutions = self.bypass_detect(text_without_spaces)

        words = re.findall(r'\b\w+\b', text_with_substitutions)

        detected_words = []

        for i in range(len(words)):
            word = words[i]
            word_lower = word.lower()

            # Combine single letters separated by spaces
            while i + 1 < len(words) and len(word) == 1 and word.isalpha() and len(words[i + 1]) == 1 and words[i + 1].isalpha():
                word += words[i + 1]
                i += 1

            if word_lower in self.external_bad_words or word_lower in self.hardcoded_bad_words:
                detected_words.append(word_lower)

        return detected_words

#Example usage:

"""

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
            
"""
