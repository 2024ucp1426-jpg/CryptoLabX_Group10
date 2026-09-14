from collections import Counter, defaultdict

# English letter frequencies
ENGLISH_FREQ = [
    0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020,
    0.061, 0.070, 0.0015, 0.0077, 0.040, 0.024, 0.067,
    0.075, 0.019, 0.00095, 0.060, 0.063, 0.091, 0.028,
    0.0098, 0.024, 0.0015, 0.020, 0.00074
]


# 1. Remove spaces and special characters
def clean_ciphertext(ciphertext):
    result = ""

    for ch in ciphertext:
        if ch.isalpha():
            result += ch.upper()

    return result


# 2. Find repeated patterns
def find_repeated_patterns(ciphertext, min_len=3, max_len=5):

    patterns = defaultdict(list)

    for length in range(min_len, max_len + 1):

        for i in range(len(ciphertext) - length + 1):

            pattern = ciphertext[i:i + length]
            patterns[pattern].append(i)

    # Keep only patterns that occur more than once
    repeated = {}

    for pattern in patterns:
        if len(patterns[pattern]) > 1:
            repeated[pattern] = patterns[pattern]

    return repeated


# 3. Calculate distances between repeated patterns
def calculate_distances(repeated_patterns):

    distances = []

    for pattern in repeated_patterns:

        positions = repeated_patterns[pattern]

        for i in range(len(positions)):

            for j in range(i + 1, len(positions)):

                distance = positions[j] - positions[i]
                distances.append(distance)

    return distances


# 4. Find factors of distances
def find_factors(distances, max_key_length=20):

    factor_count = Counter()

    for distance in distances:

        for factor in range(2, max_key_length + 1):

            if distance % factor == 0:
                factor_count[factor] += 1

    return factor_count


# 5. Kasiski analysis
def kasiski_analysis(ciphertext):

    repeated_patterns = find_repeated_patterns(ciphertext)

    distances = calculate_distances(repeated_patterns)

    factor_count = find_factors(distances)

    # Sort according to number of occurrences
    candidates = [
        length
        for length, count in factor_count.most_common()
    ]

    return candidates


# 6. Calculate Index of Coincidence
def calculate_ic(text):

    n = len(text)

    if n <= 1:
        return 0

    count = Counter(text)

    total = 0

    for value in count.values():
        total += value * (value - 1)

    return total / (n * (n - 1))


# 7. Divide ciphertext into groups
def split_into_groups(ciphertext, key_length):

    groups = []

    for i in range(key_length):
        group = ciphertext[i::key_length]
        groups.append(group)

    return groups


# 8. Frequency analysis
def frequency_analysis(group):

    count = Counter(group)

    frequency = {}

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        frequency[letter] = count[letter]

    return frequency


# 9. Find Caesar shift using Chi-Square
def find_shift(group):

    best_shift = 0
    best_value = float("inf")

    n = len(group)

    if n == 0:
        return 0

    for shift in range(26):

        # Decrypt the group using this shift
        decrypted = ""

        for ch in group:
            value = (ord(ch) - ord('A') - shift) % 26
            decrypted += chr(value + ord('A'))

        count = Counter(decrypted)

        chi_square = 0

        for i in range(26):

            expected = n * ENGLISH_FREQ[i]
            observed = count[chr(i + ord('A'))]

            if expected > 0:
                chi_square += (
                    (observed - expected) ** 2
                ) / expected

        if chi_square < best_value:

            best_value = chi_square
            best_shift = shift

    return best_shift


# 10. Find the complete key
def find_key(groups):

    key = ""

    for group in groups:

        shift = find_shift(group)

        key += chr(shift + ord('A'))

    return key


# 11. Vigenere decryption
def vigenere_decrypt(ciphertext, key):

    plaintext = ""

    for i in range(len(ciphertext)):

        c = ord(ciphertext[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        p = (c - k) % 26

        plaintext += chr(p + ord('A'))

    return plaintext


# 12. Vigenere encryption
def vigenere_encrypt(plaintext, key):

    ciphertext = ""

    for i in range(len(plaintext)):

        p = ord(plaintext[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')

        c = (p + k) % 26

        ciphertext += chr(c + ord('A'))

    return ciphertext


# 13. Verification
def verify(original_ciphertext, encrypted_ciphertext):

    return original_ciphertext == encrypted_ciphertext
