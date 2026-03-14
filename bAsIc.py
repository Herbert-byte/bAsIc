r"""
 _       _        ___
| |__   / \   ___|_ _|___
| '_ \ / _ \ / __|| |/ __|
| |_) / ___ \\__ \| | (__
|_.__/_/   \_\___/___\___|
A basic AI that can answer some basic questions. It is only allowed to be asked a few specific questions.
By Herbert Kumar & Akshaj Tiwari(y3ll0what_, whitespc_,Aks-pro171Git)
"""

import random
import re
from datetime import datetime

# ANSI color codes (no external dependencies)
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
LIGHT_BLUE = "\033[94m"
RESET = "\033[0m"

BANNER = [
    "  _       _        ___     ",
    " | |__   / \\   ___|_ _|___ ",
    " | '_ \\ / _ \\ / __| |/ __|",
    " | |_) / ___ \\ (__| | (__ ",
    " |_.__/_/   \\_\\___|___\\___|",
]

BASE_QUERY = [
    "How are you",
    "What are you doing",
    "What do you think about right now",
    "What to ask?",
    "/help",
    "/exit",
    "I wish to ask a fibbonaci question",
    "I wish to use a calculator",
    "What is your name",
    "Who created you",
    "What can you do",
    "Tell me a joke",
    "What time is it",
    "Give me a random number",
    "Compliment me",
    "Inspire me",
]

def normalize(text):
    cleaned = re.sub(r"[^\w\s/]", "", text)
    return cleaned.strip().lower()


def contains_any(text, symbols):
    """Return True if any string in symbols appears in text.

    Matching is case-insensitive and works correctly whether `text` is
    normalized (lowercased/punctuation-stripped) or raw user input.
    """
    text_lower = text.lower()
    return any(s.lower() in text_lower for s in symbols)


symbols_to_check = ["/", "*", "-", "+", "multiply", "divide", "add", "subtract", "plus", "minus"]
set_of_purpose = [
    "who are you",
    "what are you",
    "what do you do",
    "tell me about yourself",
    "what is your purpose",
    "who is this",
    "help pls",
    "what can you do",
    "What kind of AI are you?",
    "Introduce yourself",
]
set_of_greetings = ["hi", "hello", "whats up?", "whats up", "yo!", "hey"]
set_of_questions = ["how are you?", "you good?", "are you well?"]
set_of_questions2 = ["what should i ask you?", "i need help", "how to use"]
set_of_questions3 = ["how can i win", "how to succed", "how can i do good in life"]
tango_mangle_keywords = ["tangomangle", "do you want a free chicken nugget"]
set_of_capabilities = ["What are you best at?","What should I use you for?","Give me some use cases for this AI","Why would I use you instead of a search engine?","Show me your skill set."]

# Normalized versions of several keyword sets.
# These are used for case-insensitive (and punctuation-insensitive) matching.
normalized_set_of_purpose = [normalize(s) for s in set_of_purpose]
normalized_set_of_greetings = [normalize(s) for s in set_of_greetings]
normalized_set_of_questions = [normalize(s) for s in set_of_questions]
normalized_set_of_questions2 = [normalize(s) for s in set_of_questions2]
normalized_set_of_questions3 = [normalize(s) for s in set_of_questions3]
normalized_tango_mangle_keywords = [normalize(s) for s in tango_mangle_keywords]
normalized_set_of_capabilities = [normalize(s) for s in set_of_capabilities]


def unique_preserve_order(items):
    seen = set()
    out = []
    for item in items:
        key = normalize(item)
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


query = unique_preserve_order(
    BASE_QUERY
    + set_of_purpose
    + set_of_greetings
    + set_of_questions
    + set_of_questions2
    + set_of_questions3
    + set_of_capabilities
    # Avoid math operators that normalize to "" (e.g. "+", "*")
    + [s for s in symbols_to_check if normalize(s)]
)

query_normalized = {normalize(q) for q in query}

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except Exception:
        return "I could not understand that calculation."


def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        seq = [0, 1]
        for i in range(2, n):
            next_value = seq[i-1] + seq[i-2]
            seq.append(next_value)
        return seq

def print_banner():
    for line in BANNER:
        print(CYAN + line)
    print(RESET, end="")


def manual_calculator_mode():
    choice = input("Action triggered: Go to calculator mode? (yes/no): ").strip().lower()
    if choice != "yes":
        return

    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
    except ValueError:
        print("Error: Please enter numbers only!")
        return

    op = input("Enter operation (e.g. addition, subtraction, multiplication, division): ").strip().lower()
    if op == "addition":
        print(f"Result: {num1 + num2}")
    elif op == "subtraction":
        print(f"Result: {num1 - num2}")
    elif op == "multiplication":
        print(f"Result: {num1 * num2}")
    elif op == "division":
        if num2 != 0:
            print(f"Result: {num1 / num2}")
        else:
            print("Error: Cannot divide by zero!")


