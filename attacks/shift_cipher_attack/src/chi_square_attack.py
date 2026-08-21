# chi_square_attack.py

from shift_cipher import decrypt


# English letter frequencies in percentage
english_frequency = {
    'a': 8.167,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.153,
    'k': 0.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.327,
    't': 9.056,
    'u': 2.758,
    'v': 0.978,
    'w': 2.360,
    'x': 0.150,
    'y': 1.974,
    'z': 0.074
}


def chi_square(text):

    # Count only alphabets
    letters = []

    for ch in text.lower():
        if ch.isalpha():
            letters.append(ch)

    total = len(letters)

    if total == 0:
        return float("inf")

    chi = 0

    for letter in english_frequency:

        observed = letters.count(letter)

        expected = (english_frequency[letter] / 100) * total

        if expected > 0:
            chi += ((observed - expected) ** 2) / expected

    return chi


def chi_square_attack(ciphertext):

    best_key = 0
    best_score = float("inf")
    best_text = ""

    print("\nChi-Square Attack")
    print("-----------------")

    for key in range(26):

        plaintext = decrypt(ciphertext, key)

        score = chi_square(plaintext)

        print(
            "Key:", key,
            "| Chi-Square:", round(score, 2),
            "|", plaintext
        )

        if score < best_score:
            best_score = score
            best_key = key
            best_text = plaintext

    return best_key, best_text, best_score