r"""
 _       _        ___
| |__   / \   ___|_ _|___
| '_ \ / _ \ / __|| |/ __|
| |_) / ___ \\__ \| | (__
|_.__/_/   \_\___/___\___|
A basic AI that can answer some basic questions. It is only allowed to be asked few questions that are specific.
By Herbert Kumar
"""

import random
import re
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

greet = [
    "  _       _        ___     ",
    " | |__   / \\   ___|_ _|___ ",
    " | '_ \\ / _ \\ / __| |/ __|",
    " | |_) / ___ \\ (__| | (__ ",
    " |_.__/_/   \\_\\___|___\\___|"
]
for line in greet:
    print(Fore.CYAN + line)
print(Style.RESET_ALL, end="")

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

print(Fore.GREEN + "Hello There, I am an bAsIc." + Style.RESET_ALL)
name = str(input("What's your name? - "))
print(Fore.GREEN + "Ok. Your name is " + name + Style.RESET_ALL)


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
            print(Fore.LIGHTBLUE_EX + "I am doing good, thanks for asking. 🤗" + Style.RESET_ALL)
        elif index == 1:
            print(Fore.LIGHTBLUE_EX + "I am chatting with you. 💬" + Style.RESET_ALL)
        elif index == 2:
            print(Fore.LIGHTBLUE_EX + "I am thinking about how to make a better AI than me. 💭" + Style.RESET_ALL)
        elif index == 3:
            print(Fore.LIGHTBLUE_EX + "Say something like " + str(query) + Style.RESET_ALL)
        elif index == 4:
            print(Fore.LIGHTBLUE_EX + "You can ask me things like " + str(query) + Style.RESET_ALL)
        elif index == 5:
            print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
            break
        elif index == 6:
            user_fib = int(input("Enter the number of Fibonacci numbers to generate: "))
            print(Fore.LIGHTBLUE_EX + str(fibonacci(user_fib)) + Style.RESET_ALL)
        elif index == 7:
            expr = input("Enter a calculation (for example: 2 + 2 * 3) - ")
            print(Fore.LIGHTBLUE_EX + "Result: " + str(calculate(expr)) + Style.RESET_ALL)
        elif index == 8:
            print(Fore.LIGHTBLUE_EX + "My name is bAsIc." + Style.RESET_ALL)
        elif index == 9:
            print(Fore.LIGHTBLUE_EX + "I was created by Herbert Kumar." + Style.RESET_ALL)
        elif index == 10:
            print(Fore.LIGHTBLUE_EX + "I can chat with you, calculate expressions, and generate Fibonacci sequences." + Style.RESET_ALL)
        elif index == 11:
            jokes = [
                "Why did the computer show up at work late? It had a hard drive.",
                "There are 10 kinds of people in the world: those who understand binary and those who don't.",
                "I would tell you a UDP joke, but you might not get it."
            ]
            print(Fore.LIGHTBLUE_EX + random.choice(jokes) + Style.RESET_ALL)
        elif index == 12:
            now = datetime.now().strftime("%H:%M:%S")
            print(Fore.LIGHTBLUE_EX + "The current time is " + now + Style.RESET_ALL)
        elif index == 13:
            n = random.randint(1, 100)
            print(Fore.LIGHTBLUE_EX + "Here is a random number between 1 and 100: " + str(n) + Style.RESET_ALL)
        elif index == 14:
            compliments = [
                "You are doing great!",
                "You are smarter than you think.",
                "The world is better with you in it, " + name + "."
            ]
            print(Fore.LIGHTBLUE_EX + random.choice(compliments) + Style.RESET_ALL)
        elif index == 15:
            quotes = [
                "Keep going, you are closer than you think.",
                "Every expert was once a beginner.",
                "Small steps every day lead to big change."
            ]
            print(Fore.LIGHTBLUE_EX + random.choice(quotes) + Style.RESET_ALL)
    elif userask_normalized == "exit":
        print(Fore.YELLOW + "Use /exit next time. Bye!" + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "I don't understand that question." + Style.RESET_ALL)
        print(Fore.RED + "Say something like - " + str(random.choice(query)) + Style.RESET_ALL)
