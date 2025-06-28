import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from colorama import init, Fore, Style

init(autoreset=True)

url = input("Enter The Target URL e.g (https://example.com): ")

print("")

print_lock = threading.Lock()

def check_directory(folder):
    full_url = url + folder
    try:
        response = requests.get(full_url)
        if response.status_code in [200, 301, 302, 403]:
            with print_lock:
                if response.status_code == 200:
                    color = Fore.GREEN
                elif response.status_code in [301, 302]:
                    color = Fore.YELLOW
                elif response.status_code in [403,404,500]:
                    color = Fore.RED
                else:
                    color = Fore.WHITE
                print(color + f"Directory Found: {full_url} [{response.status_code}]")
        else:
            pass
    except requests.RequestException:
        with print_lock:
            print(Fore.MAGENTA + f"Request failed for {folder}")

# Main thread logic
try:
    with open("r.txt", "r", encoding="UTF-8") as df:
        dict_folder = df.read().splitlines()
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_directory, dict_folder)

except FileNotFoundError:
    print(Fore.RED + "File Not Found!")
    exit()
