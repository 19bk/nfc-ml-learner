#!/usr/bin/env python3
"""
Terminal demo simulation of the NFC-ML-Learner device.
Simulates: NFC tap -> word lookup -> speak -> spell -> listen -> feedback
No hardware or API keys required.
"""

import json
import sys
import time
import random

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BG_GREEN = "\033[42m"
BG_CYAN = "\033[46m"

def slow_print(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    print()
    print(f"{BOLD}{CYAN}{'=' * 52}{RESET}")
    print(f"{BOLD}{CYAN}   NFC-ML-Learner  |  Edge ML Vocabulary Device{RESET}")
    print(f"{BOLD}{CYAN}   For rural Kenya & refugee camp classrooms{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 52}{RESET}")
    print(f"{DIM}   All speech recognition runs offline on-device{RESET}")
    print()
    time.sleep(1.0)

def simulate_card_tap(tag_id, word):
    print(f"{DIM}-------------------------------------------{RESET}")
    time.sleep(0.5)
    slow_print(f"{YELLOW}[NFC]{RESET}  Card detected: tag {BOLD}{tag_id}{RESET}", 0.02)
    time.sleep(0.3)
    slow_print(f"{CYAN}[MAP]{RESET}  Lookup: {tag_id} -> \"{BOLD}{word}{RESET}\"", 0.02)
    time.sleep(0.4)

def simulate_speak(word):
    slow_print(f"{GREEN}[TTS]{RESET}  Speaking: \"{word}\"", 0.02)
    time.sleep(0.6)
    spelling = "  ".join(letter.upper() for letter in word)
    slow_print(f"{GREEN}[TTS]{RESET}  Spelling: {BOLD}{spelling}{RESET}", 0.03)
    time.sleep(0.5)

def simulate_listen(word):
    slow_print(f"{MAGENTA}[MIC]{RESET}  Listening for \"{word}\"...", 0.02)
    time.sleep(0.4)
    for i in range(3):
        bars = "+" * random.randint(3, 12)
        sys.stdout.write(f"\r{MAGENTA}[MIC]{RESET}  Audio: |{bars:<12}|")
        sys.stdout.flush()
        time.sleep(0.3)
    print()
    time.sleep(0.2)

def simulate_match(word):
    slow_print(f"{MAGENTA}[ML] {RESET}  Edge model processing...", 0.02)
    time.sleep(0.4)
    print(f"{BG_GREEN}{BOLD}  MATCH  {RESET} Keyword detected: \"{word}\"  confidence: 0.94")
    time.sleep(0.3)
    slow_print(f"{GREEN}[TTS]{RESET}  \"Great job!\"", 0.02)
    time.sleep(0.5)

def run_demo():
    print_banner()

    with open("src/ml/nfc_word_map.json", "r") as f:
        word_map = json.load(f)

    demo_cards = [("nfc_001", "lion"), ("nfc_003", "elephant"), ("nfc_005", "monkey")]

    for tag_id, word in demo_cards:
        simulate_card_tap(tag_id, word)
        simulate_speak(word)
        simulate_listen(word)
        simulate_match(word)
        print()
        time.sleep(0.6)

    print(f"{DIM}-------------------------------------------{RESET}")
    print(f"{BOLD}Session complete. 3 words practised offline.{RESET}")
    print(f"{DIM}Log saved to data/session_log.csv{RESET}")
    print()

if __name__ == "__main__":
    run_demo()
