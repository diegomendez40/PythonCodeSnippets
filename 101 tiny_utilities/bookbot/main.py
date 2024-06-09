"""
BOOKBOT
Provides letter counts for different characters for deciphering purposes
Based on a Boot.dev idea

Author: diegomendez40 (Diego Méndez Romero)
Date: 08.06.24
"""

def sort_on(dict):
    return dict["value"]

def main():
    with open("books/frankenstein.txt") as f:
        file_contents = f.read()
    words = file_contents.split()
    word_count = len(words)
    letter_count = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lc_text = file_contents.lower()         # Lower-case for counting letters
    for ch in alphabet:
        letter_count[ch] = 0
    for ch in lc_text:
        if ch in alphabet:
            letter_count[ch] += 1
    char_list = [{"id": key, "value": value} for key, value in letter_count.items()]
    char_list.sort(reverse=True, key=sort_on)

    print("--- Begin report of books/frankenstein.txt ---")
    print(f"{word_count} words found in the document")
    print()
    for ch in char_list:
        letter = ch["id"]
        count = ch["value"]
        print(f"The '{letter}' character was found {count} times")
    print("--- End report ---")


if __name__ == "__main__":
    main()