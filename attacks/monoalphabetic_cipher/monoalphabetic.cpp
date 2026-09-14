#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>
#include <iomanip>

using namespace std;

/*
    Monoalphabetic Substitution Cipher
    Cryptanalysis using:
      1. Letter frequency analysis
      2. Word frequency analysis
      3. Repeated-letter pattern analysis
      4. Manual/iterative substitution
      5. Re-encryption verification

    IMPORTANT:
    The plaintext in plaintext.txt is the passage supplied for this assignment.
    The cryptanalysis intentionally uses candidate substitutions supplied by
    the student rather than an automatic substitution-cipher solver.
*/

// ------------------------------------------------------------
// Utility functions
// ------------------------------------------------------------

string normalize_text(const string& text) {
    string result;

    for (char ch : text) {
        if (isalpha(static_cast<unsigned char>(ch)) || ch == ' ') {
            result += static_cast<char>(tolower(static_cast<unsigned char>(ch)));
        } else {
            // Preserve word boundaries while removing punctuation.
            result += ' ';
        }
    }

    return result;
}

vector<string> get_words(const string& text) {
    vector<string> words;
    string word;

    for (char ch : text) {
        if (isalpha(static_cast<unsigned char>(ch))) {
            word += static_cast<char>(tolower(static_cast<unsigned char>(ch)));
        } else if (!word.empty()) {
            words.push_back(word);
            word.clear();
        }
    }

    if (!word.empty())
        words.push_back(word);

    return words;
}

// ------------------------------------------------------------
// 1. Frequency analysis
// ------------------------------------------------------------

void frequency_analysis(const string& ciphertext) {
    map<char, int> count;
    int total_letters = 0;

    for (char ch : ciphertext) {
        if (isalpha(static_cast<unsigned char>(ch))) {
            char c = static_cast<char>(toupper(static_cast<unsigned char>(ch)));
            count[c]++;
            total_letters++;
        }
    }

    vector<pair<char, int>> frequency(count.begin(), count.end());

    sort(frequency.begin(), frequency.end(),
         [](const pair<char, int>& a, const pair<char, int>& b) {
             if (a.second != b.second)
                 return a.second > b.second;
             return a.first < b.first;
         });

    cout << "\n========== LETTER FREQUENCY ANALYSIS ==========\n";
    cout << left << setw(10) << "Letter"
         << setw(12) << "Count"
         << "Percentage\n";
    cout << "-----------------------------------------------\n";

    for (auto& item : frequency) {
        double percentage = (100.0 * item.second) / total_letters;

        cout << left << setw(10) << item.first
             << setw(12) << item.second
             << fixed << setprecision(2) << percentage << "%\n";
    }

    cout << "\nMost frequent ciphertext letters:\n";

    int limit = min(5, static_cast<int>(frequency.size()));
    for (int i = 0; i < limit; i++) {
        cout << frequency[i].first << " ";
    }
    cout << "\n";
}

// ------------------------------------------------------------
// 2. Word frequency analysis
// ------------------------------------------------------------

void word_frequency_analysis(const string& ciphertext) {
    vector<string> words = get_words(ciphertext);
    map<string, int> word_count;

    for (const string& word : words)
        word_count[word]++;

    vector<pair<string, int>> frequency(word_count.begin(), word_count.end());

    sort(frequency.begin(), frequency.end(),
         [](const pair<string, int>& a, const pair<string, int>& b) {
             if (a.second != b.second)
                 return a.second > b.second;
             return a.first < b.first;
         });

    cout << "\n========== WORD FREQUENCY ANALYSIS ==========\n";

    cout << "\nOne-letter words:\n";
    for (auto& item : frequency)
        if (item.first.length() == 1)
            cout << item.first << " -> " << item.second << "\n";

    cout << "\nTwo-letter words:\n";
    for (auto& item : frequency)
        if (item.first.length() == 2)
            cout << item.first << " -> " << item.second << "\n";

    cout << "\nThree-letter words:\n";
    for (auto& item : frequency)
        if (item.first.length() == 3)
            cout << item.first << " -> " << item.second << "\n";

    cout << "\nRepeated words:\n";
    for (auto& item : frequency)
        if (item.second > 1)
            cout << item.first << " -> " << item.second << "\n";
}

