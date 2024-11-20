# Define the input string
text = """
The answer is as plain as the nose on your face, or the cream in your coffee, or the vowels in your alphabet. The above paragraph is missing the most common letter in the English language: the letter E.

E is everywhere. In an analysis of all 240,000 entries in the Concise Oxford English Dictionary, OED editors found that the letter E appears in approximately 11% of all words in the common English vocabulary, about 6,000 more words than the runner-up letter, A. What’s more: E is the most commonly struck letter on your keyboard, and the second most popular key after the space bar. It’s one third of the single most-used word in English—“the”—and appears in the most common English noun (“time”), the most common verb (“be”), in ubiquitous pronouns like he, she, me, and we, not to mention tens of thousands of words ending in -ed and -es.

There’s a reason, in other words, that scribes see composing prose without the letter E as one of the ultimate challenges in constrained writing. This hasn’t stopped masochistic wordsmiths from trying. Author Ernest Vincent Wright’s 1939 novel Gadsby, for example, contains some 50,000 words—none of them containing an E—while the 1969 French novel La Disparition has been translated into a dozen different languages, each edition omitting the most common letter in that language. The French and English versions successfully last 300 pages without the letter E; in Spanish, the letter A gets omitted, and in Russian, it’s O.

On the whole, most of the 5 full-time vowels (sorry, “sometimes Y”)  appear more frequently in English than most consonants, with a few exceptions. Anyone who’s spent the evening watching Wheel of Fortune over the years into its 40th season, can tell you the most common consonants—at least, the ones Pat Sajak gives you for free during the final puzzle—are R, S, T L, and N (tellingly, he also throws in the letter E). Oxford’s analysis confirms that Pat is on the money.
"""

# Initialize an empty dictionary to store character frequencies
char_freq = {}

# Iterate over each character in the text
for char in text:
    if char in char_freq:
        char_freq[char] += 1
    else:
        char_freq[char] = 1

# Optionally, sort the dictionary by frequency in descending order
sorted_char_freq = sorted(char_freq.items(), key=lambda item: item[1], reverse=True)

# Print the character frequencies
print("Character Frequency in the Provided Text:\n")
for char, freq in sorted_char_freq:
    # For better readability, represent newline and space characters explicitly
    if char == ' ':
        display_char = "' ' (space)"
    elif char == '\n':
        display_char = "'\\n' (newline)"
    else:
        display_char = f"'{char}'"
    print(f"{display_char}: {freq}")
