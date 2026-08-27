# 🤖 Персональний помічник (Personal Assistant Bot)

Консольний бот-помічник для зручного керування контактами, нотатками та тегами з автоматичним збереженням даних на диск (`pickle`).

---

## 🚀 Як запустити проєкт

Перейдіть у кореневу папку проєкту та виконайте команду:

```bash
python src/main.py
```

---

## 📁 Структура проєкту

```text
├── src/
│   ├── main.py                   # Точка входу в програму (головний цикл бота)
│   ├── models.py                 # Класи даних (AddressBook, Record, NoteBook, Note, поля)
│   ├── handlers.py               # Функції-обробники команд бота
│   ├── storage.py                # Логіка збереження та завантаження даних на диск
│   ├── decorators.py             # Декоратор @input_error для обробки помилок вводу
│   ├── constants.py              # Перелік команд (Command) та формат дати
│   ├── config.py                 # Завантаження системних повідомлень
│   ├── utils.py                  # Функція parse_input для розбору введеного тексту
│   └── messages.json             # Тексти успішних відповідей та помилок
├── class_diagram.drawio          # UML-діаграма класів (відкривати на diagrams.net)
├── tasks.md                      # Спринт-таски за етапами розробки
└── README.md                     # Опис проєкту та довідка з команд
```

---

## 📋 Довідник команд

### 📞 Книга контактів

| Команда | Аргументи | Опис |
| :--- | :--- | :--- |
| `hello` | — | Привітання від бота. |
| `add` | `[ім'я] [телефон]` | Додати новий контакт або номер до існуючого. |
| `add-phone` | `[ім'я] [телефон]` | Додати додатковий номер телефону. |
| `change` | `[ім'я] [старий_тел] [новий_тел]` | Змінити номер телефону контакту. |
| `phone` | `[ім'я]` | Показати всі номери телефонів контакту. |
| `add-email` | `[ім'я] [email]` | Додати або оновити email адресу контакту. |
| `show-email` | `[ім'я]` | Показати email адресу контакту. |
| `add-address` | `[ім'я] [адреса...]` | Додати або оновити фізичну адресу контакту. |
| `show-address` | `[ім'я]` | Показати адресу контакту. |
| `add-birthday` | `[ім'я] [ДД.ММ.РРРР]` | Встановити день народження контакту. |
| `show-birthday` | `[ім'я]` | Показати день народження контакту. |
| `birthdays` | `[днів]` *(опціонально)* | Список іменинників на найближчі N днів (за замовчуванням 7). |
| `search-contacts` | `[запит]` | Пошук контактів за ім'ям, телефоном, email або адресою. |
| `delete` | `[ім'я]` | Видалити контакт з книги. |
| `all` | — | Показати список усіх збережених контактів. |

### 📝 Блокнот (Нотатки та теги)

| Команда | Аргументи | Опис |
| :--- | :--- | :--- |
| `add-note` | `[заголовок] [текст...]` | Створити нову текстову нотатку. |
| `show-notes` | — | Показати всі збережені нотатки. |
| `search-notes` | `[запит]` | Пошук нотаток за ключовим словом або заголовком. |
| `edit-note` | `[заголовок] [новий_текст...]` | Змінити текст існуючої нотатки. |
| `delete-note` | `[заголовок]` | Видалити нотатку за заголовком. |
| `add-tag` | `[заголовок] [тег1] [тег2...]` | Додати один або декілька тегів до нотатки. |
| `search-by-tag` | `[тег]` | Знайти всі нотатки за вказаним тегом. |
| `sort-notes-by-tags` | — | Сортувати нотатки за кількістю тегів (від більшої до меншої). |

### ⚙️ Системні команди

| Команда | Аргументи | Опис |
| :--- | :--- | :--- |
| `close` / `exit` | — | Зберегти всі дані на диск та завершити роботу помічника. |

---

## 🛠️ Як працювати з темплейтом (для розробників)