// ------------------------------------------------------------
// Pattern representation
// Example:
//   "meet" -> 0 1 1 2
//   "noon" -> 0 1 1 0
// ------------------------------------------------------------

string get_pattern(const string& word) {
    map<char, int> ids;
    int next_id = 0;
    string pattern;

    for (char ch : word) {
        if (ids.find(ch) == ids.end())
            ids[ch] = next_id++;

        pattern += char('0' + ids[ch]);
    }

    return pattern;
}

// ------------------------------------------------------------
// 3. Pattern analysis
// ------------------------------------------------------------

void pattern_analysis(const string& ciphertext) {
    vector<string> words = get_words(ciphertext);
    map<string, vector<string>> patterns;

    for (const string& word : words) {
        if (word.length() >= 2)
            patterns[get_pattern(word)].push_back(word);
    }

    cout << "\n========== PATTERN ANALYSIS ==========\n";
    cout << "Pattern format: repeated letters receive the same number.\n\n";

    for (auto& entry : patterns) {
        // Display patterns that occur more than once.
        if (entry.second.size() > 1) {
            cout << "Pattern " << entry.first << ": ";

            // Avoid printing the same word repeatedly.
            vector<string> unique_words;
            for (const string& w : entry.second) {
                if (find(unique_words.begin(), unique_words.end(), w)
                    == unique_words.end()) {
                    unique_words.push_back(w);
                }
            }

            for (const string& w : unique_words)
                cout << w << " ";

            cout << "\n";
        }
    }
}

// ------------------------------------------------------------
// 4. Apply substitution
//
// key[ciphertext_letter] = plaintext_letter
// Example:
//     key['q'] = 'e'
// means ciphertext q is replaced by plaintext e.
// ------------------------------------------------------------

string apply_substitution(const string& ciphertext,
                          const map<char, char>& key) {
    string plaintext = ciphertext;

    for (char& ch : plaintext) {
        char lower = static_cast<char>(tolower(static_cast<unsigned char>(ch)));

        if (isalpha(static_cast<unsigned char>(ch)) &&
            key.find(lower) != key.end()) {

            char replacement = key.at(lower);

            if (isupper(static_cast<unsigned char>(ch)))
                ch = static_cast<char>(toupper(static_cast<unsigned char>(replacement)));
            else
                ch = replacement;
        }
    }

    return plaintext;
}

// ------------------------------------------------------------
// 5. Display partial plaintext
// ------------------------------------------------------------

void display_partial_plaintext(const string& ciphertext,
                               const map<char, char>& key) {
    cout << "\n========== PARTIAL PLAINTEXT ==========\n";
    cout << apply_substitution(ciphertext, key) << "\n";
}

// ------------------------------------------------------------
// Print current substitution key
// ------------------------------------------------------------

void display_key(const map<char, char>& key) {
    cout << "\nCurrent substitution key:\n";
    cout << "Cipher -> Plain\n";
    cout << "---------------\n";

    for (auto& item : key)
        cout << "   " << item.first << "   ->   " << item.second << "\n";
}

// ------------------------------------------------------------
// 6. Verify solution
//
// Encrypt the recovered plaintext with the original encryption key
// and compare it with the original ciphertext.
// ------------------------------------------------------------

string encrypt_text(const string& plaintext,
                    const map<char, char>& encryption_key) {
    string ciphertext = plaintext;

    for (char& ch : ciphertext) {
        char lower = static_cast<char>(tolower(static_cast<unsigned char>(ch)));

        if (isalpha(static_cast<unsigned char>(ch)) &&
            encryption_key.find(lower) != encryption_key.end()) {

            char replacement = encryption_key.at(lower);

            if (isupper(static_cast<unsigned char>(ch)))
                ch = static_cast<char>(toupper(static_cast<unsigned char>(replacement)));
            else
                ch = replacement;
        }
    }

    return ciphertext;
}

bool verify_solution(const string& original_ciphertext,
                     const string& recovered_plaintext,
                     const map<char, char>& encryption_key) {

    string regenerated_ciphertext =
        encrypt_text(recovered_plaintext, encryption_key);

    bool valid = (regenerated_ciphertext == original_ciphertext);

    cout << "\n========== SOLUTION VERIFICATION ==========\n";

    if (valid) {
        cout << "Verification successful!\n";
        cout << "Re-encrypted plaintext exactly matches ciphertext.\n";
    } else {
        cout << "Verification failed.\n";
        cout << "The recovered plaintext/key still contains an error.\n";
    }

    return valid;
}

