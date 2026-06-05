"""

"""

import random
import re
import time
from datetime import datetime
import sys
import shutil
import tty
import termios

try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    curses = None

IN_IDLE = False
try:
    IN_IDLE = sys.stdin.__class__.__name__ == 'PyShell'
except Exception:
    pass

if IN_IDLE:
    RED = GREEN = YELLOW = CYAN = LIGHT_BLUE = RESET = ""

    class _IdleOut:
        _map = str.maketrans({
            '┌': '+', '─': '-', '┐': '+', '│': '|',
            '├': '+', '┤': '+', '└': '+', '┘': '+',
            '▸': '>', '●': '*', '█': '#', '░': '.',
            '═': '=', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
        })
        def __init__(self, s):
            self._s = s
        def write(self, t):
            t = re.sub(r'\033\[[0-9;?]*[A-Za-z]', '', t)
            t = t.translate(self._map)
            self._s.write(t)
        def flush(self):
            self._s.flush()

    sys.stdout = _IdleOut(sys.stdout)
else:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    LIGHT_BLUE = "\033[94m"
    RESET = "\033[0m"
AI_RESPONSE_DELAY_SECONDS = 1.0

BANNER = [
    " ▄▄                     ▄▄▄▄▄▄      ",
    " █▄      ▄█▀▀█▄        █▀ ██        ",
    " ██      ██  ██           ██        ",
    " ████▄   ██▀▀██   ▄██▀█   ██   ▄███▀",
    " ██ ██ ▄ ██  ██   ▀███▄   ██   ██   ",
   "▄████▀ ▀██▀  ▀█▄██▄▄██▀ ▄▄██▄▄▄▀███▄",
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

def clear_line():
    print("\033[2K", end="\r")

def typewrite(text, delay=0.03, color="", end="\n"):
    for ch in text:
        if color:
            sys.stdout.write(color + ch + RESET)
        else:
            sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def thinking_animation(duration=1.0):
    sys.stdout.write(GREEN + "  thinking" + RESET)
    steps = 5
    for _ in range(steps):
        sys.stdout.write(CYAN + " ●" + RESET)
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def styled_input(prompt="Ask me something"):
    print()
    print(CYAN + " ┌─" + "─" * 38 + "┐" + RESET)
    val = input(CYAN + " │ " + YELLOW + prompt + CYAN + " : " + RESET).strip()
    print(CYAN + " └─" + "─" * 38 + "┘" + RESET)
    return val

def anim_bar(duration=1.5, label=""):
    try:
        cols = shutil.get_terminal_size().columns
    except Exception:
        cols = 80
    bar_width = min(30, cols - 30)
    if bar_width < 5:
        bar_width = 5
    steps = bar_width

    empty = "░" * steps
    clear_line()
    sys.stdout.write(f"{GREEN}[{empty}]{RESET}   0% {label}")
    sys.stdout.flush()
    time.sleep(0.15)

    for i in range(1, steps + 1):
        pct = int((i / steps) * 100)
        filled = "█" * i
        empty = "░" * (steps - i)
        clear_line()
        sys.stdout.write(f"{GREEN}[{filled}{empty}]{RESET} {pct:3d}% {label}")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def boot_splash_and_get_name():
    print("\033[H\033[J", end="")

    cols = shutil.get_terminal_size().columns
    box_w = min(48, cols - 4)

    def draw_border(left, fill, right, color=LIGHT_BLUE):
        for ch in left:
            print(color + ch + RESET, end="", flush=True)
            time.sleep(0.005)
        for ch in fill:
            print(color + ch + RESET, end="", flush=True)
            time.sleep(0.001)
        for ch in right:
            print(color + ch + RESET, end="", flush=True)
            time.sleep(0.005)
        print()

    draw_border("╔", "═" * box_w, "╗")

    for line in BANNER:
        typewrite(line, 0.003, CYAN)

    draw_border("╚", "═" * box_w, "╝")
    print()

    anim_bar(0.8, CYAN + "Initializing bAsIc kernel..." + RESET)
    anim_bar(0.6, CYAN + "Loading conversational modules..." + RESET)
    anim_bar(1.0, CYAN + "bAsIc AI core ready." + RESET)
    print()

    typewrite(" ▸ Hello, I am bAsIc.", 0.04, GREEN)
    print()
    name = input(CYAN + " ▸ What's your name? " + RESET).strip()
    print()
    typewrite(GREEN + f" ▸ Welcome, {name}!" + RESET, 0.03, YELLOW)
    print()
    return name

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

def _wrap_text(text, width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]

def ai_print(*args, **kwargs):
    text = " ".join(str(a) for a in args)
    has_color = "\033" in text
    plain = re.sub(r'\033\[[0-9;]*m', '', text) if has_color else text

    cols = shutil.get_terminal_size().columns
    box_w = min(48, cols - 4)
    cw = box_w - 4

    print()
    print(GREEN + "┌" + "─" * (box_w - 2) + "┐" + RESET)

    if has_color:
        display = plain[:cw]
        pad = cw - len(display)
        sys.stdout.write(GREEN + "│ " + RESET + text + " " * pad + GREEN + " │" + RESET + "\n")
        sys.stdout.flush()
    else:
        for line in _wrap_text(plain, cw):
            pad = cw - len(line)
            sys.stdout.write(GREEN + "│ " + RESET)
            for ch in line:
                sys.stdout.write(GREEN + ch + RESET)
                sys.stdout.flush()
                time.sleep(0.03)
            sys.stdout.write(" " * pad + GREEN + " │" + RESET + "\n")
            sys.stdout.flush()

    print(GREEN + "└" + "─" * (box_w - 2) + "┘" + RESET)
    print()
    time.sleep(AI_RESPONSE_DELAY_SECONDS)

def manual_calculator_mode():
    choice = styled_input("Go to calculator mode? (yes/no)").lower()
    if choice != "yes": return
    try:
        num1 = int(styled_input("Enter the first number"))
        num2 = int(styled_input("Enter the second number"))
        op = styled_input("Enter operation (add, sub, mul, div)").lower()
        if op in ("addition", "add"):
            ai_print(f"Result: {num1 + num2}")
        elif op in ("subtraction", "sub"):
            ai_print(f"Result: {num1 - num2}")
        elif op in ("multiplication", "mul"):
            ai_print(f"Result: {num1 * num2}")
        elif op in ("division", "div"):
            if num2 != 0:
                ai_print(f"Result: {num1 / num2}")
            else:
                ai_print(RED + "Error: Cannot divide by zero!" + RESET)
        else:
            ai_print(RED + "Error: Unknown operation!" + RESET)
    except ValueError:
        ai_print(RED + "Error: Please enter numbers only!" + RESET)

def process_userask(userask_normalized, jokes, kick_out_words):
    if contains_any(userask_normalized, ["hi", "hello"]):
        ai_print("Hello! I'm here to help.")
    elif contains_any(userask_normalized, ["joke", "funny"]):
        ai_print(random.choice(jokes))
    elif contains_any(userask_normalized, ["time"]):
        ai_print(datetime.now().strftime("%H:%M:%S"))
    elif contains_any(userask_normalized, ["name"]):
        ai_print("I am bAsIc!")
    elif contains_any(userask_normalized, ["help"]):
        ai_print("I can help with math, fibonacci, jokes, time, compliments, and more!")
    elif contains_any(userask_normalized, ["calculator", "calc", "+", "-", "*", "/"]):
        manual_calculator_mode()
    elif contains_any(userask_normalized, kick_out_words):
        ai_print(YELLOW + ":(, Very rude!" + RESET)
        ai_print(YELLOW + "Goodbye!" + RESET)
        return True
    elif contains_any(userask_normalized, ["exit", "/exit"]):
        ai_print(YELLOW + "Goodbye!" + RESET)
        return True
    else:
        ai_print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)
    return False

