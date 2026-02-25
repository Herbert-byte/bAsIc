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
greet = [
    "  _       _        ___     ",
    " | |__   / \\   ___|_ _|___ ",
    " | '_ \\ / _ \\ / __| |/ __|",
    " | |_) / ___ \\ (__| | (__ ",
    " |_.__/_/   \\_\\___|___\\___|"
]
for line in greet:
    print(line)

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

print("Hello There, I am an bAsIc.")
name = str(input("What's your name? - "))
print("Ok. Your name is", name)


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
            print("I am doing good, thanks for asking. 🤗")
        elif index == 1:
            print("I am chatting with you. 💬")
        elif index == 2:
            print("I am thinking about how to make a better AI than me. 💭")
        elif index == 3:
            print("Say something like", query)
        elif index == 4:
            print("You can ask me things like", query)
        elif index == 5:
            print("Goodbye!")
            break
        elif index == 6:
            user_fib = int(input("Enter the number of Fibonacci numbers to generate: "))
            print(fibonacci(user_fib))
        elif index == 7:
            expr = input("Enter a calculation (for example: 2 + 2 * 3) - ")
            print("Result:", calculate(expr))
        elif index == 8:
            print("My name is bAsIc.")
        elif index == 9:
            print("I was created by Herbert Kumar.")
        elif index == 10:
            print("I can chat with you, calculate expressions, and generate Fibonacci sequences.")
        elif index == 11:
            jokes = [
                "Why did the computer show up at work late? It had a hard drive.",
                "There are 10 kinds of people in the world: those who understand binary and those who don't.",
                "I would tell you a UDP joke, but you might not get it."
            ]
            print(random.choice(jokes))
        elif index == 12:
            now = datetime.now().strftime("%H:%M:%S")
            print("The current time is", now)
        elif index == 13:
            print("Here is a random number between 1 and 100:", random.randint(1, 100))
        elif index == 14:
            compliments = [
                "You are doing great!",
                "You are smarter than you think.",
                "The world is better with you in it, " + name + "."
            ]
            print(random.choice(compliments))
        elif index == 15:
            quotes = [
                "Keep going, you are closer than you think.",
                "Every expert was once a beginner.",
                "Small steps every day lead to big change."
            ]
            print(random.choice(quotes))
    elif userask_normalized == "exit":
        print("Use /exit next time. Bye!")
        break
    else:
        print("I don't understand that question.")
        print("Say something like -", random.choice(query))
