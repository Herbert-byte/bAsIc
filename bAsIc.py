import random
import re
from datetime import datetime

# ANSI color codes
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
    "How are you", "What are you doing", "What do you think about right now",
    "What to ask?", "/help", "/exit", "I wish to ask a Fibonacci question",
    "I wish to use a calculator", "What is your name", "Who created you",
    "What can you do", "Tell me a joke", "What time is it",
    "Give me a random number", "Compliment me", "Inspire me",
]

def normalize(text):
    # Keeps math symbols and forward slashes for /help or /exit
    cleaned = re.sub(r"[^\w\s/+\-*]", "", text)
    return cleaned.strip().lower()

def contains_any(text, symbols):
    text_lower = text.lower()
    for s in symbols:
        keyword = s.lower().strip()
        if not keyword: continue
        if keyword in ["+", "-", "*", "/"]:
            if keyword in text_lower: return True
        elif re.match(r"^[\w\s]+$", keyword):
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, text_lower): return True
        else:
            if keyword in text_lower: return True
    return False

# --- Original Statement Sets ---
symbols_to_check = ["/", "*", "-", "+", "multiply", "divide", "add", "subtract", "plus", "minus"]
set_of_purpose = ["who are you", "what are you", "what do you do", "tell me about yourself", "what is your purpose", "who is this", "help pls", "What kind of AI are you?", "Introduce yourself"]
set_of_greetings = ["hi", "hello", "whats up?", "whats up", "yo!", "hey"]
set_of_questions = ["how are you?", "you good?", "are you well?"]
set_of_questions2 = ["how can i get help", "i need help", "help me", "what should i do?", "what can i ask?"]
set_of_questions3 = ["how can i win", "how to succeed", "how can i do good in life"]
set_of_capabilities = ["what can you do", "what are your capabilities", "what are your strengths", "what are you good at"]
set_of_feedbackP = ["ok","sure","wow","you are good","you are so good","Yes"]
set_of_feedbackN = ["no","nah","bruh","you are bad","you are so bad","eww","No"]
tango_mangle_keywords = ["tangomangle", "do you want a free chicken nugget"]
kick_out_words = ["fuck","motherfucker","matharchod","bitch","dick","lauda","maa ki"]
context_triggers = ["why", "how", "explain", "tell me more"]

def calculate(expression):
    try:
        return eval(expression, {"__builtins__": None}, {})
    except Exception:
        return "I could not understand that calculation."

def fibonacci(n):
    if n <= 0: return []
    elif n == 1: return [0]
    elif n == 2: return [0, 1]
    else:
        seq = [0, 1]
        for i in range(2, n): seq.append(seq[i-1] + seq[i-2])
        return seq

def print_banner():
    for line in BANNER: print(CYAN + line)
    print(RESET, end="")

def manual_calculator_mode():
    choice = input("Action triggered: Go to calculator mode? (yes/no): ").strip().lower()
    if choice != "yes": return
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        op = input("Enter operation (addition, subtraction, multiplication, division): ").strip().lower()
        if op == "addition": print(f"Result: {num1 + num2}")
        elif op == "subtraction": print(f"Result: {num1 - num2}")
        elif op == "multiplication": print(f"Result: {num1 * num2}")
        elif op == "division":
            if num2 != 0: print(f"Result: {num1 / num2}")
            else: print("Error: Cannot divide by zero!")
    except ValueError:
        print("Error: Please enter numbers only!")

def main():
    print_banner()
    print(GREEN + "Hello there, I am bAsIc." + RESET)
    name = input("What's your name? - ").strip()
    print(GREEN + "Okay, your name is " + name + RESET)

    last_response_type = ""

    jokes = ["Why did the computer show up at work late? It had a hard drive.", "There are 10 kinds of people in the world: those who understand binary and those who don't.", "I would tell you a UDP joke, but you might not get it."]
    compliments = ["You are doing great!", "You are smarter than you think.", "The world is better with you in it, " + name + "."]
    quotes = ["Keep going, you are closer than you think.", "Every expert was once a beginner.", "Small steps every day lead to big change."]

    while True:
        userask = input("Ask me something - ")
        userask_normalized = normalize(userask)

        # 1. CONTEXT CHECK
        if userask_normalized in context_triggers:
            if last_response_type == "math":
                print(LIGHT_BLUE + "I triggered the calculator because I detected math operators." + RESET)
            elif last_response_type == "success":
                print(LIGHT_BLUE + "Hard work is the only way to reach your goals!" + RESET)
            elif last_response_type == "purpose":
                print(LIGHT_BLUE + "I'm just a bAsIc AI meant to help with simple tasks." + RESET)
            elif last_response_type == "":
                print(LIGHT_BLUE + "I haven't said anything to explain yet!" + RESET)
            else:
                print(LIGHT_BLUE + f"That was a response for my '{last_response_type}' logic branch." + RESET)
            continue

        # 2. KICK OUT CHECK
        if contains_any(userask_normalized, kick_out_words):
            print(YELLOW + ":(, Very rude and unapropriate,")
            print(RED + "Initiating kick out")
            break

        # 3. EXIT CHECK
        if userask_normalized == "/exit" or userask_normalized == "exit":
            print(YELLOW + "Goodbye!" + RESET)
            break

        # 4. FULL ELIF STATEMENTS (RESTORING ALL RESPONSES)
        if contains_any(userask_normalized, symbols_to_check):
            last_response_type = "math"
            manual_calculator_mode()
        elif contains_any(userask_normalized, tango_mangle_keywords):
            last_response_type = "tangomangle"
            for _ in range(7): print("Do you want a free chicken nugget")
            print("continued to infinity\n" + YELLOW + "You found a secret and got tangomangled lol" + RESET)
        elif contains_any(userask_normalized, set_of_questions2):
            last_response_type = "help"
            print("Ask whatever you want! If you need help, type 'help pls'.")
        elif contains_any(userask_normalized, set_of_questions3):
            last_response_type = "success"
            print("By being dedicated and working hard.")
        elif contains_any(userask_normalized, set_of_questions):
            last_response_type = "status"
            print("I am great, I hope you are too!")
        elif contains_any(userask_normalized, set_of_greetings):
            last_response_type = "greeting"
            print("Hello! I'm here to help.")
        elif contains_any(userask_normalized, set_of_purpose):
            last_response_type = "purpose"
            print("I am bAsIc, an AI that answers questions and calculates answers.") 
        elif contains_any(userask_normalized, set_of_capabilities):
            last_response_type = "capabilities"
            print("My core strengths are basic communication and arithmetic.")
        elif contains_any(userask_normalized, set_of_feedbackP):
            last_response_type = "feedbackP"
            print(":), I am happy to help.")
        elif contains_any(userask_normalized, set_of_feedbackN):
            last_response_type = "feedbackN"
            print(":(, sorry, I am just trying to help.")
        elif "joke" in userask_normalized:
            last_response_type = "joke"
            print(LIGHT_BLUE + random.choice(jokes) + RESET)
        elif "time" in userask_normalized:
            last_response_type = "time"
            print(LIGHT_BLUE + datetime.now().strftime("%H:%M:%S") + RESET)
        else:
            last_response_type = "unknown"
            print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)

if __name__ == "__main__":
    main()
