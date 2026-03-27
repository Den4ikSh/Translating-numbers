import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Функции для работы с римской системой
def to_roman(n):
    if not 0 < n < 4000:
        raise ValueError("Римская система поддерживает числа от 1 до 3999")

    roman_numerals = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    result = []
    for value, numeral in roman_numerals:
        count = n // value
        n -= count * value
        result.append(numeral * count)

    return ''.join(result)


def from_roman(roman):
    roman = roman.upper()
    valid_chars = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
    if not all(char in valid_chars for char in roman):
        raise ValueError("Недопустимые символы в римском числе")

    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    for char in reversed(roman):
        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


# Функции для работы с азбукой Морзе
MORSE_DIGITS = {
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}


def to_morse(n):
    s = str(n)
    return ' '.join(MORSE_DIGITS[digit] for digit in s)


def from_morse(morse):
    reverse_morse = {v: k for k, v in MORSE_DIGITS.items()}
    digits = morse.split()
    return int(''.join(reverse_morse[d] for d in digits))


# Функции для работы с греческой системой
GREEK_NUMERALS = {
    1: 'α', 2: 'β', 3: 'γ', 4: 'δ', 5: 'ε',
    6: 'ϛ', 7: 'ζ', 8: 'η', 9: 'θ', 10: 'ι',
    20: 'κ', 30: 'λ', 40: 'μ', 50: 'ν', 60: 'ξ',
    70: 'ο', 80: 'π', 90: 'ϟ', 100: 'ρ', 200: 'σ',
    300: 'τ', 400: 'υ', 500: 'φ', 600: 'χ', 700: 'ψ',
    800: 'ω', 900: 'ϡ'
}


def to_greek(n):
    if n < 1 or n > 999:
        raise ValueError("Поддерживаются числа от 1 до 999")

    if n in GREEK_NUMERALS:
        return GREEK_NUMERALS[n]

    hundreds = n // 100 * 100
    tens = (n % 100) // 10 * 10
    units = n % 10

    result = []
    if hundreds:
        result.append(GREEK_NUMERALS[hundreds])
    if tens:
        result.append(GREEK_NUMERALS[tens])
    if units:
        result.append(GREEK_NUMERALS[units])

    return ''.join(result)


def from_greek(greek):
    reverse_greek = {v: k for k, v in GREEK_NUMERALS.items()}

    total = 0
    for char in greek:
        if char in reverse_greek:
            total += reverse_greek[char]
        else:
            raise ValueError(f"Недопустимый греческий символ: {char}")

    return total


# Функции для работы с еврейской системой (гематрия)
HEBREW_NUMERALS = {
    1: 'א', 2: 'ב', 3: 'ג', 4: 'ד', 5: 'ה',
    6: 'ו', 7: 'ז', 8: 'ח', 9: 'ט', 10: 'י',
    15: 'ט"ו', 16: 'ט"ז',  # Специальные комбинации для 15-16
    20: 'כ', 30: 'ל', 40: 'מ', 50: 'נ', 60: 'ס',
    70: 'ע', 80: 'פ', 90: 'צ', 100: 'ק', 200: 'ר',
    300: 'ש', 400: 'ת'
}


