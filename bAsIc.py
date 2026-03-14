r"""
 _       _        ___
| |__   / \   ___|_ _|___
| '_ \ / _ \ / __|| |/ __|
| |_) / ___ \\__ \| | (__
|_.__/_/   \_\___/___\___|
A basic AI that can answer some basic questions. It is only allowed to be asked few questions that are specific.
By Herbert Kumar (y3ll0what_, whitespc_)
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

greet = [
    "  _       _        ___     ",
    " | |__   / \\   ___|_ _|___ ",
    " | '_ \\ / _ \\ / __| |/ __|",
    " | |_) / ___ \\ (__| | (__ ",
    " |_.__/_/   \\_\\___|___\\___|"
]
for line in greet:
    print(CYAN + line)
print(RESET, end="")

query = [
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
            "Inspire me"
        ]

def normalize(text):
    cleaned = re.sub(r"[^\w\s/]", "", text)
    return cleaned.strip().lower()


query_normalized = [normalize(q) for q in query]


def contains_any(text, symbols):
    """Return True if any string in symbols appears in text (case-insensitive)."""
    for s in symbols:
        if s.lower() in text.lower():
            return True
    return False


symbols_to_check = ["/", "*", "-", "+", "multiply", "divide", "add", "subtract", "plus", "minus"]
set_of_purpose = ["who are you", "what are you", "what do you do", "tell me about yourself", "what is your purpose", "who is this", "help pls", "what can you do"]
set_of_greetings = ["hi", "hello", "whats up?", "whats up", "yo!", "hey"]
set_of_questions = ["how are you?", "you good?", "are you well?"]
set_of_questions2 = ["what should i ask?", "i need help", "how to use"]
set_of_questions3 = ["how can i win", "how to succed", "how can i do good in life"]
Tango_mangle = ["tangomangle", "do you want a free chicken nugget"]

print(GREEN + "Hello There, I am an bAsIc." + RESET)
name = str(input("What's your name? - "))
print(GREEN + "Ok. Your name is " + name + RESET)


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
while True:
    userask = str(input("Ask me something - "))
    userask_normalized = normalize(userask)

    if userask_normalized in query_normalized:
        index = query_normalized.index(userask_normalized)
        if index == 0:
            print(LIGHT_BLUE + "I am doing good, thanks for asking. 🤗" + RESET)
        elif index == 1:
            print(LIGHT_BLUE + "I am chatting with you. 💬" + RESET)
        elif index == 2:
            print(LIGHT_BLUE + "I am thinking about how to make a better AI than me. 💭" + RESET)
        elif index == 3:
            print(LIGHT_BLUE + "Say something like " + str(query) + RESET)
        elif index == 4:
            print(LIGHT_BLUE + "You can ask me things like " + str(query) + RESET)
        elif index == 5:
            print(YELLOW + "Goodbye!" + RESET)
            break
        elif index == 6:
            user_fib = int(input("Enter the number of Fibonacci numbers to generate: "))
            print(LIGHT_BLUE + str(fibonacci(user_fib)) + RESET)
        elif index == 7:
            expr = input("Enter a calculation (for example: 2 + 2 * 3) - ")
            print(LIGHT_BLUE + "Result: " + str(calculate(expr)) + RESET)
        elif index == 8:
            print(LIGHT_BLUE + "My name is bAsIc." + RESET)
        elif index == 9:
            print(LIGHT_BLUE + "I was created by Herbert Kumar." + RESET)
        elif index == 10:
            print(LIGHT_BLUE + "I can chat with you, calculate expressions, and generate Fibonacci sequences." + RESET)
        elif index == 11:
            jokes = [
                "Why did the computer show up at work late? It had a hard drive.",
                "There are 10 kinds of people in the world: those who understand binary and those who don't.",
                "I would tell you a UDP joke, but you might not get it."
            ]
            print(LIGHT_BLUE + random.choice(jokes) + RESET)
        elif index == 12:
            now = datetime.now().strftime("%H:%M:%S")
            print(LIGHT_BLUE + "The current time is " + now + RESET)
        elif index == 13:
            n = random.randint(1, 100)
            print(LIGHT_BLUE + "Here is a random number between 1 and 100: " + str(n) + RESET)
        elif index == 14:
            compliments = [
                "You are doing great!",
                "You are smarter than you think.",
                "The world is better with you in it, " + name + "."
            ]
            print(LIGHT_BLUE + random.choice(compliments) + RESET)
        elif index == 15:
            quotes = [
                "Keep going, you are closer than you think.",
                "Every expert was once a beginner.",
                "Small steps every day lead to big change."
            ]
            print(LIGHT_BLUE + random.choice(quotes) + RESET)
    elif userask_normalized == "exit":
        print(YELLOW + "Use /exit next time. Bye!" + RESET)
        break
    elif contains_any(userask, symbols_to_check):
        QsA = input("Action Triggered: Go to calculator mode? (yes/no): ")
        if QsA.lower() == "yes":
            try:
                num1 = int(input("Enter first number: "))
                num2 = int(input("Enter second number: "))
                op = input("Enter operation (ie addition,subtraction,multiplication,division): ").lower()

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
            except ValueError:
                print("Error: Please enter numbers only!")
    elif contains_any(userask, set_of_questions):
        print("I am Great, Hope you are too!")
    elif contains_any(userask, set_of_greetings):
        print("Hello! I'm here to help.")
    elif contains_any(userask, set_of_purpose):
        print("I am bAsIc AI used to answer question do basic comunication and calculate answer")
    elif contains_any(userask, set_of_questions2):
        print("Ask whatever you want!, If you need help press 'help pls'")
    elif contains_any(userask, set_of_questions3):
        print("by being dedicated (using dedication and working hard)")
    elif contains_any(userask, Tango_mangle):
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("Do you want a free chicken nugget")
        print("continued to infinity")
    else:
        print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)
