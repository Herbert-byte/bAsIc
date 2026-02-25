## bAsIc

A very simple, terminal-based AI chatbot that can respond to a small set of predefined questions, generate Fibonacci sequences, and evaluate basic calculator expressions.

### Features

- **Predefined responses**: Answers to a curated list of questions (e.g. *How are you?*, *What are you doing?*).
- **Fibonacci helper**: Generates the first \(n\) Fibonacci numbers on request.
- **Calculator**: Evaluates basic math expressions like `2 + 2 * 3`.
- **Friendly greeting**: ASCII-art banner and name prompt when you start the program.

### Requirements

- **Python**: 3.8 or newer
- **Dependencies**: Only uses the Python standard library (`random`, `re`). No extra packages required.

### Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/bAsIc.git
   cd bAsIc
   ```

2. **Run the program**

   ```bash
   python bAsIc.py
   ```

3. **Interact**

   When prompted, you can ask questions like:

   - `How are you`
   - `What are you doing`
   - `What do you think about right now`
   - `What to ask?`
   - `/help`
   - `/exit`
   - `I wish to ask a fibbonaci question`
   - `I wish to use a calculator`

   The program normalizes your input, so capitalization and punctuation do not matter much.

### Project Structure

- `bAsIc.py` – main script with the chatbot logic.
- `README.md` – project documentation (this file).
- `requirements.txt` – lists Python dependencies (standard-library only for now).

### Contributing

Pull requests are welcome! Some ideas:

- Add more supported questions and responses.
- Improve error handling around user input.
- Turn this into an installable package with a CLI entrypoint.

### License

Choose a license (for example MIT) and add it as `LICENSE` at the project root.
