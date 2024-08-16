import requests
import json
import os
import time

# List of available models and LORAs to check
MODELS_TYPE = [
    "SD-3.0", "SD-1.5", "SDXL-1.0", "SD-2.0",
    "Playground-v2", "SD-1.4", "Pony", "Kolors",
    "PixArt", "FLUX.1", "HunYuanDiT-v1.2"
]

LORAS_TYPE = [
    "sd", "sdxl"
]

# List of the different api endpoints
URLS = {
    "1": ("https://visioncraft.top/image/models/", "models_checker.json", "models"),
    "2": ("https://visioncraft.top/image/loras/", "loras_checker.json", "loras"),
    "3": ("https://visioncraft.top/image/samplers", "samplers_checker.json", "samplers"),
    "4": ("https://visioncraft.top/models-llm", "llm_checker.json", "llm models"),
}

LOG_FILE = "log.txt"

# Fetch data from URL with error handling
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}. Error: {e}")
        return None

# Load data from a file
def load_data(filename):
    if os.path.isfile(filename):
        with open(filename, "r", encoding='utf-8') as file:
            return json.load(file)
    return {}

# Save data to a file
def save_data(filename, data):
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Find new items in the response data
def find_new_items(new_items, existing_items):
    existing_lower = set(item.lower() for item in existing_items)
    return [item for item in new_items if item.lower() not in existing_lower]

# Find missing items in the existing data
def find_missing_items(response_items, existing_items):
    response_lower = set(item.lower() for item in response_items)
    return [item for item in existing_items if item.lower() not in response_lower]

# Update or create data file
def update_file(filename, data, created=False, no=False):
    action = "updated" if created else "created"
    if no:
        message = f"The list for {filename.replace('checker.json', '').replace('_',' ')} hasn't been {action}."
    else:
        message = f"The list for {filename.replace('checker.json', '').replace('_',' ')} has been successfully {action}."
        save_data(filename, data)
    print(message)

# Log new and missing items to a file
def log_changes(item_type, new_items, missing_items):
    with open(item_type+"_change"+LOG_FILE, "a", encoding='utf-8') as log_file:
        if new_items:
            log_file.write(f"New {item_type} detected:\n")
            for item_type, items in new_items.items():
                log_file.write(f"- {item_type}:\n")
                for item in items:
                    log_file.write(f"  > {item}\n")
        if missing_items:
            log_file.write(f"Unknown/deleted {item_type} detected:\n")
            for item_type, items in missing_items.items():
                log_file.write(f"- {item_type}:\n")
                for item in items:
                    log_file.write(f"  > {item}\n")
        log_file.write("\n")

# Main function
def main(user_type=None):
    while True:
        os.system("cls || clear")
        if user_type is None:
            user_input = input(
                "What do you want to check?\n"
                "1 - Models\n"
                "2 - LORAs\n"
                "3 - Samplers\n"
                "4 - llm models\n\n"
                "5 - All\n>>> "
            )
        else:
            user_input = user_type

        if user_input == "5":
            check_all()
            return

        if user_input not in URLS:
            print("Invalid input. Please select a valid option.")
            time.sleep(3)
            continue

        url, filename, item_type = URLS[user_input]

        if user_input == "1":  # Checking models
            models_data = {}
            for model_type in MODELS_TYPE:
                full_url = url + model_type
                response_data = fetch_data(full_url)
                print("checking " + model_type + " ...")
                if response_data is None:
                    return
                
                models_data[model_type] = response_data
            
            existing_data = load_data(filename)
            print("#" * 20)
            
            new_models = {}
            missing_models = {}
            
            for model_type, models in models_data.items():
                existing_models = existing_data.get(model_type, [])
                new_items = find_new_items(models, existing_models)
                missing_items = find_missing_items(models, existing_models)

                if new_items:
                    new_models[model_type] = new_items
                if missing_items:
                    missing_models[model_type] = missing_items

            if new_models or missing_models:
                if new_models:
                    print("New models found:")
                    for model_type, items in new_models.items():
                        print(f"- {model_type}: {len(items)}")
                
                if missing_models:
                    print("\nUnknown/deleted models found:")
                    for model_type, items in missing_models.items():
                        print(f"- {model_type}: {len(items)}")

                log_changes("models", new_models, missing_models)
                
                while True:
                    value = input("Do you want to update the list [y/n]? ").lower()
                    created = os.path.isfile(filename)
                    
                    if value in ("y", "yes"):
                        update_file(filename, models_data, created)
                        break
                    elif value in ("n", "no"):
                        update_file(filename, models_data, created, no=True)
                        break
                    else:
                        print("Invalid input\n" + "*" * 20)
                break

        elif user_input == "2":  # Checking LORAs
            loras_data = {}
            for lora_type in LORAS_TYPE:
                full_url = url + lora_type
                response_data = fetch_data(full_url)
                print("checking " + lora_type + " ...")
                if response_data is None:
                    return
                
                loras_data[lora_type] = response_data
            
            existing_data = load_data(filename)
            print("#" * 20)
            
            new_loras = {}
            missing_loras = {}
            
            for lora_type, loras in loras_data.items():
                existing_loras = existing_data.get(lora_type, [])
                new_items = find_new_items(loras, existing_loras)
                missing_items = find_missing_items(loras, existing_loras)

                if new_items:
                    new_loras[lora_type] = new_items
                if missing_items:
                    missing_loras[lora_type] = missing_items

            if new_loras or missing_loras:
                if new_loras:
                    print("New LORAs found:")
                    for lora_type, items in new_loras.items():
                        print(f"- {lora_type}: {len(items)}")
                
                if missing_loras:
                    print("\nUnknown/deleted LORAs found:")
                    for lora_type, items in missing_loras.items():
                        print(f"- {lora_type}: {len(items)}")

                log_changes("LORAs", new_loras, missing_loras)
                
                while True:
                    value = input("Do you want to update the list [y/n]? ").lower()
                    created = os.path.isfile(filename)
                    
                    if value in ("y", "yes"):
                        update_file(filename, loras_data, created)
                        break
                    elif value in ("n", "no"):
                        update_file(filename, loras_data, created, no=True)
                        break
                    else:
                        print("Invalid input\n" + "*" * 20)
                break

        else:  # Checking Samplers or llm models
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
                if os.path.isfile(filename):
                    print(f"No unknown/deleted {item_type} found.\n{'#' * 25}")
                else:
                    print('#' * 25)

            if new_items or missing_items:
                if user_type != "All":
                    # For samplers and llm models, just log without grouping
                    log_changes(item_type, {item_type: new_items}, {item_type: missing_items})
                    
                    while True:
                        value = input("Do you want to update the list [y/n]? ").lower()
                        created = os.path.isfile(filename)
                        
                        if value in ("y", "yes"):
                            update_file(filename, response_data, created)
                            break
                        elif value in ("n", "no"):
                            update_file(filename, response_data, created, no=True)
                            break
                        else:
                            print("Invalid input\n" + "*" * 20)
                    break
            else:
                break

# Check all types and update/create all files
def check_all():
    for key, (url, filename, _) in URLS.items():
        print(f"Checking {filename}...")
        response_data = fetch_data(url)
        if response_data:
            save_data(filename, response_data)
            print(f"Updated {filename}." if os.path.isfile(filename) else f"Created {filename}.")
        else:
            print(f"Failed to fetch data for {filename}.")
    print("All data has been saved.")

# Entry point of the program
if __name__ == "__main__":
    main()
    input("Press any key to exit...")

