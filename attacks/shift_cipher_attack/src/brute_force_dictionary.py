# brute_force_dictionary.py

from shift_cipher import decrypt


def load_dictionary(filename):
    words = set()

    with open(filename, "r") as file:
        for line in file:
            word = line.strip().lower()

            if word != "":
                words.add(word)

    return words


def dictionary_score(text, dictionary):
    words = text.lower().split()

    score = 0

    for word in words:

        # Remove punctuation
        word = word.strip(".,!?;:")

        if word in dictionary:
            score += 1

    return score


def dictionary_attack(ciphertext, dictionary):

    best_key = 0
    best_score = -1
    best_text = ""

    print("\nDictionary Attack")
    print("-----------------")

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = dictionary_score(plaintext, dictionary)

        print("Key:", key, "| Score:", score, "|", plaintext)

        if score > best_score:
            best_score = score
            best_key = key
            best_text = plaintext

    return best_key, best_text, best_score