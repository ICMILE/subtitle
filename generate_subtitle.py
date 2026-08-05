import sys
import os
import re
import math
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog

BASE_DIR = r"E:\miscellaneous\BAT\subtitle"
os.makedirs(BASE_DIR, exist_ok=True)  
DEFAULT_INPUT = os.path.join(BASE_DIR, "input.txt")
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "output.srt")
MODE = "character"
MODE = "typewriter"

INITIAL_DURATION = 0.15
TARGET_DURATION = 0.06
CONVERGENCE_SPEED = 0.8
MIN_DURATION = 0.02
HOLD_DURATION = 0.3

FONT_NAME = "Microsoft YaHei"
FONT_SIZE = 36
PRIMARRY_COLOR = "#FFFFFF"
OUTLINE_COLOR = "#000000"


def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Select Input Text File", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialdir=BASE_DIR
    )
    root.destroy()
    return file_path if file_path else None

def get_lastest_txt_file(directory):
    txt_files = []
    for f in os.listdir(directory):
        if f.lower().endswith('.txt'):
            full_path = os.path.join(directory, f)
            txt_files.append(full_path)
    if not txt_files:
        return None
    txt_files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return txt_files[0]
    
def get_input_output_path():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if not os.path.exists(input_path):
            print(f"Input file '{input_path}' does not exist.")
            input("Press Enter to exit...")
            sys.exit(1)
        base, ext = os.path.splitext(input_path)
        output_path = base + ".srt"
        return input_path, output_path

    lastest = get_lastest_txt_file(BASE_DIR)
    if lastest is None:
        print(f"No .txt files found in '{BASE_DIR}'. Please create an input file.")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"automatically selected the latest .txt file: {os.path.basename(lastest)}")
    base, ext = os.path.splitext(lastest)
    output_path = base + ".srt"
    return lastest, output_path
        
def get_char_duration(index):
    dur = TARGET_DURATION + (INITIAL_DURATION - TARGET_DURATION) * math.exp(-CONVERGENCE_SPEED * index)
    return max(dur, MIN_DURATION)

def split_sentences(text):
    sentences = re.split(r'[。！？；\n]+', text)
    return [s.strip() for s in sentences if s.strip()]

def split_characters(text):
    return list(text)

def format_time(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02},{milliseconds:03}"

def generate_srt_sentence_mode(text):
    sentences = split_sentences(text)
    srt_entries = []
    current_time = 0.0

    for index, sentence in enumerate(sentences):
        duration = get_char_duration(index)
        start_time = format_time(current_time)
        end_time = format_time(current_time + duration)
        srt_entries.append(f"{index + 1}\n{start_time} --> {end_time}\n{sentence}\n")
        current_time += duration

    return "\n".join(srt_entries)

def generate_srt_character_mode(text):
    chars = split_characters(text)
    srt_entries = []
    current_time = 0.0
    char_index = 0

    for ch in chars:
        if ch.strip() == "":
            current_time += MIN_DURATION
            continue

        duration = get_char_duration(char_index)
        start = current_time
        end = current_time + duration
        srt_entries.append(f"{char_index + 1}\n{format_time(start)} --> {format_time(end)}\n{ch}\n")
        current_time = end
        char_index += 1
    
    return "\n".join(srt_entries)

def generate_srt_typewriter_mode(text):

    max_line_length = 24
    duration = 0.3

    sentences = split_sentences(text)
    srt_entries = []
    current_time = 0.0
    entry_counter = 1

    for raw in sentences:
        if not raw:
            continue

        if len(raw) > max_line_length:
            lines = [raw[i:i+max_line_length] for i in range(0, len(raw), max_line_length)]
            display_text = "\n".join(lines)
            for line in lines:
                chars = list(line)
                total_len = len(chars)
                durations = [get_char_duration(i) for i in range(total_len)]


    # for sentence in sentences:
    #     if not sentence:
    #         continue
    #     chars = list(sentence)
    #     total_len = len(chars)
    #     durations = [get_char_duration(i) for i in range(total_len)]

                for idx, ch in enumerate(chars):
                    cumulative = "".join(chars[:idx+1])
                    padded = cumulative + "\u3000" * (total_len - len(cumulative)) 
                    duration = durations[idx]
                    start = current_time
                    end = current_time + duration
                    srt_entries.append(f"{entry_counter}\n{format_time(start)} --> {format_time(end)}\n{padded}\n")
                    current_time = end
                    entry_counter += 1
            continue

        chars = list(raw)
        total_len = len(chars)
        durations = [get_char_duration(i) for i in range(total_len)]

        for idx, ch in enumerate(chars):
            cumulative = "".join(chars[:idx+1])
            padded = cumulative + "\u3000" * (total_len - len(cumulative)) 
            duration = durations[idx]
            start = current_time
            end = current_time + duration
            srt_entries.append(f"{entry_counter}\n{format_time(start)} --> {format_time(end)}\n{padded}\n")
            current_time = end
            entry_counter += 1

    total = entry_counter - 1
    print(f"Total characters processed: {total}")
    return "\n".join(srt_entries)

def main():
    input_file, output_file = get_input_output_path()
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist.")
        print("Please create the input file and add your text.")
        input("Press Enter to exit...")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    if not text.strip():
        print("Input file is empty. Please add some text.")
        input("Press Enter to exit...")
        return

    modes = {
        "sentence": generate_srt_sentence_mode,
        "character": generate_srt_character_mode,
        "typewriter": generate_srt_typewriter_mode
    }

    if MODE not in modes:
        print("Invalid mode. Please choose 'sentence', 'character', or 'typewriter'.")
        input("Press Enter to exit...")
        return

    srt_content = modes[MODE](text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f"Subtitle file saved to '{output_file}'.")
    print("Please input in Davince Resolve through 'File -> Import -> Subtitles'.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
    