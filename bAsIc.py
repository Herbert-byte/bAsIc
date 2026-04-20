import random
import re
from datetime import datetime
import sys
import tty
import termios

try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    curses = None

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

MENU_OPTIONS = [
    ("Ask a question", "type"),
    ("Fibonacci", "fib"),
    ("Calculator", "calc"),
    ("Get time", "time"),
    ("Random number", "random"),
    ("Tell joke", "joke"),
    ("Compliment me", "compliment"),
    ("Inspire me", "inspire"),
    ("/help", "help"),
    ("/exit", "exit"),
]

def normalize(text):
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

def get_key():
    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            seq = ""
            while True:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    seq = ch
                    continue
                if seq == '\x1b' and ch == '[':
                    seq += ch
                    continue
                if seq == '\x1b[':
                    seq += ch
                    return seq + ch
                return ch
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    except termios.error:
        return '\n'

def handle_choice(choice, name, jokes, compliments, quotes):
    last_response_type = ""
    
    if choice == "fib":
        n = input("How many Fibonacci numbers? ")
        try:
            count = int(n)
            print("Fibonacci sequence:", fibonacci(count))
        except ValueError:
            print("Please enter a valid number!")
    elif choice == "calc":
        manual_calculator_mode()
    elif choice == "time":
        print(datetime.now().strftime("%H:%M:%S"))
    elif choice == "random":
        print(random.randint(1, 100))
    elif choice == "joke":
        print(random.choice(jokes))
    elif choice == "compliment":
        print(random.choice(compliments))
    elif choice == "inspire":
        print(random.choice(quotes))
    elif choice == "help":
        print("I can perform calculations by calculator mode.")
        print("I can do basic communication.")
        print("I also have some hidden secrets.")
        print("I am age friendly and prevent bad things.")
    elif choice == "quit" or choice == "exit":
        return True
    return False

CURSES_FAILED = False

