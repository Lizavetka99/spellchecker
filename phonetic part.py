import re

dict_mistake = {
    "-": "", "ъ": "", "ь": "", "стн": "сн", "ндш": "нш", "стл": "сл", "здн": "зн", "вств": "ств",
    "здц": "сц", "лнц": "нц", "ндц": "нц", "нтг": "нг", "рдч": "рч", "сч": "ш", "зч": "ш", "жч": "ш", "сш": "ш",
    "тч": "ш",
    "стг": "сг", "хг": "г", "тс": "ц", "дц": "ц", "о": "а", "ё": "а", "ю": "у", "я": "и", "ы": "и", "е": "и", "э": "и",
    "б": "п", "з": "с", "д": "т", "в": "ф", "г": "к", "щ": "ш", "ч": "ш", "ж": "ш", "ц": "ш"
}

#приводит слово к фонетически чистому виду, готовое для поиска в фонетическом словаре
def phonetic_processing(word_ph):
    for key, value in dict_mistake.items():
        word_ph = word_ph.replace(key, value)
    pattern = r'([бвгджзйклмнпрстфхцчшщ])\1+'
    return re.sub(pattern, r'\1', word_ph, flags=re.IGNORECASE)


def load_phonetic_dictionary(path):
    phonetic_dict = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    correct_word, phonetic_label = parts
                    pattern = r'([бвгджзйклмнпрстфхцчшщ])\1+'
                    phonetic_label = re.sub(pattern, r'\1', phonetic_label, flags=re.IGNORECASE)
                    phonetic_dict.setdefault(phonetic_label.lower(), []).append(correct_word.lower())
    except Exception as ex:
        print(f"Ошибка при загрузке фонетического словаря: {ex}")
    return phonetic_dict



if __name__ == "__main__":
    phonetic_dictionary_path = "assets/russian_fonetic.txt"
    phonetic_dict = load_phonetic_dictionary(phonetic_dictionary_path)
    text = input().split()
    new_text = []
    result_text =[]
    for word in text:
        new_word = phonetic_processing(word)
        new_text.append(new_word)
        if new_word in phonetic_dict:
            result_text.append(f"({phonetic_dict[new_word]})")
        else: result_text.append(word)
    print(*new_text)
    print(*result_text)
