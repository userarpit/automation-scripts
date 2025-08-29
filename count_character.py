#! python3

import pprint
user_string = input("Enter a string: ")

char_counts = {}
for char in user_string.lower():
    char_counts.setdefault(char, 0)
    char_counts[char] += 1

# pprint.pprint(char_counts)
pprint.pprint(char_counts)