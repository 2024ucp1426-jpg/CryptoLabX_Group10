# main.py

from shift_cipher import encrypt
from brute_force_dictionary import load_dictionary
from brute_force_dictionary import dictionary_attack
from chi_square_attack import chi_square_attack


def main():

    print("====================================")
    print(" Shift Cipher Cryptanalysis")
    print("====================================")

    plaintext = input("\nEnter plaintext: ")
    key = int(input("Enter actual key (0-25): "))

    # Encrypt plaintext
    ciphertext = encrypt(plaintext, key)

    print("\nOriginal Plaintext :", plaintext)
    print("Actual Key         :", key)
    print("Ciphertext         :", ciphertext)

    # Load dictionary
    dictionary = load_dictionary(
        "../dictionary/english_words.txt"
    )

    # Dictionary attack
    dictionary_key, dictionary_text, dictionary_score_value = \
        dictionary_attack(ciphertext, dictionary)

    # Chi-square attack
    chi_key, chi_text, chi_score = \
        chi_square_attack(ciphertext)

    # Final result
    print("\n====================================")
    print(" Final Results")
    print("====================================")

    print("\nActual Key       :", key)

    print("\nDictionary Attack")
    print("Predicted Key    :", dictionary_key)
    print("Decrypted Text   :", dictionary_text)
    print("Dictionary Score :", dictionary_score_value)

    print("\nChi-Square Attack")
    print("Predicted Key    :", chi_key)
    print("Decrypted Text   :", chi_text)
    print("Chi-Square Score :", round(chi_score, 2))

    print("\n====================================")
    print(" Comparison")
    print("====================================")

    if dictionary_key == key:
        print("Dictionary Attack : CORRECT")
    else:
        print("Dictionary Attack : WRONG")

    if chi_key == key:
        print("Chi-Square Attack  : CORRECT")
    else:
        print("Chi-Square Attack  : WRONG")


if __name__ == "__main__":
    main()