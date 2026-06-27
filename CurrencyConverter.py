# /* API: https://www.jsdelivr.com/package/npm/@fawazahmed0/currency-api by Fawaz Ahmed */

from decimal import Decimal
from pathlib import Path
import json
import requests
import socket
import os
import pkgutil

#print("__file__ =", __file__)
#print("cwd =", Path.cwd())

def check_file_existence(path):
    file_path = Path(path)
    if file_path.is_file():
        return True
    else:
        return False


def check_requests(url, headers):
    response = requests.get(url, headers=headers)
    if response.ok:
        return True
    else:
        return False


def check_connection():
    REMOTE_SERVER = "one.one.one.one"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass
    return False


def obtain_json(url, headers, file_name):
    request = requests.get(url, headers=headers)
    json_dict = request.json()
    json_idented = json.dumps(json_dict, indent=4)

    ScriptDir = Path(__file__).resolve().parent
    json_path = ScriptDir / "rates" / file_name
    json_path.parent.mkdir(parents=True, exist_ok=True)

    filehandler = open(json_path, 'w', encoding="utf-8")
    filehandler.write(json_idented)
    filehandler.close()
    


def read_json(file_name):
    #filehandler = open(f"rates/{file_name}.json", 'r', encoding="utf-8")
    #content = filehandler.read()
    #filehandler.close()
    script_dir = Path(__file__).resolve().parent
    json_path = script_dir / "rates" / f"{file_name}.json"
    
    with open(json_path, "r", encoding="utf-8") as filehandler:
        content = filehandler.read()
    python_obj = json.JSONDecoder().decode(content)
    return python_obj


def print_help(currency_list):
    print("List of currency codes with their names that are supported:")
    currency_codes = list(currency_list.keys())
    currency_names = list(currency_list.values())

    entries = len(currency_codes)
    column_amount = 4
    table = [[] for _ in range(column_amount)]
    row_amount = int(entries / column_amount) + (1 if entries % column_amount != 0 else 0)

    for i in range(column_amount):
        for j in range(row_amount):
            try:
                text = f"{currency_codes[j + (row_amount*i)].upper() :<5} = {currency_names[j + (row_amount*i)] if currency_names[j + (row_amount*i)] != "" else "Unknown Name"}"
                table[i].append(text)
            except IndexError:
                table[i].append("")

    for i in range(row_amount):
        print(f"{table[0][i]:<40}  {table[1][i]:<40}  {table[2][i]:<40}  {table[3][i]}")

def search(list, base_currency_code,dict_key):
    for key in list[base_currency_code]:
        if key == dict_key:
            return list[base_currency_code][key]


def alternative_route(start_currency_amount, start_currency_code, end_currency_code):
    ScriptDir = Path(__file__).resolve().parent
    path = ScriptDir / "rates"
    directory_path = Path(path)
    file_names = [file.name for file in directory_path.iterdir() if file.is_file()]

    if "currency_codes.json" in file_names:
        file_names.remove("currency_codes.json")
    else:
        return None

    if file_names:
        base_rate_json = (file_names[0])[:-5]
        base_currency_code = (file_names[0])[:-5]
    else:
        print("[ERROR] No rates.json are found for any conversion. Please connect to the internet to retrieve conversion rates.")
        return None

    base_rate_list = read_json(base_rate_json)
    for key in base_rate_list[base_currency_code]:
        if key == start_currency_code:
            rate_1 = Decimal(str(base_rate_list[base_currency_code][key]))
    for key in base_rate_list[base_currency_code]:
        if key == end_currency_code:
            rate_2 = Decimal(str(base_rate_list[base_currency_code][key]))

    conversion_results = start_currency_amount * (rate_2 / rate_1)
    return conversion_results

rates_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/000.json"
currency_codes_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
fallback_1 = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
fallback_2 = "https://latest.currency-api.pages.dev/v1/currencies.json"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'}

network_flag = check_connection()
if network_flag:
    if check_requests(currency_codes_url, headers):
        rates_url_temp = rates_url.replace("000", "eur")
        obtain_json(rates_url_temp, headers, "eur.json")
        obtain_json(currency_codes_url, headers, "currency_codes.json")
        currency_code_list = read_json("currency_codes")
    elif check_requests(fallback_1, headers):
        rates_url_temp = rates_url.replace("000", "eur.json")
        obtain_json(rates_url_temp, headers, f"eur.json")
        obtain_json(fallback_1, headers, "currency_codes.json")
        currency_code_list = read_json("currency_codes")
    elif check_requests(fallback_2, headers):
        rates_url_temp = rates_url.replace("000", "eur.json")
        obtain_json(rates_url_temp, headers, f"eur.json")
        obtain_json(fallback_2, headers, "currency_codes.json")
        currency_code_list = read_json("currency_codes")
    else:
        network_flag = False
        if check_file_existence(f"rates/currency_codes.json"):
            currency_code_list = read_json("currency_codes")
        else:
            print("[ERROR] No currency_codes.json found. Please connect to internet to retrieve currency codes.")
            input("\nPress Enter to exit.")
            exit()
else:
    if check_file_existence(f"rates/currency_codes.json"):
        currency_code_list = read_json("currency_codes")
    else:
        print("[ERROR] No currency_codes.json found. Please connect to internet to retrieve currency codes.")
        input("\nPress Enter to exit.")
        exit()

currency_code_list = read_json("currency_codes")
print_help(currency_code_list)

while True:
    start_currency = input("\nEnter the starting currency code: ").lower()
    if start_currency not in currency_code_list:
        print("[ERROR] Invalid starting currency code. Please try again.")
        continue
    break

while True:
    end_currency = input("\nEnter the ending currency code: ").lower()
    if end_currency not in currency_code_list:
        print("[ERROR] Invalid ending currency code. Please try again.")
        continue
    break

start_currency_amount = Decimal(input("\nEnter the starting currency amount: "))

if network_flag:
    rates_url_temp = rates_url.replace("000", start_currency)
    obtain_json(rates_url_temp, headers, f"{start_currency}.json")
    rates_dict = read_json(start_currency)
elif check_file_existence(f"rates/{start_currency}.json"):
    rates_dict = read_json(start_currency)
else:
    print("[WARNING] No rates.json found for the desired conversion. Trying again by using other rates.json...\n")
    result = alternative_route(start_currency_amount, start_currency, end_currency)
    if not result:
        input("\nPress Enter to exit.")
        exit()
    else:
        print(
            f"\nConversion result: {start_currency_amount} {start_currency.upper()} to {result} {end_currency.upper()}")
        input("\nPress Enter to exit...")
        exit()

rate = Decimal(str(rates_dict[start_currency][end_currency]))

conversion_results = rate * start_currency_amount
print(f"\nConversion result: {start_currency_amount} {start_currency.upper()} to {conversion_results} {end_currency.upper()}")


input("\nPress Enter to exit...")