def to_hebrew(n):
    if n < 1 or n > 999:
        raise ValueError("Поддерживаются числа от 1 до 999")

    # Специальные случаи для 15 и 16
    if n in [15, 16]:
        return HEBREW_NUMERALS[n]

    result = []
    hundreds = n // 100
    remainder = n % 100

    # Обработка сотен (400, 500 и т.д.)
    if hundreds > 0:
        # Для чисел > 400 используем комбинации
        while hundreds > 0:
            if hundreds >= 4:
                result.append(HEBREW_NUMERALS[400])
                hundreds -= 4
            elif hundreds >= 3:
                result.append(HEBREW_NUMERALS[300])
                hundreds -= 3
            elif hundreds >= 2:
                result.append(HEBREW_NUMERALS[200])
                hundreds -= 2
            elif hundreds >= 1:
                result.append(HEBREW_NUMERALS[100])
                hundreds -= 1

    # Обработка десятков и единиц
    if remainder > 0:
        # Проверяем, является ли число "конечной" формой
        if remainder == 15 or remainder == 16:
            result.append(HEBREW_NUMERALS[remainder])
        else:
            tens = (remainder // 10) * 10
            units = remainder % 10

            if tens > 0:
                result.append(HEBREW_NUMERALS[tens])
            if units > 0:
                result.append(HEBREW_NUMERALS[units])

    return ''.join(result)


def from_hebrew(hebrew):
    # Создаем обратный словарь
    reverse_hebrew = {v: k for k, v in HEBREW_NUMERALS.items()}

    # Проверяем специальные случаи
    if hebrew in reverse_hebrew:
        return reverse_hebrew[hebrew]

    # Разбиваем строку на символы
    total = 0
    i = 0
    while i < len(hebrew):
        # Проверяем, есть ли комбинация из 2 символов
        if i + 1 < len(hebrew):
            combo = hebrew[i:i + 2]
            if combo in reverse_hebrew:
                total += reverse_hebrew[combo]
                i += 2
                continue

        # Одиночный символ
        char = hebrew[i]
        if char in reverse_hebrew:
            total += reverse_hebrew[char]
        else:
            raise ValueError(f"Недопустимый еврейский символ: {char}")
        i += 1

    return total


# Функции для работы с кириллической системой
CYRILLIC_NUMERALS = {
    1: 'А', 2: 'В', 3: 'Г', 4: 'Д', 5: 'Е',
    6: 'Ѕ', 7: 'З', 8: 'И', 9: 'Ѳ', 10: 'І',
    20: 'К', 30: 'Л', 40: 'М', 50: 'Н', 60: 'Ѯ',
    70: 'О', 80: 'П', 90: 'Ч', 100: 'Р', 200: 'С',
    300: 'Т', 400: 'У', 500: 'Ф', 600: 'Х', 700: 'Ѱ',
    800: 'Ѡ', 900: 'Ц'
}


def to_cyrillic(n):
    if n < 1 or n > 999:
        raise ValueError("Поддерживаются числа от 1 до 999")

    if n in CYRILLIC_NUMERALS:
        return CYRILLIC_NUMERALS[n]

    hundreds = n // 100 * 100
    tens = (n % 100) // 10 * 10
    units = n % 10

    result = []
    if hundreds:
        result.append(CYRILLIC_NUMERALS[hundreds])
    if tens:
        result.append(CYRILLIC_NUMERALS[tens])
    if units:
        result.append(CYRILLIC_NUMERALS[units])

    return ''.join(result)


def from_cyrillic(cyrillic):
    reverse_cyrillic = {v: k for k, v in CYRILLIC_NUMERALS.items()}

    total = 0
    for char in cyrillic:
        if char in reverse_cyrillic:
            total += reverse_cyrillic[char]
        else:
            raise ValueError(f"Недопустимый кириллический символ: {char}")

    return total


# Главный словарь систем с функциями преобразования
SYSTEMS = {
    "arabic": {
        "from_arabic": lambda n: str(n),
        "to_arabic": lambda s: int(s),
        "name": "Арабская"
    },
    "roman": {
        "from_arabic": to_roman,
        "to_arabic": from_roman,
        "name": "Римская"
    },
    "greek": {
        "from_arabic": to_greek,
        "to_arabic": from_greek,
        "name": "Греческая"
    },
    "hebrew": {
        "from_arabic": to_hebrew,
        "to_arabic": from_hebrew,
        "name": "Еврейская"
    },
    "cyrillic": {
        "from_arabic": to_cyrillic,
        "to_arabic": from_cyrillic,
        "name": "Кириллическая"
    },
    "morse": {
        "from_arabic": to_morse,
        "to_arabic": from_morse,
        "name": "Азбука Морзе"
    }
}


# Главное меню
def show_main_menu():
    print("\n" + "=" * 50)
    print(" Программа перевода чисел между системами представления")
    print("=" * 50)
    print("1. Перевод чисел")
    print("2. Просмотр систем")
    print("3. Выход из программы")
    return input("Ваш выбор: ")


# Меню просмотра систем записи чисел
def show_systems_menu():
    print("\n" + "-" * 50)
    print(" Просмотр систем записи чисел")
    print("-" * 50)
    systems = list(SYSTEMS.keys())
    for i, sys_key in enumerate(systems, 1):
        print(f"{i}. {SYSTEMS[sys_key]['name']}")
    print(f"{len(systems) + 1}. На главную")
    return input("Ваш выбор: "), systems


# Функция отображения определённой системы записи чисел с примерами представления
def show_system_examples(system_key):
    system_name = SYSTEMS[system_key]['name']
    print(f"\nПримеры представления чисел в системе '{system_name}':")

    examples = []
    # Если выбрана Римская система записи
    if system_key == "roman":
        examples = [1, 2, 3, 4, 5, 9, 10, 11, 40, 50, 90, 100, 400, 500, 900, 1000, 2025]
    # Если выбрана система записи Азбука Морзе
    elif system_key == "morse":
        print("Каждая цифра кодируется 5 символами:")
        for digit in range(10):
            morse = to_morse(digit)
            print(f"{digit}: {morse}")
        return
    # Если выбрана Еврейская система записи
    elif system_key == "hebrew":
        examples = [1, 2, 3, 4, 5, 10, 11, 15, 16, 20, 50, 100, 200, 500, 999]
    # Если выбрана иная система записи чисел
    else:
        examples = [1, 2, 3, 4, 5, 10, 11, 20, 50, 100, 200, 500, 999]

    for num in examples:
        try:
            converted = SYSTEMS[system_key]['from_arabic'](num)
            print(f"{num} = {converted}")
        except:
            continue


# Меню выбора ввода чисел
def show_convert_menu():
    print("\n" + "-" * 50)
    print(" Перевод чисел")
    print("-" * 50)
    print("1. Через файл")
    print("2. Ручной ввод")
    print("3. Назад")
    return input("Ваш выбор: ")


# Функция для обработки повторного ввода
def ask_retry():
    while True:
        retry = input("\nХотите повторить? (да/нет): ").lower()
        if retry in ['да', 'нет']:
            return retry == 'да'
        print("Пожалуйста, введите 'да' или 'нет'")


# Если выбран "Ручной ввод"
def manual_conversion():
    # Выбор системы записи, в которой находится вводимое пользователем число
    print("\nВыберите исходную систему:")
    systems = list(SYSTEMS.keys())
    for i, sys_key in enumerate(systems, 1):
        print(f"{i}. {SYSTEMS[sys_key]['name']}")

    try:
        source_choice = int(input("Ваш выбор: ")) - 1
        if source_choice < 0 or source_choice >= len(systems):
            raise ValueError
        source_system = systems[source_choice]
    except:
        print("Некорректный выбор системы!")
        return

    # Выбор системы записи, в которую пользователь переводит число
    print("\nВыберите целевую систему для преобразования:")
    for i, sys_key in enumerate(systems, 1):
        print(f"{i}. {SYSTEMS[sys_key]['name']}")

    try:
        target_choice = int(input("Ваш выбор: ")) - 1
        if target_choice < 0 or target_choice >= len(systems):
            raise ValueError
        target_system = systems[target_choice]
    except:
        print("Некорректный выбор системы!")
        return

    # Цикл для обработки повторных попыток
    while True:
        # Ввод числа, которое нужно перевести из одной системы в другую
        number_input = input("\nВведите число: ")

        try:
            # Конвертация в арабскую систему
            arabic_number = SYSTEMS[source_system]['to_arabic'](number_input)

            # Конвертация в целевую систему
            result = SYSTEMS[target_system]['from_arabic'](arabic_number)

            # Вывод результата
            print("\n" + "=" * 50)
            print(f"Исходное число: {number_input} ({SYSTEMS[source_system]['name']})")
            print(f"Перевод в {SYSTEMS[target_system]['name']}")
            print(f"Результат: {result}")
            print("=" * 50)
            return  # Успешное завершение
        except Exception as e:
            print(f"\nОшибка при конвертации: {str(e)}")
            if not ask_retry():
                return  # Выход в главное меню


# Функция для выбора файла через диалоговое окно
def select_file():
    try:
        # Создаем скрытое окно Tkinter
        root = Tk()
        root.withdraw()  # Скрываем основное окно
        root.attributes('-topmost', True)  # Поверх всех окон

        # Открываем диалог выбора файла
        file_path = askopenfilename(
            title="Выберите файл с числом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        # Закрываем окно Tkinter
        root.destroy()

        return file_path
    except:
        # Если возникла ошибка (например, на Linux без GUI), предлагаем ручной ввод
        print("Не удалось открыть диалог выбора файла. Введите путь вручную.")
        return input("\nВведите путь к файлу: ")


# Если выбран "Ввод через файл"
def file_conversion():
    # Выбор системы записи, в которой находится число в файле
    print("\nВыберите исходную систему для числа в файле:")
    systems = list(SYSTEMS.keys())
    for i, sys_key in enumerate(systems, 1):
        print(f"{i}. {SYSTEMS[sys_key]['name']}")

    try:
        source_choice = int(input("Ваш выбор: ")) - 1
        if source_choice < 0 or source_choice >= len(systems):
            raise ValueError
        source_system = systems[source_choice]
    except:
        print("Некорректный выбор системы!")
        return

    # Выбор системы записи, в которую нужно перевести число
    print("\nВыберите целевую систему для преобразования:")
    for i, sys_key in enumerate(systems, 1):
        print(f"{i}. {SYSTEMS[sys_key]['name']}")

    try:
        target_choice = int(input("Ваш выбор: ")) - 1
        if target_choice < 0 or target_choice >= len(systems):
            raise ValueError
        target_system = systems[target_choice]
    except:
        print("Некорректный выбор системы!")
        return

    # Цикл для обработки повторных попыток
    while True:
        # Выбор файла
        print("\nПожалуйста, выберите файл с числом...")
        filename = select_file()

        if not filename:
            print("Файл не выбран.")
            if not ask_retry():
                return
            continue

        try:
            # Чтение числа из файла
            with open(filename, 'r', encoding='utf-8') as file:
                number_input = file.read().strip()

            if not number_input:
                print("Файл пуст.")
                if not ask_retry():
                    return
                continue

            # Конвертация в арабскую систему
            arabic_number = SYSTEMS[source_system]['to_arabic'](number_input)

            # Конвертация в целевую систему
            result = SYSTEMS[target_system]['from_arabic'](arabic_number)

            # Вывод результата
            print("\n" + "=" * 50)
            print(f"Исходное число: {number_input} ({SYSTEMS[source_system]['name']})")
            print(f"Перевод в {SYSTEMS[target_system]['name']}")
            print(f"Результат: {result}")
            print("=" * 50)
            return  # Успешное завершение
        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
            if not ask_retry():
                return
        except Exception as e:
            print(f"\nОшибка при конвертации: {str(e)}")
            if not ask_retry():
                return


# Главные функции (Главное меню)
def main():
    try:
        while True:
            choice = show_main_menu()

            if choice == '1':  # Перевод чисел
                while True:
                    try:
                        convert_choice = show_convert_menu()
                    except KeyboardInterrupt:
                        print("\nВозврат в главное меню")
                        break

                    if convert_choice == '1':  # Через файл
                        file_conversion()
                    elif convert_choice == '2':  # Ручной ввод
                        manual_conversion()
                    elif convert_choice == '3':  # Назад
                        break
                    else:
                        print("Некорректный выбор, попробуйте снова.")

            elif choice == '2':  # Просмотр систем
                while True:
                    try:
                        system_choice, systems = show_systems_menu()
                    except KeyboardInterrupt:
                        print("\nВозврат в главное меню")
                        break

                    # если вводимое число == 6 (кол-во всех систем) + 1 (= 7), то выход на главную
                    if system_choice == str(len(systems) + 1):
                        break

                    try:
                        choice_index = int(system_choice) - 1
                        if 0 <= choice_index < len(systems):
                            show_system_examples(systems[choice_index])
                        else:
                            print("Некорректный выбор!")
                    except ValueError:
                        print("Пожалуйста, введите число!")

            elif choice == '3':  # Выход
                print("\nСпасибо за использование программы! До свидания!")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")

    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем. До свидания!")


# Запуск программы
if __name__ == "__main__":
    main()