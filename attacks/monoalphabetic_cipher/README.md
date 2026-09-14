Monoalphabetic Substitution Cipher

Files

monoalphabetic.cpp - C++ implementation

plaintext.txt - supplied Katz & Lindell passage

ciphertext.txt - generated automatically after execution

Compile

Linux:

g++ -std=c++17 monoalphabetic.cpp -o monoalphabetic
./monoalphabetic

Windows MinGW:

g++ -std=c++17 monoalphabetic.cpp -o monoalphabetic.exe
monoalphabetic.exe

Required functions

frequency_analysis()

word_frequency_analysis()

pattern_analysis()

apply_substitution()

display_partial_plaintext()

verify_solution()

Important lab note

The program does not call an automatic substitution-cipher solver. Frequency,
word-frequency and pattern information are displayed so that candidate
substitutions can be proposed and tested.

For the final notebook, document the actual hypotheses tested during your
experiment. For each step record:

Observation

Possible substitution

Substitution tested

Result

Decision

The program currently demonstrates the iterative process using the known
reverse of the fixed key used to generate the ciphertext. For a strict manual
cryptanalysis demonstration, replace the order/mapping section with the
candidate substitutions you derive from the displayed analysis.
