dict_misprint = {
    "й": "цф", "ц": "йфыву", "у": "цывак", "к": "увапе", "е": "капрн", "н": "епрог", "г": "нрлшо", "ш": "годщл",
    "щ": "шлджз", "з": "щджэх", "х": "зжэъ", "ъ": "хэ",
    "ф": "йцычя", "ы": "цвфчяу", "в": "уыасчк", "а": "квпсме", "п": "еармни", "р": "нпоитг", "о": "гшрлть",
    "л": "шоьбдщ",
    "д": "щзлжбю", "ж": "зхдэю", "э": "хжъ",
    "я": "фыч", "ч": "яывс", "с": "чвам", "м": "сапи", "и": "мпрт", "т": "ироь", "ь": "толб", "б": "ьлдю", "ю": "бдж"
}


def load_dictionary(path):
    dict = set()
    try:
        with open(path, 'r', encoding="windows-1251") as file:
            for line in file:
                dict.add(line.strip().lower())
    except Exception as ex:
        print(f"Ошибка при загрузке словаря: {ex}")
    return dict


def check_in_dict(word, dict):
    if word in dict:
        return True
    return False


def make_dont_misprint(word, dictionary):
    new_words = []
    for i in range(len(word)):
        misprints = dict_misprint[word[i]]
        char_list = list(word)
        for misprint in misprints:
            char_list[i] = misprint
            new_word = ''.join(char_list)
            if new_word in dictionary:
                new_words.append(new_word)
    return new_words


if __name__ == "__main__":
    dictionary_path = "assets/russian.txt"
    dictionary = load_dictionary(dictionary_path)
    text = input().split()
    new_text = []
    for word in text:
        if not check_in_dict(word, dictionary):
            new_words = make_dont_misprint(word, dictionary)
            new_text.append(f"({new_words})")
        else:new_text.append(word)
    print(new_text)
