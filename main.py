
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import heapq
import re

init()

dict_misprint = {
    "й": "цф", "ц": "йфыву", "у": "цывак", "к": "увапе", "е": "капрн", "н": "епрог", "г": "нрлшо", "ш": "годщл",
    "щ": "шлджз", "з": "щджэх", "х": "зжэъ", "ъ": "хэ",
    "ф": "йцычя", "ы": "цвфчяу", "в": "уыасчк", "а": "квпсме", "п": "еармни", "р": "нпоитг", "о": "гшрлть",
    "л": "шоьбдщ",
    "д": "щзлжбю", "ж": "зхдэю", "э": "хжъ",
    "я": "фыч", "ч": "яывс", "с": "чвам", "м": "сапи", "и": "мпрт", "т": "ироь", "ь": "толб", "б": "ьлдю", "ю": "бдж"
}

dict_mistake = {
    "-": "", "ъ": "", "ь": "", "стн": "сн", "ндш": "нш", "стл": "сл", "здн": "зн", "вств": "ств",
    "здц": "сц", "лнц": "нц", "ндц": "нц", "нтг": "нг", "рдч": "рч", "сч": "ш", "зч": "ш", "жч": "ш", "сш": "ш",
    "тч": "ш",
    "стг": "сг", "хг": "г", "тс": "ц", "дц": "ц", "о": "а", "ё": "а", "ю": "у", "я": "и", "ы": "и", "е": "и", "э": "и",
    "б": "п", "з": "с", "д": "т", "в": "ф", "г": "к", "щ": "ш", "ч": "ш", "ж": "ш", "ц": "ш"
}

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            removal = current_row[j] + 1
            replacement = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, removal, replacement))
        previous_row = current_row

    return previous_row[-1]

def load_dictionary(path):
    dict = set()
    try:
        with open(path, 'r', encoding="windows-1251") as file:
            for line in file:
                dict.add(line.strip().lower())
    except Exception as ex:
        print(f"Ошибка при загрузке словаря: {ex}")
    return dict

def check_word(word, dictionary):
    return word.lower() in dictionary

def find_closest_word(word, dictionary):
    min_dist = float('inf')
    closests_words = []
    for candidate in dictionary:
        dist = levenshtein_distance(word, candidate)
        if dist < min_dist:
            min_dist = dist
            closests_words.clear()
        if dist == min_dist:
            closests_words.append(candidate)
    return closests_words

def process_word(word, dictionary, phonetic_dict):
    is_correct = check_word(word, dictionary)
    color = Fore.GREEN if is_correct else Fore.RED
    if color == Fore.RED:
        closest_words = find_closest_word(word, dictionary)
        phonetic_word = apply_phonetic_replacements(word)
        phonetic_word = remove_consecutive_duplicates(phonetic_word)
        phonetic_correct_word = check_phonetic_word(phonetic_word, phonetic_dict)
        if phonetic_correct_word:
            closest_words.append(phonetic_correct_word)
        return f'{color}{word}{Style.RESET_ALL}({", ".join(closest_words)})'
    else:
        return f'{color}{word}{Style.RESET_ALL}'

def apply_phonetic_replacements(word):
    for key, value in dict_mistake.items():
        word = word.replace(key, value)
    return word

def remove_consecutive_duplicates(word):
    pattern = r'([бвгджзйклмнпрстфхцчшщ])\1+'
    return re.sub(pattern, r'\1', word, flags=re.IGNORECASE)

def load_phonetic_dictionary(path):
    phonetic_dict = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    correct_word, phonetic_label = parts
                    phonetic_dict.setdefault(phonetic_label.lower(), []).append(correct_word.lower())
    except Exception as ex:
        print(f"Ошибка при загрузке фонетического словаря: {ex}")
    return phonetic_dict

def check_phonetic_word(word, phonetic_dict):
    if word in phonetic_dict:
        return phonetic_dict[word][0]
    return None

def main():
    dictionary_path = "assets/russian.txt"
    phonetic_dictionary_path = "assets/russian_fonetic.txt"
    dictionary = load_dictionary(dictionary_path)
    phonetic_dict = load_phonetic_dictionary(phonetic_dictionary_path)
    text = input().replace(".", "").split()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda word: process_word(word, dictionary, phonetic_dict), text))

    print(" ".join(results))

if __name__ == "__main__":
    main()