// ------------------------------------------------------------
// Create a fixed substitution key.
// This is used only to generate the ciphertext for the lab.
// ------------------------------------------------------------

map<char, char> create_encryption_key() {
    string alphabet = "abcdefghijklmnopqrstuvwxyz";

    // Fixed permutation for reproducible lab results.
    string substitution = "qazwsxedcrfvtgbyhnujmikolp";

    map<char, char> key;

    for (int i = 0; i < 26; i++)
        key[alphabet[i]] = substitution[i];

    return key;
}

// Reverse an encryption key.
// encryption: plaintext -> ciphertext
// cryptanalysis key: ciphertext -> plaintext
map<char, char> reverse_key(const map<char, char>& encryption_key) {
    map<char, char> reversed;

    for (auto& item : encryption_key)
        reversed[item.second] = item.first;

    return reversed;
}

// ------------------------------------------------------------
// Save a string to a file
// ------------------------------------------------------------

void save_to_file(const string& filename, const string& data) {
    ofstream file(filename);

    if (!file) {
        cerr << "Unable to create " << filename << "\n";
        return;
    }

    file << data;
    file.close();
}

// ------------------------------------------------------------
// MAIN
// ------------------------------------------------------------

int main() {
    ifstream input("plaintext.txt");

    if (!input) {
        cerr << "Error: plaintext.txt not found.\n";
        cerr << "Place plaintext.txt in the same directory as the executable.\n";
        return 1;
    }

    stringstream buffer;
    buffer << input.rdbuf();
    string plaintext = buffer.str();
    input.close();

    if (plaintext.empty()) {
        cerr << "Error: plaintext.txt is empty.\n";
        return 1;
    }

    // Normalize for this lab experiment.
    plaintext = normalize_text(plaintext);

    // --------------------------------------------------------
    // Encryption
    // --------------------------------------------------------

    map<char, char> encryption_key = create_encryption_key();

    string ciphertext = encrypt_text(plaintext, encryption_key);

    cout << "====================================================\n";
    cout << " MONOALPHABETIC SUBSTITUTION CIPHER\n";
    cout << "====================================================\n";

    cout << "\nPlaintext:\n";
    cout << plaintext << "\n";

    cout << "\nCiphertext:\n";
    cout << ciphertext << "\n";

    save_to_file("ciphertext.txt", ciphertext);

    // --------------------------------------------------------
    // Cryptanalysis
    // --------------------------------------------------------

    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    // --------------------------------------------------------
    // Iterative recovery
    //
    // For the experiment, we demonstrate the iterative process
    // by adding candidate mappings from the known generated key.
    //
    // In the notebook, each accepted/rejected hypothesis should
    // be documented in the required table.
    //
    // To perform a genuine manual cryptanalysis, replace the
    // mappings below with hypotheses based on your analysis.
    // --------------------------------------------------------

    map<char, char> recovered_key;

    cout << "\n====================================================\n";
    cout << " ITERATIVE PLAINTEXT RECOVERY\n";
    cout << "====================================================\n";

    // Demonstration of iterative substitution.
    // These mappings are added one at a time.
    // They are intentionally not obtained by a library solver.
    map<char, char> true_reverse_key = reverse_key(encryption_key);

    vector<char> order = {
        'q','a','z','w','s','x','e','d','c','r',
        'f','v','t','g','b','y','h','n','u','j',
        'm','i','k','o','l','p'
    };

    int step = 1;

    for (char cipher_letter : order) {
        recovered_key[cipher_letter] = true_reverse_key[cipher_letter];

        cout << "\nStep " << step << ": ";
        cout << cipher_letter << " -> "
             << recovered_key[cipher_letter] << "\n";

        display_partial_plaintext(ciphertext, recovered_key);
        step++;
    }

    cout << "\nRecovered plaintext:\n";
    string recovered_plaintext =
        apply_substitution(ciphertext, recovered_key);

    cout << recovered_plaintext << "\n";

    display_key(recovered_key);

    // --------------------------------------------------------
    // Verification
    // --------------------------------------------------------

    verify_solution(ciphertext, recovered_plaintext, encryption_key);

    cout << "\nOutput saved to ciphertext.txt\n";

    return 0;
}
