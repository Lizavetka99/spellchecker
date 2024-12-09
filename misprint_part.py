class SpellChecker:
    def __init__(self, dictionary_path):
        self.dict_misprint = {
            "й": "цф", "ц": "йфыву", "у": "цывак", "к": "увапе", "е": "капрн", "н": "епрог", "г": "нрлшо", "ш": "годщл",
            "щ": "шлджз", "з": "щджэх", "х": "зжэъ", "ъ": "хэ",
            "ф": "йцычя", "ы": "цвфчяу", "в": "уыасчк", "а": "квпсме", "п": "еармни", "р": "нпоитг", "о": "гшрлть",
            "л": "шоьбдщ",
            "д": "щзлжбю", "ж": "зхдэю", "э": "хжъ",
            "я": "фыч", "ч": "яывс", "с": "чвам", "м": "сапи", "и": "мпрт", "т": "ироь", "ь": "толб", "б": "ьлдю", "ю": "бдж"
        }
        self.dictionary = self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        dictionary = set()
        try:
            with open(path, 'r', encoding="windows-1251") as file:
                for line in file:
                    dictionary.add(line.strip().lower())
        except Exception as ex:
            print(f"Ошибка при загрузке словаря: {ex}")
        return dictionary

    def check_in_dict(self, word):
        return word in self.dictionary

    def make_dont_misprint(self, word):
        new_words = []
        for i in range(len(word)):
            misprints = self.dict_misprint.get(word[i], '')
            for misprint in misprints:
                new_word = word[:i] + misprint + word[i+1:]
                if new_word in self.dictionary:
                    new_words.append(new_word)
        return new_words

    def for_general(self, word):
        new_words = self.make_dont_misprint(word)
        return new_words

    def process_text(self, text):
        new_text = []
        for word in text:
            if not self.check_in_dict(word):
                new_words = self.make_dont_misprint(word)
                new_text.append(f"({', '.join(new_words)})")
            else:
                new_text.append(word)
        return new_text

if __name__ == "__main__":
    dictionary_path = "assets/russian.txt"
    spell_checker = SpellChecker(dictionary_path)
    text = input().split()
    result = spell_checker.process_text(text)
    print(" ".join(result))
