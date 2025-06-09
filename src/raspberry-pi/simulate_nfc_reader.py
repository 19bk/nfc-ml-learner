import json
import os
import pyttsx3

MAP_PATH = "../ml/nfc_word_map.json"

engine = pyttsx3.init()

def pronounce(word):
    print(f"Speaking: {word}")
    engine.say(word)
    engine.runAndWait()

def spell(word):
    spelled = ' '.join(word.upper())
    print(f"Spelling: {spelled}")
    engine.say(spelled)
    engine.runAndWait()

def main():
    with open(MAP_PATH, 'r') as f:
        tag_map = json.load(f)

    tag_id = input("Scan NFC (enter tag ID): ").strip()
    if tag_id in tag_map:
        word = tag_map[tag_id]
        print(f"Found word: {word}")
        pronounce(word)
        spell(word)
    else:
        print("Unknown NFC tag.")

if __name__ == "__main__":
    main()
