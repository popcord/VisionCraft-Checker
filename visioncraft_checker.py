# Import necessary libraries
import requests, json, os, time

# Function to fetch data from a URL
def fetch_checker(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from the URL. Status code:", response.status_code)
        return None

# Function to load existing data from a file
def load_existing_checker(filename):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            data = file.read()
            if data:
                return json.loads(data)
            else:
                return []
    except FileNotFoundError:
        return []

# Function to save data to a file
def save_checker(filename, checker):
    with open(filename, "w", encoding='utf-8') as file:
        list = []
        for model in sorted(checker, key=lambda x: x.lower()):
            list.append(model)
        json.dump(list, file, indent=4, ensure_ascii=False)

# Function to check for new data
def check_new_checker(new_checker, existing_checker):
    new_checker = [model for model in new_checker if model.lower() not in map(str.lower, existing_checker)]
    return new_checker

# Function to find missing data
def find_missing_checker(response_checker, existing_checker):
    missing_checker = [model for model in existing_checker if model.lower() not in map(str.lower, response_checker)]
    return missing_checker

# Function to update the data file
def update_checker_file(filename, checker):
    save_checker(filename, checker)
    print("The list has been successfully updated.")

# Main function
def main(type=None):
    while True:
        os.system("cls || clear")
        # Prompt user for selection
        if type is None:
            TO_CHECK = input("What do you want to check?\n1 - Models/Checkpoints\n2 - LORAs\n3 - Samplers\n4 - llm models\n\n5 - All\n>>> ")
        else:
            TO_CHECK = type
        
        # Process user input
        if TO_CHECK == "1":
            url = "https://visioncraft.top/sd/models"
            filename = "models_checker.json"  # Update JSON filename for models/checkpoints
            type = "models"
            break
        elif TO_CHECK == "2":
            url = "https://visioncraft.top/sd/loras"
            filename = "loras_checker.json"  # Update JSON filename for LORAs
            type= "loras"
            break
        elif TO_CHECK == "3":
            url = "https://visioncraft.top/sd/samplers"
            filename = "samplers_checker.json"  # Update JSON filename for Samplers
            type= "samplers"
            break
        elif TO_CHECK == "4":
            url = "https://visioncraft.top/models-llm"
            filename = "llm_checker.json"  # Update JSON filename for llm models
            type= "llm models"
            break
        elif TO_CHECK == "5":
            check_all()
            return
        else:
            print("Invalid input. Please select only 1, 2, 3, 4 or 5")
            time.sleep(3)

    response_checker = fetch_checker(url)
    if response_checker is None:
        return

    existing_checker = load_existing_checker(filename)

    new_checker = check_new_checker(response_checker, existing_checker)
    missing_checker = find_missing_checker(response_checker, existing_checker)

    print(f"Registered {type}:", len(existing_checker), "\n" + "#" * 25)

    if new_checker:
        print(f"New {type} found ({len(new_checker)}):")
        for model in sorted(new_checker, key=lambda x: x.lower()):
            print("-", model)
        print("-" * 25)
    else:
        print(f"No new {type} found.")
        print("-" * 25)

    if missing_checker:
        print(f"New unknown/deleted {type} found ({len(missing_checker)}):")
        for model in missing_checker:
            print("-", model)
        print("#" * 25)
    else:
        print(f"No unknown/deleted {type} found.\n" + "#" * 25)

    if new_checker or missing_checker:
        while True:
            value = input("Do you want to update the list [y/n]? ").lower()
            if value in ("y", "yes"):
                update_checker_file(filename, response_checker)
                break
            elif value in ("n", "no"):
                print("List not updated.")
                break
            else:
                print("Invalid input\n" + "*" * 20)

    input("Press any key to exit...")

# Function to check all types
def check_all():
    main("1")
    main("2")
    main("3")

# Entry point of the program
if __name__ == "__main__":
    main()
