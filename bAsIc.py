"""

"""

import random
import re
import time
from datetime import datetime
import sys
import shutil
import platform
import os

# --- platform detection ---
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

# --- conditional POSIX imports (tty/termios not available on Windows) ---
if not IS_WINDOWS:
    try:
        import tty
        import termios
        POSIX_TTY_AVAILABLE = True
    except ImportError:
        POSIX_TTY_AVAILABLE = False
        tty = termios = None
else:
    POSIX_TTY_AVAILABLE = False
    tty = termios = None
    try:
        import msvcrt
    except ImportError:
        msvcrt = None

# --- curses: cross-platform with Windows hint ---
CURSES_AVAILABLE = False
CURSES_IMPORT_ERROR = None
try:
    import curses
    # windows-curses provides curses on Windows; curses may succeed but has_colors() false
    CURSES_AVAILABLE = True
except ImportError as e:
    CURSES_IMPORT_ERROR = e
    CURSES_AVAILABLE = False
    curses = None
    if IS_WINDOWS:
        # will be handled in main() with a friendly message
        pass

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

LAST_RESPONSE_TYPE = ""

tango_mangle_keywords = ["tangomangle", "do you want a free chicken nugget"]
context_triggers = ["why", "how", "explain", "tell me more"]

# Merged routing table: (keywords, response, tag)
# Plain responses only — colors applied by process_userask/handle_choice
BASE_QUERY = [
    (["hi", "hello", "hey"],                          "Hello! I'm here to help!", "greeting"),
    (["how are you", "you good?", "are you well?"],    "I am great, I hope you are too!", "status"),
    (["what are you doing", "think about"],             "Just here, ready to help you!", "status"),
    (["what to ask", "what can i ask", "how can i get help", "i need help", "help me", "what should i do?"], "Ask whatever you want! If you need help, type '/help'.", "help"),
    (["who are you", "what is your name", "who created you", "what are you", "tell me about yourself", "what is your purpose"], "I am bAsIc, an AI that answers questions and calculates answers.", "purpose"),
    (["what can you do", "what are your capabilities", "what are your strengths", "what are you good at"], "My core strengths are basic communication and arithmetic.", "capabilities"),
    (["help"],                                           "I can perform calculations. I can do basic communication. I also have hidden secrets. I am age friendly.", "help"),
    (["joke", "funny"],                                 "__joke__", "joke"),
    (["time"],                                           "__time__", "time"),
    (["random number", "random"],                        "__random__", "random"),
    (["compliment"],                                     "__compliment__", "compliment"),
    (["inspire", "quote"],                               "__inspire__", "inspire"),
    (["fibonacci", "fib"],                               "__fibonacci__", "fibonacci"),
    (["calculator", "calc", "+", "-", "*", "/", "multiply", "divide", "add", "subtract", "plus", "minus", "arithmetics", "arithmetic"], "__calculator__", "math"),
    (["/exit", "exit"],                                  "__exit__", "exit"),
    (["so", "now", "also", "lets continue"],           "Yes,?", "continuation"),
    (["ok", "sure", "wow", "you are good", "you are so good", "yes", "thank you"], ":), I am happy to help.", "feedbackP"),
    (["no", "nah", "bruh", "you are bad", "you are so bad", "eww"], ":(, sorry, I am just trying to help.", "feedbackN"),
    (["how can i win", "how to succeed", "how can i do good in life"], "By being dedicated and working hard.", "success"),
    (["tangomangle", "do you want a free chicken nugget"], "__tango__", "tangomangle"),
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
    if name:
        typewrite(GREEN + f" ▸ Welcome, {name}!" + RESET, 0.03, YELLOW)
    else:
        name = "friend"
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

def process_userask(userask_normalized, jokes, kick_out_words, compliments=None, quotes=None):
    global LAST_RESPONSE_TYPE
    if compliments is None:
        compliments = ["You are doing great!"]
    if quotes is None:
        quotes = ["Keep going!"]

    # context trigger — explain previous response (uses LAST_RESPONSE_TYPE)
    if userask_normalized in context_triggers:
        if LAST_RESPONSE_TYPE == "math":
            ai_print(LIGHT_BLUE + "I triggered the calculator because I detected math operators." + RESET)
        elif LAST_RESPONSE_TYPE == "success":
            ai_print(LIGHT_BLUE + "Hard work is the only way to reach your goals!" + RESET)
        elif LAST_RESPONSE_TYPE == "purpose":
            ai_print(LIGHT_BLUE + "I'm just a bAsIc AI meant to help with simple tasks." + RESET)
        elif LAST_RESPONSE_TYPE == "":
            ai_print(LIGHT_BLUE + "I haven't said anything to explain yet!" + RESET)
        elif LAST_RESPONSE_TYPE == "continuation":
            ai_print(LIGHT_BLUE + "You were saying something, right?" + RESET)
        else:
            ai_print(LIGHT_BLUE + f"That was a response for my '{LAST_RESPONSE_TYPE}' logic branch." + RESET)
        return False

    if contains_any(userask_normalized, kick_out_words):
        ai_print(YELLOW + ":(, Very rude!" + RESET)
        ai_print(YELLOW + "Goodbye!" + RESET)
        LAST_RESPONSE_TYPE = "kick"
        return True

    for keywords, response, tag in BASE_QUERY:
        if contains_any(userask_normalized, keywords):
            LAST_RESPONSE_TYPE = tag
            if response == "__exit__":
                ai_print(YELLOW + "Goodbye!" + RESET)
                return True
            elif response == "__joke__":
                ai_print(LIGHT_BLUE + random.choice(jokes) + RESET)
            elif response == "__time__":
                ai_print(LIGHT_BLUE + datetime.now().strftime("%H:%M:%S") + RESET)
            elif response == "__random__":
                ai_print(random.randint(1, 100))
            elif response == "__compliment__":
                ai_print(random.choice(compliments))
            elif response == "__inspire__":
                ai_print(random.choice(quotes))
            elif response == "__tango__":
                for _ in range(7): ai_print("Do you want a free chicken nugget")
                ai_print("continued to infinity\n" + YELLOW + "You found a secret and got tangomangled lol" + RESET)
            elif response == "__fibonacci__":
                n = styled_input("How many Fibonacci numbers")
                try:
                    count = int(n)
                    ai_print("Fibonacci sequence: " + str(fibonacci(count)))
                except ValueError:
                    ai_print(RED + "Please enter a valid number!" + RESET)
            elif response == "__calculator__":
                manual_calculator_mode()
            else:
                # apply contextual coloring for feedback/continuation/success
                if tag == "continuation":
                    ai_print(YELLOW + response + RESET)
                elif tag == "feedbackP":
                    ai_print(GREEN + response + RESET)
                elif tag == "feedbackN":
                    ai_print(RED + response + RESET)
                else:
                    ai_print(response)
            return False

    LAST_RESPONSE_TYPE = "unknown"
    ai_print(RED + "I'm not sure how to do that yet, but I'm listening!" + RESET)
    return False

def get_key():
    if IN_IDLE:
        raise RuntimeError("IDLE")
    if IS_WINDOWS:
        # Windows: use msvcrt.getch / getwch
        try:
            import msvcrt
            ch = msvcrt.getch()
            # handle extended keys (arrows) -> msvcrt returns b'\xe0' or b'\x00' + second byte
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                mapping = {b'H': '\x1b[A', b'P': '\x1b[B', b'K': '\x1b[D', b'M': '\x1b[C'}
                return mapping.get(ch2, '')
            try:
                decoded = ch.decode('utf-8', errors='ignore')
            except Exception:
                decoded = ''
            if decoded == '\r':
                return '\n'
            if decoded == '\x1b':
                return '\x1b'
            return decoded
        except Exception:
            return '\n'
    # POSIX path
    if not POSIX_TTY_AVAILABLE:
        return '\n'
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
    except (termios.error, OSError, AttributeError):
        return '\n'

def handle_choice(choice, name, jokes, compliments, quotes):
    global LAST_RESPONSE_TYPE
    if choice == "fib":
        LAST_RESPONSE_TYPE = "fibonacci"
        n = styled_input("How many Fibonacci numbers")
        try:
            count = int(n)
            ai_print("Fibonacci sequence: " + str(fibonacci(count)))
        except ValueError:
            ai_print(RED + "Please enter a valid number!" + RESET)
    elif choice == "calc":
        LAST_RESPONSE_TYPE = "math"
        manual_calculator_mode()
    elif choice == "time":
        LAST_RESPONSE_TYPE = "time"
        ai_print(datetime.now().strftime("%H:%M:%S"))
    elif choice == "random":
        LAST_RESPONSE_TYPE = "random"
        ai_print(random.randint(1, 100))
    elif choice == "joke":
        LAST_RESPONSE_TYPE = "joke"
        ai_print(random.choice(jokes))
    elif choice == "compliment":
        LAST_RESPONSE_TYPE = "compliment"
        ai_print(random.choice(compliments))
    elif choice == "inspire":
        LAST_RESPONSE_TYPE = "inspire"
        ai_print(random.choice(quotes))
    elif choice == "help":
        LAST_RESPONSE_TYPE = "help"
        ai_print("I can perform calculations. I can do basic communication. I also have hidden secrets. I am age friendly.")
    elif choice == "quit" or choice == "exit":
        LAST_RESPONSE_TYPE = "exit"
        return True
    return False

CURSES_FAILED = False

# --- curses helpers (only defined if curses available) ---
if CURSES_AVAILABLE:
    def run_outside_curses(stdscr, fn, *args, **kwargs):
        curses.def_prog_mode()
        curses.endwin()
        try:
            return fn(*args, **kwargs)
        finally:
            curses.reset_prog_mode()
            # macOS needs explicit refresh after reset
            try:
                stdscr.clear()
                stdscr.refresh()
            except curses.error:
                pass

    def init_curses_colors():
        if not curses.has_colors():
            return
        curses.start_color()
        # macOS transparency + Windows fallback: use_default_colors if available
        try:
            curses.use_default_colors()
            has_default = True
        except curses.error:
            has_default = False
        bg = -1 if has_default else curses.COLOR_BLACK
        # pair 1: border / logo cyan
        try: curses.init_pair(1, curses.COLOR_CYAN, bg)
        except curses.error: pass
        # pair 2: green text
        try: curses.init_pair(2, curses.COLOR_GREEN, bg)
        except curses.error: pass
        # pair 3: selected (white on blue)
        try: curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        except curses.error:
            try: curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
            except curses.error: pass
        # pair 4: yellow accent
        try: curses.init_pair(4, curses.COLOR_YELLOW, bg)
        except curses.error: pass
        # pair 5: dim / footer
        try: curses.init_pair(5, curses.COLOR_BLACK, bg)
        except curses.error: pass
        # pair 6: red for errors
        try: curses.init_pair(6, curses.COLOR_RED, bg)
        except curses.error: pass

    def _curses_color(pair):
        if curses.has_colors():
            try:
                return curses.color_pair(pair)
            except curses.error:
                return 0
        return 0

    def curses_input(stdscr, prompt, y, x, width=32, mask=None):
        """Curses-native single-line input with prompt. Returns stripped string."""
        curses.echo()
        curses.curs_set(1)
        try:
            stdscr.addstr(y, x, prompt, _curses_color(4) | curses.A_BOLD)
            stdscr.refresh()
            # draw input field
            field_x = x + len(prompt) + 1
            max_w = min(width, stdscr.getmaxyx()[1] - field_x - 2)
            stdscr.addstr(y, field_x, " " * max_w, _curses_color(2))
            stdscr.move(y, field_x)
            stdscr.refresh()
            # use getstr with window
            win = curses.newwin(1, max_w, y, field_x)
            win.bkgd(' ', _curses_color(2))
            win.refresh()
            curses.curs_set(1)
            s = ""
            try:
                # getstr blocks; allow 256 bytes
                raw = win.getstr(0, 0, max_w - 1)
                s = raw.decode(sys.getdefaultencoding(), errors='ignore') if isinstance(raw, bytes) else str(raw)
            except curses.error:
                s = ""
            return s.strip()
        finally:
            curses.noecho()
            try: curses.curs_set(0)
            except curses.error: pass

    def curses_splash_animation(stdscr):
        """Animated splash inside curses: banner typewriter + progress bars."""
        h, w = stdscr.getmaxyx()
        init_curses_colors()
        stdscr.clear()
        try: curses.curs_set(0)
        except curses.error: pass

        box_w = min(56, w - 4)
        box_h = len(BANNER) + 10
        start_x = max(0, (w - box_w)//2)
        start_y = max(0, (h - box_h)//2)

        # border colors
        cp_border = _curses_color(1)
        cp_logo = _curses_color(1) | curses.A_BOLD
        cp_green = _curses_color(2)
        cp_yellow = _curses_color(4)

        def safe_add(y, x, txt, attr=0):
            try:
                if 0 <= y < h and 0 <= x < w:
                    # clip to window width
                    clip = txt[: max(0, w - x - 1)]
                    stdscr.addstr(y, x, clip, attr)
            except curses.error:
                pass

        # draw outer box top
        safe_add(start_y, start_x, "╔" + "═"*(box_w-2) + "╗", cp_border)
        # banner with typewriter per line
        for i, line in enumerate(BANNER):
            y = start_y + 1 + i
            safe_add(y, start_x, "│", cp_border)
            safe_add(y, start_x + box_w -1, "│", cp_border)
            # centered banner line
            display = line[:box_w-4]
            pad = (box_w - 2 - len(display))//2
            # typewriter effect per char
            for ci, ch in enumerate(display):
                safe_add(y, start_x + 1 + pad + ci, ch, cp_logo)
                stdscr.refresh()
                time.sleep(0.006 if not IS_WINDOWS else 0.004)
            # small delay per line
            time.sleep(0.06)

        # bottom border of banner section
        bn_bot = start_y + 1 + len(BANNER)
        safe_add(bn_bot, start_x, "╠" + "═"*(box_w-2) + "╣", cp_border)

        # animated bars (curses version)
        labels = [
            ("Initializing bAsIc kernel...", 0.9),
            ("Loading conversational modules...", 0.7),
            ("bAsIc AI core ready.", 1.0),
        ]
        bar_y = bn_bot + 1
        bar_w = min(28, box_w - 12)
        for label, dur in labels:
            if bar_y >= start_y + box_h -2: break
            safe_add(bar_y, start_x, "│", cp_border)
            safe_add(bar_y, start_x+box_w-1, "│", cp_border)
            # label truncated
            lab = label[:box_w-6]
            safe_add(bar_y, start_x+2, lab, cp_green)
            bar_y += 1
            safe_add(bar_y, start_x, "│", cp_border)
            safe_add(bar_y, start_x+box_w-1, "│", cp_border)
            # bar area
            bar_x = start_x + 2
            steps = bar_w
            for s in range(steps+1):
                pct = int(s/steps*100)
                filled = "█"*s
                empty = "░"*(steps-s)
                bar_txt = f"[{filled}{empty}] {pct:3d}%"
                # ensure not overflow
                if len(bar_txt) > box_w-4:
                    bar_txt = bar_txt[:box_w-4]
                safe_add(bar_y, bar_x, " "*(box_w-4), 0)
                safe_add(bar_y, bar_x, bar_txt, cp_green)
                safe_add(bar_y, start_x+box_w-1, "│", cp_border)
                stdscr.refresh()
                time.sleep(dur/steps)
            bar_y += 1
            time.sleep(0.12)

        # footer border
        safe_add(start_y+box_h-1, start_x, "╚" + "═"*(box_w-2) + "╝", cp_border)
        # version / os hint centered in footer
        os_tag = "Windows" if IS_WINDOWS else ("macOS" if IS_MACOS else "Linux")
        footer_txt = f" {os_tag} • bAsIc v1.1 • curses "
        fx = start_x + max(1, (box_w - len(footer_txt))//2)
        safe_add(start_y+box_h-1, fx, footer_txt, cp_yellow | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.45)

    def draw_menu(stdscr, selected_row, options):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        # handle tiny terminal
        if h < 14 or w < 40:
            try:
                msg = "Terminal too small — resize to 40×14"
                stdscr.addstr(h//2, max(0, (w-len(msg))//2), msg, _curses_color(6) | curses.A_BOLD)
                stdscr.addstr(h//2+1, max(0, (w-22)//2), "Press Q to quit", _curses_color(4))
            except curses.error:
                pass
            stdscr.refresh()
            return

        logo_h = len(BANNER)
        # revamped: more padding, title area, numbered hints
        box_w = min(62, w - 4)
        box_h = logo_h + len(options) + 6
        start_x = max(0, (w - box_w) // 2)
        start_y = max(0, (h - box_h) // 2)

        has_c = curses.has_colors()
        cp_border = _curses_color(1)
        cp_logo = _curses_color(1) | (curses.A_BOLD if has_c else 0)
        cp_sel = _curses_color(3) | curses.A_BOLD
        cp_dim = _curses_color(5) | (curses.A_DIM if has_c else 0)
        cp_accent = _curses_color(4) | curses.A_BOLD
        cp_footer = _curses_color(1)

        try:
            # --- top border with centered title ---
            title = " ◆ bAsIc ◆ "
            safe_title = title[:box_w-6]
            left_len = (box_w - 2 - len(safe_title))//2
            right_len = box_w - 2 - len(safe_title) - left_len
            stdscr.addstr(start_y, start_x, "╔" + "═"*left_len, cp_border)
            stdscr.addstr(start_y, start_x+1+left_len, safe_title, cp_accent)
            stdscr.addstr(start_y, start_x+1+left_len+len(safe_title), "═"*right_len + "╗", cp_border)

            # --- banner ---
            for i, line in enumerate(BANNER):
                y = start_y + 1 + i
                display = line[:box_w - 4]
                pad = (box_w - 2 - len(display))//2
                stdscr.addstr(y, start_x, "│", cp_border)
                stdscr.addstr(y, start_x + 1 + pad, display, cp_logo)
                stdscr.addstr(y, start_x + box_w - 1, "│", cp_border)

            # --- separator with subtitle ---
            sep_y = start_y + 1 + logo_h
            stdscr.addstr(sep_y, start_x, "╠", cp_border)
            stdscr.addstr(sep_y, start_x+1, "─"*(box_w-2), cp_border)
            stdscr.addstr(sep_y, start_x+box_w-1, "╣", cp_border)
            # subtitle centered
            sub = "— interactive menu —"
            sub_x = start_x + (box_w - len(sub))//2
            stdscr.addstr(sep_y, sub_x, sub, cp_dim)

            # --- options with numbers ---
            for idx, (label, _) in enumerate(options):
                y = sep_y + 1 + idx
                # number hint
                num_hint = f"{idx+1:>2}."
                display = label[:box_w - 10] if len(label) > box_w - 10 else label
                if idx == selected_row:
                    # selected row full highlight
                    stdscr.addstr(y, start_x, "│", cp_border)
                    stdscr.addstr(y, start_x+1, " "*(box_w-2), cp_sel)
                    # number
                    stdscr.addstr(y, start_x+2, num_hint, cp_sel | curses.A_BOLD)
                    stdscr.addstr(y, start_x+5, "▸ " + display, cp_sel)
                    # right arrow
                    try: stdscr.addstr(y, start_x+box_w-3, "◂", cp_sel)
                    except curses.error: pass
                    stdscr.addstr(y, start_x+box_w-1, "│", cp_border)
                else:
                    stdscr.addstr(y, start_x, "│", cp_border)
                    stdscr.addstr(y, start_x+2, num_hint, cp_dim)
                    stdscr.addstr(y, start_x+5, "  " + display, 0)
                    stdscr.addstr(y, start_x+box_w-1, "│", cp_border)

            # --- footer with key legend and OS ---
            foot_y = sep_y + 1 + len(options)
            stdscr.addstr(foot_y, start_x, "├", cp_border)
            stdscr.addstr(foot_y, start_x+1, "─"*(box_w-2), cp_border)
            stdscr.addstr(foot_y, start_x+box_w-1, "┤", cp_border)

            legend = " ↑↓/W S  ↵ Enter  1-9 Jump  Q Quit "
            # handle narrow
            if len(legend) > box_w - 2:
                legend = " ↑↓  ↵  Q "
            lx = start_x + (box_w - len(legend))//2
            stdscr.addstr(foot_y+1, start_x, "│", cp_border)
            stdscr.addstr(foot_y+1, lx, legend, cp_footer | curses.A_DIM)
            stdscr.addstr(foot_y+1, start_x+box_w-1, "│", cp_border)

            # bottom border with OS tag
            os_tag = "WIN" if IS_WINDOWS else ("macOS" if IS_MACOS else "LINUX")
            bottom = f"╚{'═'*(box_w-2)}╝"
            stdscr.addstr(foot_y+2, start_x, bottom, cp_border)
            tag_txt = f" {os_tag} "
            tx = start_x + box_w - len(tag_txt) - 3
            if tx > start_x:
                stdscr.addstr(foot_y+2, tx, tag_txt, cp_accent)

            # hint line below box
            hint = "Tip: type number to jump • Esc to quit"
            if foot_y+3 < h:
                hx = max(0, (w - len(hint))//2)
                try: stdscr.addstr(foot_y+3, hx, hint, cp_dim)
                except curses.error: pass

        except curses.error:
            pass
        stdscr.refresh()

    def run_curses_menu(stdscr, options):
        init_curses_colors()
        try: curses.curs_set(0)
        except curses.error: pass
        stdscr.clear()
        stdscr.keypad(True)
        # Use blocking wait but handle resize
        selected = 0
        draw_menu(stdscr, selected, options)
        while True:
            try:
                key = stdscr.getch()
            except curses.error:
                key = -1
            if key in (curses.KEY_RESIZE, curses.KEY_MAX):
                draw_menu(stdscr, selected, options)
                continue
            if key in (10, 13, curses.KEY_ENTER, 32):  # Enter / Space
                return options[selected][1]
            elif key in (curses.KEY_UP,):
                selected = (selected - 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif key in (curses.KEY_DOWN,):
                selected = (selected + 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif key in (27,):  # ESC
                # need to distinguish ESC vs arrow prefix; simple: quit
                return "quit"
            elif key == ord('q') or key == ord('Q'):
                return "quit"
            elif key == ord('w') or key == ord('W'):
                selected = (selected - 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif key == ord('s') or key == ord('S'):
                selected = (selected + 1) % len(options)
                draw_menu(stdscr, selected, options)
            elif ord('1') <= key <= ord('9'):
                idx = key - ord('1')
                if 0 <= idx < len(options):
                    return options[idx][1]
            elif key == ord('0'):
                # 0 jumps to last (usually /exit)
                if len(options) >= 10:
                    return options[9][1]
            elif key != -1:
                # ignore other keys but redraw to keep responsive
                pass

    def curses_main(stdscr):
        global CURSES_FAILED
        try:
            # --- revamped splash inside curses ---
            curses_splash_animation(stdscr)
            # --- name prompt inside curses ---
            h, w = stdscr.getmaxyx()
            # clear and show prompt
            stdscr.clear()
            box_w = min(56, w-4)
            sx = max(0, (w-box_w)//2)
            sy = max(0, h//2 -2)
            try:
                stdscr.addstr(sy, sx, "╔" + "═"*(box_w-2) + "╗", _curses_color(1))
                stdscr.addstr(sy+1, sx, "│", _curses_color(1))
                stdscr.addstr(sy+1, sx+box_w-1, "│", _curses_color(1))
                stdscr.addstr(sy+1, sx+2, "▸ Hello, I am bAsIc.", _curses_color(2) | curses.A_BOLD)
                stdscr.addstr(sy+2, sx, "╚" + "═"*(box_w-2) + "╝", _curses_color(1))
                stdscr.refresh()
            except curses.error:
                pass
            name = curses_input(stdscr, "▸ What's your name?", sy+4, sx, width=box_w-4)
            if not name:
                name = "friend"
            # welcome
            try:
                stdscr.addstr(sy+5, sx, f" Welcome, {name}! ".center(box_w), _curses_color(4) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(0.7)
            except curses.error:
                pass

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
                        stdscr, process_userask, userask_normalized, jokes, kick_out_words, compliments, quotes
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
        # OS-aware header
        os_label = "WIN" if IS_WINDOWS else ("macOS" if IS_MACOS else "LINUX")
        print(LIGHT_BLUE + "┌" + "─" * 36 + "┐" + RESET)
        print(LIGHT_BLUE + "│" + " " * 10 + CYAN + f"bAsIc Menu [{os_label}]" + " " * (12 - len(os_label)) + LIGHT_BLUE + "│" + RESET)
        print(LIGHT_BLUE + "├" + "─" * 36 + "┤" + RESET)
        for idx, (label, _) in enumerate(options):
            display = label[:34] if len(label) > 34 else label
            pad = 36 - len(display)
            if idx == selected:
                print(GREEN + "│" + " " + "▸ " + display + " " * (pad - 2) + "│" + RESET)
            else:
                print("│" + "  " + display + " " * (pad - 2) + "│")
        print(LIGHT_BLUE + "└" + "─" * 36 + "┘" + RESET)
        print(CYAN + "  ↑↓/W S Navigate  ↵ Select  Q Quit  1-9 Jump" + RESET)
        if IS_WINDOWS and not CURSES_AVAILABLE:
            print(YELLOW + "  (Install windows-curses for full menu: pip install windows-curses)" + RESET)

        if IS_WINDOWS:
            # Windows: msvcrt arrow handling or fallback to input
            try:
                import msvcrt
                # try msvcrt path via get_key
                key = get_key()
            except Exception:
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
            if sys.platform != "win32":
                try:
                    key = get_key()
                except Exception:
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

        if key == '\n' or key == '' or key == '\r':
            return options[selected][1]
        elif key in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            try:
                sel = int(key) - 1
                if key == '0':
                    sel = 9
                if 0 <= sel < len(options):
                    return options[sel][1]
            except:
                pass
        elif key == '\x1b[A' or key.lower() == 'w':
            selected = (selected - 1) % len(options)
        elif key == '\x1b[B' or key.lower() == 's':
            selected = (selected + 1) % len(options)
        elif key.lower() == 'q' or key == '\x1b':
            return "quit"

def main():
    global CURSES_FAILED

    if CURSES_AVAILABLE and not CURSES_FAILED:
        # macOS: ensure TERM is set for curses
        if IS_MACOS and not os.environ.get("TERM"):
            os.environ["TERM"] = "xterm-256color"
        try:
            curses.wrapper(curses_main)
            ai_print(YELLOW + "Goodbye!" + RESET)
            return
        except curses.error as e:
            CURSES_FAILED = True
            try:
                curses.endwin()
            except:
                pass
            msg = str(e)
            if IS_WINDOWS and ("nocbreak" in msg or "cbreak" in msg):
                ai_print(YELLOW + "Curses unavailable on this Windows terminal. Using text menu..." + RESET)
            elif "cbreak" in msg or "nocbreak" in msg:
                ai_print(YELLOW + f"No TTY for curses ({msg}). Falling back to text menu..." + RESET)
            else:
                ai_print(YELLOW + f"Could not use curses menu ({msg}). Falling back to text menu..." + RESET)
        except Exception as e:
            CURSES_FAILED = True
            try:
                curses.endwin()
            except:
                pass
            ai_print(YELLOW + f"Could not use curses menu. Falling back to text menu... ({e})" + RESET)
    else:
        if IS_WINDOWS and CURSES_IMPORT_ERROR is not None:
            ai_print(YELLOW + "Tip: for full Windows menu install windows-curses: pip install windows-curses" + RESET)

    name = boot_splash_and_get_name()

    jokes = ["Why did the computer show up at work late? It had a hard drive.", "There are 10 kinds of people in the world: those who understand binary and those who don't.", "I would tell you a UDP joke, but you might not get it."]
    compliments = ["You are doing great!", "You are smarter than you think.", "The world is better with you in it, " + name + "."]
    quotes = ["Keep going, you are closer than you think.", "Every expert was once a beginner.", "Small steps every day lead to big change."]

    # all query routing now lives in BASE_QUERY + process_userask (merged)
    kick_out_words = ["fuck","motherfucker","matharchod","bitch","dick","lauda","maa ki"]

    print("\nSelect mode: (t)ext menu or (d)irect input [t/d]: ", end="")
    try:
        mode = input().strip().lower()
    except EOFError:
        mode = "d"

    if mode == "t":
        while True:
            choice = text_menu_select(MENU_OPTIONS, jokes, compliments, quotes)
            if choice == "type":
                userask = styled_input("Ask me something")
                userask_normalized = normalize(userask)
                thinking_animation(0.7)
                should_exit = process_userask(userask_normalized, jokes, kick_out_words, compliments, quotes)
                if should_exit:
                    return
                continue
            done = handle_choice(choice, name, jokes, compliments, quotes)
            if done:
                ai_print(YELLOW + "Goodbye!" + RESET)
                break
        return

    # direct-input mode now delegates entirely to the merged BASE_QUERY + process_userask
    while True:
        userask = styled_input("Ask me something")
        userask_normalized = normalize(userask)
        should_exit = process_userask(userask_normalized, jokes, kick_out_words, compliments, quotes)
        if should_exit:
            break

if __name__ == "__main__":
    main()
