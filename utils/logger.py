from datetime import datetime


LOG_FILE = "cryptolab.log"


def log_menu_choice(option):

    with open(LOG_FILE, "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - {option}\n")