def main():
    print_banner()

    print(GREEN + "Hello there, I am bAsIc." + RESET)
    name = input("What's your name? - ").strip()
    print(GREEN + "Okay, your name is " + name + RESET)

    jokes = [
        "Why did the computer show up at work late? It had a hard drive.",
        "There are 10 kinds of people in the world: those who understand binary and those who don't.",
        "I would tell you a UDP joke, but you might not get it.",
    ]
    compliments = [
        "You are doing great!",
        "You are smarter than you think.",
        "The world is better with you in it, " + name + ".",
    ]
    quotes = [
        "Keep going, you are closer than you think.",
        "Every expert was once a beginner.",
        "Small steps every day lead to big change.",
    ]

    command_handlers = {
        normalize("How are you"): lambda: print(LIGHT_BLUE + "I am doing well, thanks for asking. 🤗" + RESET),
        normalize("What are you doing"): lambda: print(LIGHT_BLUE + "I am chatting with you. 💬" + RESET),
        normalize("What do you think about right now"): lambda: print(
            LIGHT_BLUE + "I am thinking about how to make a better AI than me. 💭" + RESET
        ),
        normalize("What to ask?"): lambda: print(LIGHT_BLUE + "Say something like " + str(query) + RESET),
        normalize("/help"): lambda: print(LIGHT_BLUE + "You can ask me things like " + str(query) + RESET),
        normalize("/exit"): None,  # handled in-loop
        normalize("I wish to ask a fibbonaci question"): None,  # handled in-loop
        normalize("I wish to use a calculator"): None,  # handled in-loop
        normalize("What is your name"): lambda: print(LIGHT_BLUE + "My name is bAsIc." + RESET),
        normalize("Who created you"): lambda: print(LIGHT_BLUE + "I was created by Herbert Kumar." + RESET),
        normalize("What can you do"): lambda: print(
            LIGHT_BLUE + "I can chat with you, calculate expressions, and generate Fibonacci sequences." + RESET
        ),
        normalize("Tell me a joke"): lambda: print(LIGHT_BLUE + random.choice(jokes) + RESET),
        normalize("What time is it"): lambda: print(
            LIGHT_BLUE + "The current time is " + datetime.now().strftime("%H:%M:%S") + RESET
        ),
        normalize("Give me a random number"): lambda: print(
            LIGHT_BLUE + "Here is a random number between 1 and 100: " + str(random.randint(1, 100)) + RESET
        ),
        normalize("Compliment me"): lambda: print(LIGHT_BLUE + random.choice(compliments) + RESET),
        normalize("Inspire me"): lambda: print(LIGHT_BLUE + random.choice(quotes) + RESET),
    }

    while True:
        userask = input("Ask me something - ")
        userask_normalized = normalize(userask)

        if userask_normalized in query_normalized:
            if userask_normalized == normalize("/exit"):
                print(YELLOW + "Goodbye!" + RESET)
                break
            if userask_normalized == normalize("I wish to ask a fibbonaci question"):
                try:
                    user_fib = int(input("Enter the number of Fibonacci numbers to generate: "))
                except ValueError:
                    print(RED + "Please enter a valid number." + RESET)
                    continue
                print(LIGHT_BLUE + str(fibonacci(user_fib)) + RESET)
                continue
            if userask_normalized == normalize("I wish to use a calculator"):
                expr = input("Enter a calculation (for example: 2 + 2 * 3) - ")
                print(LIGHT_BLUE + "Result: " + str(calculate(expr)) + RESET)
                continue

            handler = command_handlers.get(userask_normalized)
            if handler:
                handler()
                continue

        if userask_normalized == "exit":
            print(YELLOW + "Use /exit next time. Bye!" + RESET)
            break
        if contains_any(userask_normalized, symbols_to_check):
            manual_calculator_mode()
        elif contains_any(userask_normalized, normalized_set_of_questions):
            print("I am great, I hope you are too!")
        elif contains_any(userask_normalized, normalized_set_of_greetings):
            print("Hello! I'm here to help.")
        elif contains_any(userask_normalized, normalized_set_of_purpose):
            print("I am bAsIc, an AI that answers questions, has basic conversations, and calculates answers.")
        elif contains_any(userask_normalized, normalized_set_of_questions2):
            print("Ask whatever you want! If you need help, type 'help pls'.")
        elif contains_any(userask_normalized, normalized_set_of_questions3):
            print("By being dedicated and working hard.")
        elif contains_any(userask_normalized, normalized_tango_mangle_keywords):
            for _ in range(7):
                print("Do you want a free chicken nugget")
            print("continued to infinity")
            print(YELLOW + "You found a secret and got tangomangled lol" + RESET)
        elif contains_any(userask_normalized, normalized_set_of_capabilities):
            print("My core strengths are basic communication, giving fibonacci, and answering basic arithmatic equations questions.")
        else:
            print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)


if __name__ == "__main__":
    main()
