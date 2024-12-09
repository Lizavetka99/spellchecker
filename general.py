# main.py
from phonetic_part import PhoneticPart
from misprint_part import SpellChecker
from colorama import Fore, Style, init

def main1(text):

    result = spell_checker.for_general(text)
    # print(" ".join(result))
    return result


def main(word):

    result_text = phonetic_part.for_general(word)
    #print(*new_text)
    # print(*result_text)
    return result_text


if __name__ == "__main__":
    dictionary_path = "assets/russian.txt"
    spell_checker = SpellChecker(dictionary_path)
    phonetic_dictionary_path = "assets/russian_fonetic.txt"
    phonetic_part = PhoneticPart(phonetic_dictionary_path)

    running = True
    while running:
        text = input().strip()  # Убираем пробелы по краям и не разбиваем на символы
        output = ""
        if text == "QUIT":
            running = False
        else:
            words = text.split()  # Разбиваем текст на слова
            for word in words:
                if not spell_checker.check_in_dict(word):
                    result1 = main(word)
                    result2 = main1(word)
                    color = Fore.RED
                    output += f'{Fore.RESET}{word} {Fore.RED}({", ".join(result2 + result1)})'
                    #print(f'{color}{" ".join(result2 + result1)}')
                    # print(result2)
                    # print(*result1)
                else:
                    output += f'{Fore.GREEN}{word}'
                    # print(f'{color}{word}')
                output += " "
            print(output)
