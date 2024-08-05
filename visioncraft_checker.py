import requests
import json
import os
import time

# List of available endpoints to check with the filename for them
urls = {
            "1": ("https://visioncraft.top/sd/models-sd", "SD1-5_models_checker.json", "models"),
            "2": ("https://visioncraft.top/sd/models-sdxl", "SDXL_models_checker.json", "models"),
            "3": ("https://visioncraft.top/sd/models-sd3", "SD3_models_checker.json", "models"),
            "4": ("https://visioncraft.top/sd/loras-sd", "SD1-5_loras_checker.json", "loras"),
            "5": ("https://visioncraft.top/sd/loras-sdxl", "SDXL_loras_checker.json", "loras"),
            "6": ("https://visioncraft.top/sd/loras-sd3", "SD3_loras_checker.json", "loras"),
            "7": ("https://visioncraft.top/sd/samplers", "samplers_checker.json", "samplers"),
            "8": ("https://visioncraft.top/models-llm", "llm_checker.json", "llm models"),
        }

# Function to fetch data from a URL
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}. Error: {e}")
        return None

# Function to load existing data from a file
def load_data(filename):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save data to a file
def save_data(filename, data):
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(sorted(data, key=lambda x: x.lower()), file, indent=4, ensure_ascii=False)

# Function to check for new data
def find_new_items(new_items, existing_items):
    existing_lower = set(item.lower() for item in existing_items)
    return [item for item in new_items if item.lower() not in existing_lower]

# Function to find missing data
def find_missing_items(response_items, existing_items):
    response_lower = set(item.lower() for item in response_items)
    return [item for item in existing_items if item.lower() not in response_lower]

# Function to update/create the data file
def check_file(filename, data, created=False, no=False):
    name = filename.replace('checker.json', '').replace('_',' ')
    if created :
        msg = "updated"
    else:
        msg = "created"

    
    if no :
        message = f"The list for {name}hasn't been {msg}."
    else:
        message = f"The list for {name}has been successfully {msg}."
        save_data(filename, data)
    print(message)

# Main function
def main(type=None):
    while True:
        os.system("cls || clear")
        if type is None:
            TO_CHECK = input(
                "What do you want to check?\n"
                "1 - SD1.5 Models\n"
                "2 - SDXL Models\n"
                "3 - SD3 Models\n-----\n"
                "4 - SD 1.5 LORAs\n"
                "5 - SDXL LORAs\n"
                "6 - SD3 LORAs\n-----\n"
                "7 - Samplers\n"
                "8 - llm models\n\n"
                "9 - All\n>>> "
            )
        else:
            TO_CHECK = type


        if TO_CHECK == "9":
            check_all()
            return

        if TO_CHECK not in urls:
            print("Invalid input. Please select a valid option.")
            time.sleep(3)
            continue

        url, filename, item_type = urls[TO_CHECK]
        response_data = fetch_data(url)
        if response_data is None:
            return

        existing_data = load_data(filename)

        new_items = find_new_items(response_data, existing_data)
        missing_items = find_missing_items(response_data, existing_data)

        print(f"Registered {item_type}: {len(existing_data)}\n{'#' * 25}")

        if new_items:
            print(f"New {item_type} found ({len(new_items)}):")
            for item in sorted(new_items, key=lambda x: x.lower()):
                print(f"- {item}")
            print('-' * 25)
        else:
            print(f"No new {item_type} found.")
            print('-' * 25)

        if missing_items:
            print(f"Unknown/deleted {item_type} found ({len(missing_items)}):")
            for item in missing_items:
                print(f"- {item}")
            print('#' * 25)
        else:
            if os.path.isfile(filename) :
                print(f"No unknown/deleted {item_type} found.\n{'#' * 25}")
                break
            else:
                print('#' * 25)
                

        if new_items or missing_items:
            if type != "All":
                while True:
                    value = input("Do you want to update the list [y/n]? ").lower()
                    if os.path.isfile(filename):
                        created = True
                    else:
                        created = False
                        
                    if value in ("y", "yes"):
                        check_file(filename, response_data, created)
                        break
                    elif value in ("n", "no"):
                        check_file(filename, response_data, created, no=True)
                        break
                    else:
                        print("Invalid input\n" + "*" * 20)
                break
            
        else:
            break

    

# Function to check all types and update/create all files
def check_all():
    
    for key, (url, filename, useless) in urls.items():
        print(f"Checking {filename}...")
        response_data = fetch_data(url)
        if response_data:
            save_data(filename, response_data)
            if os.path.isfile(filename):
                print(f"Updated {filename}.")
            else:
                print(f"Created {filename}.")
        else:
            print(f"Failed to fetch data for {filename}.")
    print("all datas are saved")

# Entry point of the program
if __name__ == "__main__":
    main()
    input("Press any key to exit...")
