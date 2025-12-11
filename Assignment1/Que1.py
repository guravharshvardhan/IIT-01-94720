sentence = input("Enter a sentence: ")

# Number of characters
num_chars = len(sentence)

# Number of words
words = sentence.split()
num_words = len(words)

# Number of vowels
vowels = "aeiouAEIOU"
num_vowels = 0

for ch in sentence:
    if ch in vowels:
        num_vowels += 1

print("Characters:", num_chars)
print("Words:", num_words)
print("Vowels:", num_vowels)

