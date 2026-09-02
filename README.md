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
| `delete-contact` / `delete` | `[name]` | Archive a contact (soft delete). |
| `restore-contact` | `[name]` | Restore an archived contact. |
| `archived` | — | Show all archived contacts. |
| `all` | `[--all \| -a]` *(optional)* | Show all active contacts. Use `--all` or `-a` to include archived. |
| `export-contacts` | `[filename.csv/json]` | Export contacts to a CSV or JSON file. |
| `import-contacts` | `[filepath]` | Import contacts from a CSV or JSON file. |
| `clear-contacts` | — | Clears all saved contacts. |

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
| `export-notes` | `[filename.json]` | Export notes to a JSON file. |
| `import-notes` | `[filepath.json]` | Import notes from a JSON file. |
| `clear-notes` | — | Clears all saved notes. |

### ⚙️ System & General Commands

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `help` | `[command/category]` *(optional)* | Display interactive help for all or specific commands. |
| `clear-data` | — | Clears all saved contacts and notes. |
| `close` / `exit` | — | Save all data to disk and exit the assistant. |

---

## 🛠️ Developer Guide (Working with the Template)

1. **Data Models (`src/models/`):**
   * Field validation: `Phone` (10 digits), `Email` (email format), `Birthday` (custom date validation handling leap years), `Address` & `Name` (non-empty).
   * Methods for contact management in `Record` and `AddressBook`.
   * Methods for note management in `Note` and `NoteBook`.

2. **Data Persistence (`src/storage/`):**
   * Persistence mechanism using `pickle` to a file in the user directory (`~/.personal_assistant/assistant_data.pkl`), utilizing the Repository pattern.

3. **Command Architecture (`src/commands/` & `src/core/`):**
   * Completely refactored to use the **Command Pattern**. All commands are encapsulated in individual classes.
   * Employs **Middleware** (Chain of Responsibility) for validation and logging before a command is executed.
    * Event-driven architecture for handling decoupled notifications.

---

## 🏛️ Architecture, Patterns & Libraries

### Design Patterns
1. **Command Pattern**: Encapsulates requests as objects, allowing for parameterization of clients with queues or logs.
   * *Example*: `AddContactCommand`, `ShowAllCommand` in `src/commands/`.
2. **Chain of Responsibility (Middleware)**: Passes a request along a chain of handlers.
   * *Example*: `ValidationMiddleware` ensures the application state is valid before allowing any command to execute.
3. **Observer Pattern**: Defines a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.
   * *Example*: `dispatcher.dispatch("NOTE_ADDED")` notifies the `LoggingObserver` to log the event without coupling the command to the logger.
4. **Repository Pattern**: Mediates between the domain and data mapping layers acting like an in-memory collection of domain objects.
   * *Example*: `PickleStorage` in `src/storage/` abstracts the `pickle` read/write operations from the application logic.

### External Libraries & Modules
1. **`prompt_toolkit`**: Used for building the powerful interactive command-line interface.
   * *Feature*: Provides auto-completion (`WordCompleter`) and command history navigation (`FileHistory`).
2. **`rich`**: A Python library for rich text and beautiful formatting in the terminal.
   * *Feature*: Renders list-based outputs (contacts, notes, birthdays) as aligned, colored tables (`rich.table.Table`).
3. **`pytest`**: A framework that makes building simple and scalable tests easy.
   * *Feature*: Used extensively in the `tests/` directory to run unit and integration tests for the new OOP architecture.

---

## 🧪 How to Run Tests

To run all unit and integration tests for the project, execute the following command:

```bash
# if need call firt
deactivate
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

3. **Advanced CLI Interface (`prompt_toolkit` & `rich`)**
   - **Interactive Prompt:** Features auto-completion for commands and command history navigation (using Up/Down arrows).
   - **Rich Tables:** All list-based outputs (e.g., viewing contacts, notes, and birthdays) are rendered as beautiful, formatted, and aligned tables using the `rich` library.

4. **English Localization (100% English Codebase)**
   - All internal comments, class documentation (docstrings), and code artifacts are fully written in English to adhere to best development practices.
