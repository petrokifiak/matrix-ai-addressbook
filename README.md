# 🤖 Personal Assistant Bot

A console-based personal assistant bot for convenient management of contacts, notes, and tags with automatic data persistence on disk (`pickle`).

---

## 🚀 How to Run the Project

Navigate to the project root directory and run:

```bash
python src/main.py
```

---

## 📁 Project Structure

```text
├── src/
│   ├── main.py                   # Application entry point (main bot loop)
│   ├── models.py                 # Data models (AddressBook, Record, NoteBook, Note, Fields)
│   ├── handlers.py               # Bot command handler functions
│   ├── help.py                   # Interactive help system
│   ├── storage.py                # Data persistence logic (save/load from disk)
│   ├── decorators.py             # @input_error decorator for user input error handling
│   ├── constants.py              # Command enums, ANSI colors, and date formats
│   ├── config.py                 # System messages loader
│   ├── utils.py                  # Helper functions (parse_input, print_colored)
│   └── messages.json             # Texts of responses and error messages
├── tests/
│   ├── unit/                     # Unit tests (models, handlers)
│   │   ├── test_models.py
│   │   └── test_handlers.py
│   └── integration/              # Integration tests
│       └── test_integration.py
├── class_diagram.drawio          # UML class diagram (open via diagrams.net)
└── README.md                     # Project overview and documentation
```

---

## 📋 Command Reference

### 📞 Contacts Book

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `hello` | — | Greeting from the bot. |
| `add` | `[name] [phone]` | Add a new contact or phone number to an existing one. |
| `add-phone` | `[name] [phone]` | Add an additional phone number to a contact. |
| `change` | `[name] [old_phone] [new_phone]` | Change an existing phone number of a contact. |
| `phone` | `[name]` | Show all phone numbers of a contact. |
| `add-email` | `[name] [email]` | Add or update the email address of a contact. |
| `show-email` | `[name]` | Show the email address of a contact. |
| `add-address` | `[name] [address...]` | Add or update the physical address of a contact. |
| `show-address` | `[name]` | Show the physical address of a contact. |
| `add-birthday` | `[name] [DD.MM.YYYY]` | Set the birthday for a contact. |
| `show-birthday` | `[name]` | Show the birthday of a contact. |
| `birthdays` | `[days]` *(optional, default 7)* | List upcoming birthdays within the next N days (with weekend shift). |
| `search-contacts` | `[query]` | Search contacts by name, phone, email, or address substring. |
| `delete-contact` / `delete` | `[name]` | Delete a contact from the address book. |
| `all` | — | Show all saved contacts. |

### 📝 NoteBook (Notes & Tags)

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `add-note` | `[title] [content...]` | Create a new text note. |
| `show-notes` / `all-notes` | — | Show all saved notes. |
| `search-notes` | `[query]` | Search notes by keyword or title substring. |
| `edit-note` | `[ID_or_title] [new_content...]` | Edit the text of an existing note. |
| `delete-note` | `[ID_or_title]` | Delete a note by its ID or title. |
| `add-tag` | `[ID_or_title] [tag1] [tag2...]` | Add one or more tags to a note. |
| `search-by-tag` | `[tag]` | Find all notes matching a specific tag. |
| `sort-notes-by-tags` | `[tag1 tag2...]` *(optional)* | Sort notes by matching tags (relevance descending) or total tags. |

### ⚙️ System & General Commands

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `help` | `[command/category]` *(optional)* | Display interactive help for all or specific commands. |
| `close` / `exit` | — | Save all data to disk and exit the assistant. |

---

## 🛠️ Developer Guide (Working with the Template)

1. **Data Models (`src/models.py`):**
   * Field validation: `Phone` (10 digits), `Email` (email format), `Birthday` (date format `DD.MM.YYYY`), `Address` & `Name` (non-empty).
   * Methods for contact management in `Record` and `AddressBook`.
   * Methods for note management in `Note` and `NoteBook`.

2. **Data Persistence (`src/storage.py`):**
   * Persistence mechanism using `pickle` to a file in the user directory (`~/.personal_assistant/assistant_data.pkl`).

3. **Command Handlers (`src/handlers.py`):**
   * Modular handlers decorated with `@input_error` for robust exception handling.

---

## 🧪 How to Run Tests

To run all unit and integration tests for the project, execute the following command:

```bash
# Run using pytest (recommended)
python -m pytest

# Or using standard unittest
python -m unittest discover -s tests
```

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
   - All internal comments, class documentation (docstrings), and code artifacts are fully written in English to adhere to best development practices.