if CURSES_AVAILABLE:
    def draw_menu(stdscr, selected_row, options):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        if h < len(options) + 3:
            stdscr.addstr(0, 0, "Terminal too small! Need more rows.")
            stdscr.refresh()
            return
        
        mid_y = h // 2
        start_y = mid_y - len(options) // 2
        
        for idx, (label, _) in enumerate(options):
            y = start_y + idx
            if 0 <= y < h:
                display_label = label[:w-6] if len(label) > w-6 else label
                x = max(1, (w - len(display_label)) // 2)
                
                if idx == selected_row:
                    try:
                        stdscr.addstr(y, x, f"> {display_label} <", curses.A_REVERSE)
                    except curses.error:
                        pass
                else:
                    try:
                        stdscr.addstr(y, x, f"  {display_label}  ")
                    except curses.error:
                        pass
        
        try:
            stdscr.addstr(h - 1, 0, "↑/↓: Navigate | Enter: Select | Q: Quit")
        except curses.error:
            pass
        
        stdscr.refresh()

    def run_curses_menu(stdscr, options):
        curses.curs_set(0)
        stdscr.clear()
        stdscr.nodelay(True)
        stdscr.timeout(100)
        
        selected = 0
        draw_menu(stdscr, selected, options)
        
        while True:
            key = stdscr.getch()
            
            if key == ord('\n') or key == ord(' '):
                return options[selected][1]
            elif key == curses.KEY_UP or key == ord('w'):
                selected = (selected - 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif key == curses.KEY_DOWN or key == ord('s'):
                selected = (selected + 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif key == ord('q') or key == ord('Q') or key == 27:
                return "quit"
            elif key != -1:
                draw_menu(stdscr, selected, options)

    def curses_main(stdscr):
        global CURSES_FAILED
        try:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        except:
            pass
        
        try:
            print_banner()
            print(GREEN + "Hello there, I am bAsIc." + RESET)
            name = input("What's your name? - ").strip()
            print(GREEN + "Okay, your name is " + name + RESET)
            print()

            jokes = ["Why did the computer show up at work late? It had a hard drive.", "There are 10 kinds of people in the world: those who understand binary and those who don't.", "I would tell you a UDP joke, but you might not get it."]
            compliments = ["You are doing great!", "You are smarter than you think.", "The world is better with you in it, " + name + "."]
            quotes = ["Keep going, you are closer than you think.", "Every expert was once a beginner.", "Small steps every day lead to big change."]

            while True:
                choice = run_curses_menu(stdscr, MENU_OPTIONS)
                
                if choice == "quit":
                    break
                elif choice == "type":
                    stdscr.clear()
                    stdscr.nodelay(False)
                    userask = input("Ask me something - ")
                    stdscr.nodelay(True)
                    stdscr.timeout(100)
                else:
                    done = handle_choice(choice, name, jokes, compliments, quotes)
                    if done:
                        break
                
                try:
                    stdscr.nodelay(False)
                    stdscr.addstr(curses.LINES - 1, 0, "Press any key to continue...")
                    stdscr.refresh()
                    stdscr.getch()
                    stdscr.nodelay(True)
                    stdscr.timeout(100)
                except curses.error:
                    pass
        except Exception as e:
            CURSES_FAILED = True
            raise e

def text_menu_select(options, jokes, compliments, quotes):
    selected = 0
    while True:
        print("\033[H\033[J", end="")
        print("\n" + "=" * 30)
        print("        bAsIc Menu")
        print("=" * 30)
        for idx, (label, _) in enumerate(options):
            marker = ">" if idx == selected else " "
            print(f"  {marker} {label}")
        print("=" * 30 + "\n")
        
        if sys.platform != "win32":
            try:
                key = get_key()
            except:
                key = input("Select (1-" + str(len(options)) + ") or q: ")
                if key:
                    if key.lower() == 'q':
                        return "quit"
                    try:
                        sel = int(key) - 1
                        if 0 <= sel < len(options):
                            return options[sel][1]
                    except ValueError:
                        pass
                continue
        else:
            key = input("Select (1-" + str(len(options)) + ") or q: ")
            if key.lower() == 'q':
                return "quit"
            try:
                sel = int(key) - 1
                if 0 <= sel < len(options):
                    return options[sel][1]
            except ValueError:
                pass
            continue
        
        if key == '\n' or key == '':
            return options[selected][1]
        elif key in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            try:
                sel = int(key) - 1
                if 0 <= sel < len(options):
                    return options[sel][1]
            except:
                pass
        elif key == '\x1b[A' or key == 'w':
            selected = (selected - 1) % len(options)
        elif key == '\x1b[B' or key == 's':
            selected = (selected + 1) % len(options)
        elif key == 'q':
            return "quit"

def main():
    global CURSES_FAILED
    
    if CURSES_AVAILABLE and not CURSES_FAILED:
        try:
            curses.wrapper(curses_main)
            print(YELLOW + "Goodbye!" + RESET)
            return
        except Exception as e:
            CURSES_FAILED = True
            try:
                curses.endwin()
            except:
                pass
            print(YELLOW + f"Could not use curses menu: {e}" + RESET)
            print(YELLOW + "Falling back to text menu..." + RESET)
    
    print(GREEN + "Hello there, I am bAsIc." + RESET)
    name = input("What's your name? - ").strip()
    print(GREEN + "Okay, your name is " + name + RESET)

    jokes = ["Why did the computer show up at work late? It had a hard drive.", "There are 10 kinds of people in the world: those who understand binary and those who don't.", "I would tell you a UDP joke, but you might not get it."]
    compliments = ["You are doing great!", "You are smarter than you think.", "The world is better with you in it, " + name + "."]
    quotes = ["Keep going, you are closer than you think.", "Every expert was once a beginner.", "Small steps every day lead to big change."]
    
    symbols_to_check = ["/", "*", "-", "+", "multiply", "divide", "add", "subtract", "plus", "minus","arithmetics","calculator","arithmetic"]
    set_of_purpose = ["who are you", "what are you", "what do you do", "tell me about yourself", "what is your purpose", "who is this", "help pls", "What kind of AI are you?", "Introduce yourself"]
    set_of_greetings = ["hi", "hello", "whats up?", "whats up", "yo!", "hey"]
    set_of_questions = ["how are you?", "you good?", "are you well?"]
    set_of_questions2 = ["how can i get help", "i need help", "help me", "what should i do?", "what can i ask?"]
    set_of_questions3 = ["how can i win", "how to succeed", "how can i do good in life"]
    set_of_capabilities = ["what can you do", "what are your capabilities", "what are your strengths", "what are you good at"]
    set_of_feedbackP = ["ok","sure","wow","you are good","you are so good","Yes","thank you"]
    set_of_feedbackN = ["no","nah","bruh","you are bad","you are so bad","eww","No"]
    tango_mangle_keywords = ["tangomangle", "do you want a free chicken nugget"]
    kick_out_words = ["fuck","motherfucker","matharchod","bitch","dick","lauda","maa ki"]
    context_triggers = ["why", "how", "explain", "tell me more"]
    set_of_continuationwords = ["so","now","also","lets continue"]
    
    print("\nSelect mode: (t)ext menu or (d)irect input [t/d]: ", end="")
    mode = input().strip().lower()
    
    if mode == "t":
        while True:
            choice = text_menu_select(MENU_OPTIONS, jokes, compliments, quotes)
            if choice == "type":
                userask = input("Ask me something - ")
                userask_normalized = normalize(userask)
                
                if contains_any(userask_normalized, ["joke", "funny"]):
                    print(random.choice(jokes))
                elif contains_any(userask_normalized, ["time"]):
                    print(datetime.now().strftime("%H:%M:%S"))
                elif contains_any(userask_normalized, ["name"]):
                    print(f"I am bAsIc!")
                elif contains_any(userask_normalized, ["help"]):
                    print("I can help with math, fibonacci, jokes, time, compliments, and more!")
                elif contains_any(userask_normalized, ["calculator", "calc", "+", "-", "*", "/"]):
                    manual_calculator_mode()
                elif contains_any(userask_normalized, kick_out_words):
                    print(YELLOW + ":(, Very rude!" + RESET)
                    print(YELLOW + "Goodbye!" + RESET)
                    return
                elif contains_any(userask_normalized, ["exit", "/exit"]):
                    print(YELLOW + "Goodbye!" + RESET)
                    return
                else:
                    print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)
                continue
            done = handle_choice(choice, name, jokes, compliments, quotes)
            if done:
                print(YELLOW + "Goodbye!" + RESET)
                break
        return
    
    last_response_type = ""
    while True:
        userask = input("Ask me something - ")
        userask_normalized = normalize(userask)

        if userask_normalized in context_triggers:
            if last_response_type == "math":
                print(LIGHT_BLUE + "I triggered the calculator because I detected math operators." + RESET)
            elif last_response_type == "success":
                print(LIGHT_BLUE + "Hard work is the only way to reach your goals!" + RESET)
            elif last_response_type == "purpose":
                print(LIGHT_BLUE + "I'm just a bAsIc AI meant to help with simple tasks." + RESET)
            elif last_response_type == "":
                print(LIGHT_BLUE + "I haven't said anything to explain yet!" + RESET)
            elif last_response_type == "continuation":
                print(LIGHT_BLUE + "You were saying something, right?" + RESET)
            else:
                print(LIGHT_BLUE + f"That was a response for my '{last_response_type}' logic branch." + RESET)
            continue

        if contains_any(userask_normalized, kick_out_words):
            print(YELLOW + ":(, Very rude and unapropiate,")
            print(RED + "Initiating kick out")
            break

        if userask_normalized == "/exit" or userask_normalized == "exit":
            print(YELLOW + "Goodbye!" + RESET)
            break
        elif userask_normalized == "/help" or userask_normalized == "help":
            print("I can perform calculations by calculator mode.")
            print("I can do basic communication.")
            print("I also have some hidden secrets.")
            print("I am age friendly and prevent bad things.")
            continue

        if contains_any(userask_normalized, symbols_to_check):
            last_response_type = "math"
            manual_calculator_mode()
        elif contains_any(userask_normalized, tango_mangle_keywords):
            last_response_type = "tangomangle"
            for _ in range(7): print("Do you want a free chicken nugget")
            print("continued to infinity\n" + YELLOW + "You found a secret and got tangomangled lol" + RESET)
        elif contains_any(userask_normalized, set_of_questions2):
            last_response_type = "help"
            print("Ask whatever you want! If you need help, type '/help'.")
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
            print(GREEN + ":), I am happy to help." + RESET)
        elif contains_any(userask_normalized, set_of_feedbackN):
            last_response_type = "feedbackN"
            print(RED + ":(, sorry, I am just trying to help." + RESET)
        elif contains_any(userask_normalized, set_of_continuationwords):
            last_response_type = "continuation"
            print(YELLOW + "Yes,?" + RESET)
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