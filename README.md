<div align="center">

<pre>
 _       _        ___
| |__   / \   ___|_ _|___
| '_ \ / _ \ / __|| |/ __|
| |_) / ___ \\__ \| | (__
|_.__/_/   \_\___/___\___|
</pre>

**bAsIc**  
A basic AI that can answer some basic questions.

</div>

---

### Overview

`bAsIc` is a very simple, terminal-based AI chatbot.  
It can respond to a **small set of predefined questions**, generate **Fibonacci sequences**, and evaluate **basic calculator expressions**.

Originally created by **Herbert Kumar** as a tiny experiment in building a “basic AI”.

### Features

- **Predefined responses**: Answers to a curated list of questions (e.g. *How are you?*, *What are you doing?*).
- **Fibonacci helper**: Generates the first \(n\) Fibonacci numbers on request.
- **Calculator**: Evaluates basic math expressions like `2 + 2 * 3`.
- **Friendly greeting**: ASCII-art banner and name prompt when you start the program.
- **Input normalization**: Ignores case and most punctuation so you don’t have to type questions perfectly.

### Requirements

- **Python**: 3.8 or newer
- **Dependencies**: Colorama, Python Standard Library('random', 're') [*The libs are already installed by default*]

#### To install colorama -

```bash
pip install colorama -U # Make sure that your python client or cli is in PATH.
```

### Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/Herbert-byte/bAsIc.git
   cd bAsIc
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Run the program**

   ```bash
   python bAsIc.py
   ```

You should see the ASCII-art logo, then be prompted for your name, followed by:

> `Hello There, I am an bAsIc.`

### How to talk to bAsIc

After the greeting, you can type questions or commands.  
Some examples it understands:

- `How are you`
- `What are you doing`
- `What do you think about right now`
- `What to ask?`
- `/help`
- `/exit`
- `I wish to ask a fibbonaci question`
- `I wish to use a calculator`

Because input is normalized, variations in case and most punctuation are fine.

### Special modes

- **Fibonacci mode**
  - Type: `I wish to ask a fibbonaci question`
  - Then enter how many Fibonacci numbers you want:
    - Example: `5` → outputs `[0, 1, 1, 2, 3]`

- **Calculator mode**
  - Type: `I wish to use a calculator`
  - Then enter a math expression:
    - Example: `2 + 2 * 3` → outputs `Result: 8`

> Note: The calculator uses Python’s expression rules and is intentionally simple.

### Project Structure

- `bAsIc.py` – main script with the chatbot logic.
- `README.md` – project documentation (this file).
- `requirements.txt` – lists Python dependencies (standard-library only for now).

### Contributing

Pull requests are welcome! Some ideas:

- Add more supported questions and responses.
- Improve error handling around user input.
- Turn this into an installable package with a CLI entrypoint.

### LICENSE
The license is not introduced yet, we are choosing the MIT License soon.
