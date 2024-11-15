import json


def create_json_file(filename="user_data.json"):
    user_data = {
        "First name": input("First name: "),
        "Last name": input("Last name: "),
        "Book title": input("Book title: "),
        "Author": input("Author: ")
    }

    with open(filename, "w") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)
    print(f"Данные записаны в файл {filename}")


def read_json_file(filename="user_data.json"):
    try:
        with open(filename, "r") as file:
            user_data = json.load(file)
        print("Содержимое файла: ")
        for key, value in user_data.items():
            print(f"{key}: {value}")
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except json.JSONDecodeError:
        print("Ошибка чтения JSON. Проверьте формат файла.")


create_json_file()
read_json_file()

