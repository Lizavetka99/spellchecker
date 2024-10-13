from colorama import Fore, Style, init

init()


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


def main():
    dictionary_path = "assets/russian.txt"
    dictionary = load_dictionary(dictionary_path)
    text = input().replace(".", "").split()
    result = []
    for slovo in text:
        is_correct = check_word(slovo, dictionary)
        color = Fore.GREEN if is_correct else Fore.RED
        if color is Fore.RED:
            min_sl = ""
            min_dist = 10000
            for i in dictionary:
                dist = levenshtein_distance(i, slovo)
                if dist < min_dist:
                    min_dist = dist
                    min_sl = i
            result.append(f'{color}{slovo}{Style.RESET_ALL}({min_sl})')
        else:   result.append(f'{color}{slovo}{Style.RESET_ALL}')
    print(" ".join(result))


if __name__ == "__main__":
    main()
