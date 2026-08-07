import os
from analysis.file_analysis import analyze_file
from utils.logger import log_menu_choice


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER = os.path.join(BASE_DIR, "datasets")

def menu():
    while True:
        print("\n==============================")
        print("      CryptoLabX Toolkit")
        print("==============================")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze Dataset")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            log_menu_choice("Encrypt")
            print("\nComing Soon...")

        elif choice == "2":
            log_menu_choice("Decrypt")
            print("\nComing Soon...")

        elif choice == "3":
            log_menu_choice("Attack")
            print("\nComing Soon...")

        elif choice == "4":
            log_menu_choice("Analyze Dataset")

            filename = input("Enter filename: ")
            filepath = os.path.join(DATASET_FOLDER, filename)

            if os.path.exists(filepath):
                analyze_file(filepath)
            else:
                print("File not found.")

        elif choice == "5":
            log_menu_choice("Exit")
            print("\nThank you for using CryptoLabX.")
            break

        else:
            print("Invalid Choice.")


if __name__ == "__main__":
    menu()