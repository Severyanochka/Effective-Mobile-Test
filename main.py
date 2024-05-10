import json  # Импорт модуля json для работы с JSON
import os  # Импорт модуля os для работы с файловой системой (проверки существует ли искомый файл. Это помогает избежать ошибок, если файл не существует, и предотвращает исключение.)
from typing import List, Dict, Any



class DataFormat:
    def __init__(self, date: str, category: str, amount: float, description: str = "") -> None:
        """
        Класс определяющий формат данных.

        :param date: Дата в формате 'гггг-мм-дд'.
        :param category: Категория ('Доход' или 'Расход').
        :param amount: Сумма.
        :param description: Описание. По умолчанию пустая строка.
        """

        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def dictionary(self) -> Dict[str, Any]:
        """
         Метод преобразования данных в словарь.

        :return:
            Dict[str, Any]: Словарь с данными.
        """
        return {
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }


class DataControl:
    def __init__(self, filename: str) -> None:
        """
        Класс по управлению данными.

        :param filename: Имя файла для хранения данных.
        """
        self.filename = filename

    def read_file(self) -> List[Dict[str, Any]]:
        """
        Метод для чтения данных из файла.

        :return:
            List[Dict[str, Any]]: Список словарей с данными.
        """

        if os.path.exists(self.filename):  # Проверка наличия файла os.path: Это модуль в стандартной библиотеке Python, который предоставляет функции для работы с путями к файлам и директориям в файловой системе.exists: Это функция модуля os.path, которая проверяет, существует ли файл или директория по указанному пути.
            with open(self.filename, 'r') as file:  # Открытие файла для чтения 'r' означает режим "чтение" (read), что позволяет только читать данные из файла. file объект используемый для доступа к информации из файла
                return json.load(file)  # Загрузка данных из файла JSON и возврат результата в формате Python
        else:
            return []

    def save_records(self, records: List[Dict[str, Any]]) -> None:
        """
        Метод для сохранения данных в файл.

        :param records: Список словарей с данными.
        """
        with open(self.filename, 'w') as file:  # Открытие файла для записи, из-за команды w старое содержимое зааменится новым
            json.dump(records, file,
                      indent=4)  # Сериализация данных в JSON и запись в файл с отступами для удобства чтения

    def add_record(self, record: DataFormat) -> None:
        """
        Метод добавления записи.

        :param record: Экземпляр класса DataFormat.
        """
        records = self.read_file()
        records.append(record.dictionary())  # Добавление новой записи преобразуя ее в словарь
        self.save_records(records)

    def update_record(self, index: int, updated_record: DataFormat) -> bool:
        """
        Метод обновления записи.

        :param index: Индекс записи.
        :param updated_record: Обновленная запись.
        :return:
            bool: Результат выполнения операции (успешно или нет).
        """
        records = self.read_file()
        if 0 <= index < len(records): # Если такая запись есть, то ее заменить
            records[index] = updated_record.dictionary()
            self.save_records(records)
            return True
        else:
            return False

    def search_records(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Метод для поиска записей по критериям.

        :param search_criteria: Критерии поиска.
        :return:
            List[Dict[str, Any]]: Список найденных записей.
        """
        records = self.read_file()
        matching_records = []
        for record in records:
            if all(record[key] == value for key, value in search_criteria.items()):
                matching_records.append(record)
        return matching_records


class UserInterface:
    def actual_balance(self, balance: float, income: float, expenses: float) -> None:
        """
        Метод для вывода текущего баланса.

        :param balance:Текущий баланс.
        :param income: Доход.
        :param expenses:Pасходы.
        """
        print('Текущий баланс:', balance)
        print('Текущий доход:', income)
        print('Текущий расход:', expenses)

    def display_records(self, records: List[Dict[str, Any]]) -> None:
        """
        Метод для вывода записей на консоль.

        :param records: Список словарей с данными.
        """
        for record in records:
            print('Дата:', record['date'], 'Категория:', record['category'], 'Сумма:', record['amount'], 'Описание:', record['description'])

    def input_record(self) -> DataFormat:
        """
        Метод для ввода данных.

        :return:
            DataFormat: Экземпляр класса DataFormat.
        """
        date= input('Введите дату (гггг-мм-дд): ')

        while True:
            category_choice = input('Введите число для выбора категории (1 - Доход, 2 - Расход): ')
            if category_choice == '1':
                category = 'Доход'
                break
            elif category_choice == '2':
                category = 'Расход'
                break
            else:
                    print('Некорректный ввод. Пожалуйста, введите 1 для Дохода или 2 для Расхода.')
        while True:
            amount = float(input('Введите сумму: '))
            if amount >= 0:
                break
            else:
                print('Некорректный ввод. Введите положительное число')
        description = input('Введите описание: ')
        return DataFormat(date, category, amount, description)

    def input_search_criteria(self) -> Dict[str, Any]:
        """
        Метод для ввода критериев поиска.

        :return:
            Dict[str, Any]: Словарь с критериями поиска.
        """
        date = input('Введите дату для поиска (гггг-мм-дд): ')
        category = input('Введите категорию для поиска (Доход/Расход): ')
        return {'date': date, 'category': category}


class Main:
    def __init__(self, data_manager: DataControl, ui: UserInterface) -> None:
        """
        Главный класс приложения

        :param data_manager: Объект для управления данными.
        :param ui: Объект пользовательского интерфейса.
        """
        self.data_manager = data_manager
        self.ui = ui

    def start_application(self) -> None:
        """
        Метод для запуска приложения.
        """
        while True:
            choice = input('Выберите действие: 1 - Вывод баланса, 2 - Добавление записи, 3 - Вывод записей, 4 - Изменение записи, 5 - Поиск по записям, 0- Выход ')

            if choice == '1':
                self.display_balance()
            elif choice == '2':
                self.add_record()
            elif choice == '3':
                self.display_records()
            elif choice == '4':
                self.changing_record()
            elif choice == '5':
                self.search_records()
            elif choice == '0':
                break
            else:
                print('Некорректный ввод')

    def display_balance(self) -> None:
        """
        Метод для вывода текущего баланса.
        """
        records = self.data_manager.read_file()
        income = sum(record['amount'] for record in records if record['category'] == 'Доход')
        expenses = sum(record['amount'] for record in records if record['category'] == 'Расход')
        balance = income - expenses
        self.ui.actual_balance(balance, income, expenses)

    def add_record(self) -> None:
        """
        Метод для добавления записи.
        """
        record = self.ui.input_record()
        self.data_manager.add_record(record)

    def display_records(self) -> None:
        """
        Метод для вывода записи.
        """
        records = self.data_manager.read_file()
        self.ui.display_records(records)

    def changing_record(self) -> None:
        """
        Метод для изменения записи.
        """
        records = self.data_manager.read_file()
        if not records:
            print("Нет доступных записей для изменения.")
            return

        self.ui.display_records(records)
        index = int(input("Введите номер записи, которую хотите изменить: ")) - 1
        if 0 <= index < len(records):
            updated_record = self.ui.input_record()
            success = self.data_manager.update_record(index, updated_record)
            if success:
                print("Запись успешно изменена.")
            else:
                print("Не удалось изменить запись.")
        else:
            print("Некорректный номер записи.")

    def search_records(self) -> None:
        """
        Метод для поиска записи.
        """
        search_criteria = self.ui.input_search_criteria()
        matching_records = self.data_manager.search_records(search_criteria)
        if matching_records:
            self.ui.display_records(matching_records)
        else:
            print("По вашему запросу ничего не найдено.")


if __name__ == "__main__":
    filename = "financial_records.json"
    data_manager = DataControl(filename)
    ui = UserInterface()
    app = Main(data_manager, ui)
    app.start_application()