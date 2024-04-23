import requests
import json

def fetch_models(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from the URL. Status code:", response.status_code)
        return None

def load_existing_models(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            if data:
                return json.loads(data)
            else:
                return []
    except FileNotFoundError:
        return []

def save_models(filename, models):
    with open(filename, "w") as file:
        list = []
        for model in sorted(models, key=lambda x: x.lower()):
            list.append(model)
        json.dump(list, file, indent=4)

def check_new_models(new_models, existing_models):
    new_models = [model for model in new_models if model.lower() not in map(str.lower, existing_models)]
    return new_models

def find_missing_models(response_models, existing_models):
    missing_models = [model for model in existing_models if model.lower() not in map(str.lower, response_models)]
    return missing_models

def update_models_file(filename, models):
    save_models(filename, models)
    print("The list has been successfully updated.")

def main():
    url = "https://visioncraft.top/sd/models"
    filename = "config.json"

    response_models = fetch_models(url)
    if response_models is None:
        return

    existing_models = load_existing_models(filename)

    new_models = check_new_models(response_models, existing_models)
    missing_models = find_missing_models(response_models, existing_models)

    print("Registered models:", len(existing_models), "\n" + "#" * 25)

    if new_models:
        print(f"New models found ({len(new_models)}):")
        for model in sorted(new_models, key=lambda x: x.lower()):
            print("-", model)
        print("-" * 25)
    else:
        print("No new models found.")

    if missing_models:
        print(f"New unknown models found ({len(missing_models)}):")
        for model in missing_models:
            print("-", model)
        print("#" * 25)
    else:
        print("No unknown models found.")

    if new_models or missing_models:
        while True:
            value = input("Do you want to update the list [y/n]? ").lower()
            if value in ("y", "yes"):
                update_models_file(filename, response_models)
                break
            elif value in ("n", "no"):
                print("List not updated.")
                break
            else:
                print("Invalid input\n" + "*" * 20)

    input("Press any key to exit...")

if __name__ == "__main__":
    main()
