Українська версія (UA)

Команда: DIPE — Dynamic International Partnership for Excellence

# Опис проєкту

Personal Assistant (персональний помічник) — це консольна Python-програма, що дозволяє зручно зберігати, шукати та редагувати особисту інформацію, включаючи:

- Контакти (ім’я, номер телефону, email, дата народження, адреса)
- Нотатки

Програма зберігає всі дані локально на жорсткому диску, що дозволяє працювати з ними навіть після перезапуску програми. 


# Структура проєкту

```bash
project-v_i_pvsk/
├── README.md               # Документація
├── requirements.txt        # Залежності
├── setup.py                # Налаштування пакету
└── src/
    ├── main.py             # Точка входу
    ├── commands.py         # Команди CLI
    ├── formatters.py       # Форматування виводу
    ├── handlers.py         # Обробка команд
    ├── models.py           # Класи Field, Record, AddressBook
    ├── storage.py          # Серіалізація (pickle)
    ├── utils.py            # Валідація email/телефону

```


# Використані технології

- Python 3.11+
- ООП: Field, Record, AddressBook, Note, NotesBook
- Модулі: datetime, pickle, collections, re, difflib, colorama, tabulate
- Централізована валідація: через utils.py
- GitHub: Kateryna286/project-v_i_pvsk


# Основний функціонал

1) Контакти:

- Додавання нового контакту (ім’я, телефон, email, дата народження, адреса);
- Пошук за ім’ям, номером телефону, email, адресою;
- Редагування та видалення контактів;
- Перевірка днів народження за вказану кількість днів;
- Валідація номерів телефону та email;


2) Нотатки:

- Додавання нотаток
- Пошук за ключовими словами
- Редагування та видалення нотаток


3) Збереження даних:

- Усі дані автоматично зберігаються у локальній папці користувача.
- Після перезапуску програми вся інформація зберігається.


# Встановлення

Примітка: Необхідно мати встановлений Python 3.10 або новішої версії.

1) Клонуйте репозиторій:

```bash
git clone https://github.com/Kateryna286/project-v_i_pvsk.git
cd project-v_i_pvsk
```


2) Створіть та активуйте віртуальне середовище:

Для Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

Для macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```


3)  Встановіть залежності (за потреби):

```bash
pip install -r requirements.txt
```


# Запуск

Для запуску програми виконайте в терміналі:

```bash
python src/main.py
```


# Приклади команд

1) Додати контакт:

```bash
add_contact --name "Іван Іванов" --phone "0671234567" --email "ivan@email.com" --birthday "01.01.1990" --address "м. Київ, вул. Хрещатик"
```


2) Знайти контакт:

```bash
search_contact "Іван"
```

Очікуваний результат:

Знайдено 1 контакт:
Ім'я: Іван Іванов, Телефон: 0671234567, Email: ivan@email.com, ...


3) Додати нотатку:

```bash
add_note "Купити молоко і хліб"
```


# Як зробити внесок

Ми раді будь-якому внеску! Якщо у вас є ідеї щодо нових функцій або ви знайшли помилку, будь ласка, створіть "issue" або зробіть "pull request".

1) Зробіть форк репозиторію.
2) Створіть нову гілку (git checkout -b feature/your-feature-name).
3) Внесіть свої зміни.
4) Зробіть коміт (git commit -m 'Add some feature').
5) Відправте зміни у вашу гілку (git push origin feature/your-feature-name).
6) Створіть Pull Request.


# Автори

DIPE - Dynamic International Partnership for Excellence

Валентин — 🇬🇧
Віталій — 🇩🇰
Катерина — 🇵🇱
Світлана — 🇮🇪


# TODO

[ ] Додати GUI-інтерфейс (опціонально)
[ ] Інтеграція з календарем Google
[ ] Розширений формат пошуку нотаток по даті