1. **Моделі даних (`src/models.py`):**
   * Реалізуйте валідацію полів: `Phone` (10 цифр), `Email` (формат email), `Birthday` (дата `ДД.ММ.РРРР`).
   * Допишіть методи роботи з контактами в `Record` та `AddressBook`.
   * Допишіть методи управління нотатками в `Note` та `NoteBook`.

2. **Збереження даних (`src/storage.py`):**
   * Реалізуйте збереження через `pickle` у файл (наприклад, у папці користувача `~/.personal_assistant/`).

3. **Обробники команд (`src/handlers.py`):**
   * Заповніть тіла функцій-хендлерів з коментарями `TODO`.
   * Як зразок готового хендлера орієнтуйтеся на функцію `add_contact`.

---

## 🧪 How to run tests

To run all unit tests for the project, simply open your terminal in the root directory and execute the following command:

```bash
python -m unittest discover -s tests/unit
```
This will automatically find and run all tests to ensure the application works correctly.

---

## 🌳 Basic Git Commands

Here are the essential Git commands used during development:

- `git switch <branch-name>`: Switch to an existing branch.
- `git switch -c <branch-name>`: Create and switch to a new branch (modern approach).
- `git add .`: Stage all modified and new files for the next commit.
- `git commit -m "commit message"`: Commit the staged changes with a descriptive message.
- `git push origin <branch-name>`: Push your local branch to the remote repository.
- `git fetch`: Download objects and refs from the remote repository (without merging them).
- `git merge <branch-name>`: Merge the specified branch into your current branch.
- `git pull`: Fetch and merge changes from the remote repository to your current branch.
- `git status`: Show the current status of your working directory and staging area.

---

## 🌟 Optional (Additional) Features

This project includes several extra features that improve the User Experience (UX), which were not strictly required by the base technical requirements:

1. **Interactive Help System**
   - The `help` command outputs a convenient list of all commands, grouped by categories (Contacts, Notes, General).
   - You can view help for a specific category or a detailed explanation of a single command.
   - Example output:
<pre><code style="background-color: #1e1e1e; padding: 10px; display: block; border-radius: 5px;">
<span style="color: #dcdcaa;">Enter a command: help</span>
<span style="color: #dcdcaa;">Available categories:</span>
<span style="color: #4ec9b0;">- Contacts</span>
<span style="color: #4ec9b0;">- Notes</span>
<span style="color: #4ec9b0;">- General</span>

<span style="color: #dcdcaa;">Type 'help &lt;category&gt;' to see commands in a category.</span>
<span style="color: #dcdcaa;">Type 'help &lt;command&gt;' to see details for a specific command.</span>

<span style="color: #dcdcaa;">Enter a command: help Contacts</span>
<span style="color: #dcdcaa;">--- Contacts ---</span>
<span style="color: #4ec9b0;">add                 </span> <span style="color: #d4d4d4;">: Adds a new contact.</span>
<span style="color: #4ec9b0;">add-phone           </span> <span style="color: #d4d4d4;">: Adds another phone to a contact.</span>
<span style="color: #d4d4d4;">...</span>
<span style="color: #dcdcaa;">For details type: help &lt;command&gt;</span>
</code></pre>

2. **Fuzzy Matching (Smart Command Search)**
   - If a user makes a typo when entering a command (e.g., `add-ntoe` instead of `add-note`), the bot automatically suggests correct options: *"Invalid command 'add-ntoe'. Did you mean: add-note?"*.

3. **Colorized CLI (ANSI Colors)**
   - The console interface is color-coded for better readability:
     - 🔴 Errors and warnings are highlighted in red.
     - 🟢 Successful actions are in green.
     - 🟡 Input prompts and menus are in yellow/cyan.
   - Implemented exclusively using the standard library (ANSI codes), with no third-party dependencies.

4. **English Localization (100% English Codebase)**
   - All internal comments, class documentation (docstrings), and TODOs are fully translated into English to adhere to best development practices.