def get_key():
    if IN_IDLE:
        raise RuntimeError("IDLE")
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
        n = styled_input("How many Fibonacci numbers")
        try:
            count = int(n)
            ai_print("Fibonacci sequence: " + str(fibonacci(count)))
        except ValueError:
            ai_print(RED + "Please enter a valid number!" + RESET)
    elif choice == "calc":
        manual_calculator_mode()
    elif choice == "time":
        ai_print(datetime.now().strftime("%H:%M:%S"))
    elif choice == "random":
        ai_print(random.randint(1, 100))
    elif choice == "joke":
        ai_print(random.choice(jokes))
    elif choice == "compliment":
        ai_print(random.choice(compliments))
    elif choice == "inspire":
        ai_print(random.choice(quotes))
    elif choice == "help":
        ai_print("I can perform calculations. I can do basic communication. I also have hidden secrets. I am age friendly.")
    elif choice == "quit" or choice == "exit":
        return True
    return False

CURSES_FAILED = False

if CURSES_AVAILABLE:
    def run_outside_curses(stdscr, fn, *args, **kwargs):
        curses.def_prog_mode()
        curses.endwin()
        try:
            return fn(*args, **kwargs)
        finally:
            curses.reset_prog_mode()
            stdscr.clear()
            stdscr.refresh()

    def init_curses_colors():
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def draw_menu(stdscr, selected_row, options):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        logo_h = len(BANNER)
        box_w = min(50, w - 4)
        box_h = logo_h + len(options) + 4
        start_x = max(0, (w - box_w) // 2)
        start_y = max(0, (h - box_h) // 2)

        if h < box_h + 2 or w < box_w + 4:
            try:
                stdscr.addstr(0, 0, "Terminal too small!")
            except curses.error:
                pass
            stdscr.refresh()
            return

        has_c = curses.has_colors()
        cp_border = curses.color_pair(1) if has_c else 0
        cp_logo = curses.color_pair(1) if has_c else 0
        cp_sel = curses.color_pair(3) | curses.A_BOLD if has_c else curses.A_REVERSE

        try:
            stdscr.addstr(start_y, start_x, "┌" + "─" * (box_w - 2) + "┐", cp_border)

            for i, line in enumerate(BANNER):
                y = start_y + 1 + i
                display = line[:box_w - 4]
                pad = box_w - 4 - len(display)
                stdscr.addstr(y, start_x, "│", cp_border)
                stdscr.addstr(y, start_x + 1, display + " " * pad, cp_logo)
                stdscr.addstr(y, start_x + box_w - 1, "│", cp_border)

            spacer_y = start_y + 1 + logo_h
            stdscr.addstr(spacer_y, start_x, "│", cp_border)
            stdscr.addstr(spacer_y, start_x + box_w - 1, "│", cp_border)

            for idx, (label, _) in enumerate(options):
                y = spacer_y + 1 + idx
                display = label[:box_w - 6] if len(label) > box_w - 6 else label

                if idx == selected_row:
                    stdscr.addstr(y, start_x + 1, " " * (box_w - 2), cp_sel)
                    stdscr.addstr(y, start_x + 2, "▸ " + display, cp_sel)
                    stdscr.addstr(y, start_x, "│", cp_border)
                    stdscr.addstr(y, start_x + box_w - 1, "│", cp_border)
                else:
                    stdscr.addstr(y, start_x, "│", cp_border)
                    stdscr.addstr(y, start_x + 2, "  " + display)
                    stdscr.addstr(y, start_x + box_w - 1, "│", cp_border)

            footer = "↑↓ Navigate  ↵ Select  Q Quit"
            m = box_w - 2 - len(footer)
            fl = m // 2
            fr = m - fl
            stdscr.addstr(start_y + box_h - 1, start_x, "└" + "─" * fl + footer + "─" * fr + "┘", cp_border)
        except curses.error:
            pass

        stdscr.refresh()

    def run_curses_menu(stdscr, options):
        init_curses_colors()
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
            name = run_outside_curses(stdscr, boot_splash_and_get_name)

            jokes = ["Why did the computer show up at work late? It had a hard drive.", "There are 10 kinds of people in the world: those who understand binary and those who don't.", "I would tell you a UDP joke, but you might not get it."]
            compliments = ["You are doing great!", "You are smarter than you think.", "The world is better with you in it, " + name + "."]
            quotes = ["Keep going, you are closer than you think.", "Every expert was once a beginner.", "Small steps every day lead to big change."]
            kick_out_words = ["fuck","motherfucker","matharchod","bitch","dick","lauda","maa ki"]

            while True:
                choice = run_curses_menu(stdscr, MENU_OPTIONS)

                if choice == "quit":
                    break
                elif choice == "type":
                    userask = run_outside_curses(stdscr, styled_input, "Ask me something")
                    userask_normalized = normalize(userask)
                    run_outside_curses(stdscr, thinking_animation, 0.7)
                    should_exit = run_outside_curses(
                        stdscr, process_userask, userask_normalized, jokes, kick_out_words
                    )
                    if should_exit:
                        break
                else:
                    done = run_outside_curses(stdscr, handle_choice, choice, name, jokes, compliments, quotes)
                    if done:
                        break
        except Exception as e:
            CURSES_FAILED = True
            raise e

def text_menu_select(options, jokes, compliments, quotes):
    selected = 0
    while True:
        print("\033[H\033[J", end="")
        print(LIGHT_BLUE + "┌" + "─" * 36 + "┐" + RESET)
        print(LIGHT_BLUE + "│" + " " * 12 + CYAN + "bAsIc Menu" + " " * 12 + LIGHT_BLUE + "│" + RESET)
        print(LIGHT_BLUE + "├" + "─" * 36 + "┤" + RESET)
        for idx, (label, _) in enumerate(options):
            display = label[:34] if len(label) > 34 else label
            pad = 36 - len(display)
            if idx == selected:
                print(GREEN + "│" + " " + "▸ " + display + " " * (pad - 2) + "│" + RESET)
            else:
                print("│" + "  " + display + " " * (pad - 2) + "│")
        print(LIGHT_BLUE + "└" + "─" * 36 + "┘" + RESET)
        print(CYAN + "  ↑↓ Navigate  ↵ Select  Q Quit" + RESET)

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
            ai_print(YELLOW + "Goodbye!" + RESET)
            return
        except Exception as e:
            CURSES_FAILED = True
            try:
                curses.endwin()
            except:
                pass
            ai_print(YELLOW + f"Could not use curses menu. Falling back to text menu..." + RESET)

    name = boot_splash_and_get_name()

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
                userask = styled_input("Ask me something")
                userask_normalized = normalize(userask)
                thinking_animation(0.7)
                should_exit = process_userask(userask_normalized, jokes, kick_out_words)
                if should_exit:
                    return
                continue
            done = handle_choice(choice, name, jokes, compliments, quotes)
            if done:
                ai_print(YELLOW + "Goodbye!" + RESET)
                break
        return

    last_response_type = ""
    while True:
        userask = styled_input("Ask me something")
        userask_normalized = normalize(userask)

        if userask_normalized in context_triggers:
            if last_response_type == "math":
                ai_print(LIGHT_BLUE + "I triggered the calculator because I detected math operators." + RESET)
            elif last_response_type == "success":
                ai_print(LIGHT_BLUE + "Hard work is the only way to reach your goals!" + RESET)
            elif last_response_type == "purpose":
                ai_print(LIGHT_BLUE + "I'm just a bAsIc AI meant to help with simple tasks." + RESET)
            elif last_response_type == "":
                ai_print(LIGHT_BLUE + "I haven't said anything to explain yet!" + RESET)
            elif last_response_type == "continuation":
                ai_print(LIGHT_BLUE + "You were saying something, right?" + RESET)
            else:
                ai_print(LIGHT_BLUE + f"That was a response for my '{last_response_type}' logic branch." + RESET)
            continue

        if contains_any(userask_normalized, kick_out_words):
            ai_print(YELLOW + ":(, Very rude and unapropiate,")
            ai_print(RED + "Initiating kick out")
            break

        if userask_normalized == "/exit" or userask_normalized == "exit":
            ai_print(YELLOW + "Goodbye!" + RESET)
            break
        elif userask_normalized == "/help" or userask_normalized == "help":
            ai_print("I can perform calculations. I can do basic communication. I also have hidden secrets. I am age friendly.")
            continue

        if contains_any(userask_normalized, symbols_to_check):
            last_response_type = "math"
            manual_calculator_mode()
        elif contains_any(userask_normalized, tango_mangle_keywords):
            last_response_type = "tangomangle"
            for _ in range(7): ai_print("Do you want a free chicken nugget")
            ai_print("continued to infinity\n" + YELLOW + "You found a secret and got tangomangled lol" + RESET)
        elif contains_any(userask_normalized, set_of_questions2):
            last_response_type = "help"
            ai_print("Ask whatever you want! If you need help, type '/help'.")
        elif contains_any(userask_normalized, set_of_questions3):
            last_response_type = "success"
            ai_print("By being dedicated and working hard.")
        elif contains_any(userask_normalized, set_of_questions):
            last_response_type = "status"
            ai_print("I am great, I hope you are too!")
        elif contains_any(userask_normalized, set_of_greetings):
            last_response_type = "greeting"
            ai_print("Hello! I'm here to help.")
        elif contains_any(userask_normalized, set_of_purpose):
            last_response_type = "purpose"
            ai_print("I am bAsIc, an AI that answers questions and calculates answers.")
        elif contains_any(userask_normalized, set_of_capabilities):
            last_response_type = "capabilities"
            ai_print("My core strengths are basic communication and arithmetic.")
        elif contains_any(userask_normalized, set_of_feedbackP):
            last_response_type = "feedbackP"
            ai_print(GREEN + ":), I am happy to help." + RESET)
        elif contains_any(userask_normalized, set_of_feedbackN):
            last_response_type = "feedbackN"
            ai_print(RED + ":(, sorry, I am just trying to help." + RESET)
        elif contains_any(userask_normalized, set_of_continuationwords):
            last_response_type = "continuation"
            ai_print(YELLOW + "Yes,?" + RESET)
        elif "joke" in userask_normalized:
            last_response_type = "joke"
            ai_print(LIGHT_BLUE + random.choice(jokes) + RESET)
        elif "time" in userask_normalized:
            last_response_type = "time"
            ai_print(LIGHT_BLUE + datetime.now().strftime("%H:%M:%S") + RESET)
        else:
            last_response_type = "unknown"
            ai_print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)

if __name__ == "__main__":
    main()
