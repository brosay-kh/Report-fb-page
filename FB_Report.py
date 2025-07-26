import requests
import time
import os
from colorama import Fore, init


init(autoreset=True)


os.system("cls" if os.name == "nt" else "clear")


print(Fore.YELLOW + "==============================================")
print(Fore.GREEN + "        REPORT PAGE DOG SIAM        ")
print(Fore.YELLOW + "==============================================\n")

print(Fore.RED + "toolនេះបង្កើតឡើងសម្រាប់វៃpageសៀម")
print("create by Bunsay\n")


fb_url = input(Fore.YELLOW + "[+] Enter FacebookPage URL to reports: ").strip()
repeat_count = input(Fore.CYAN + "[+] How many times to report? (default 1): ").strip()
repeat_count = int(repeat_count) if repeat_count.isdigit() and int(repeat_count) > 0 else 1

delay = input(Fore.CYAN + "[+] Delay between reports in seconds (default 5s): ").strip()
delay = float(delay) if delay.replace(".", "").isdigit() else 5.0


url = 'https://m.facebook.com/help/contact/209046679279097'


data = {
    'crt-url': FB_url,
    'cf_age': "less than 9 years",
    'submit': 'submit'
}

print(Fore.MAGENTA + f"\n[+] Starting report loop ({repeat_count}x every {delay}s)...\n")

success = 0
for i in range(repeat_count):
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(Fore.GREEN + f"[✓] Report {i+1} sent successfully.")
            success += 1
        else:
            print(Fore.RED + f"[✗] Report {i+1} failed. Status: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"[!] Error on report {i+1}: {e}")
    if i < repeat_count - 1:
        time.sleep(delay)

print(Fore.BLUE + f"\n[✔] Reporting complete. {success}/{repeat_count} reports sent.")
print(Fore.GREEN + "Thanks for used this tool to reports page news thai. 🌍")
