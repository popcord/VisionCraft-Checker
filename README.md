# VisionCraft Checker

This script checks for new and missing (deleted) SD models, LORAs, samplers, and LLM models from [VisionCraft](https://t.me/visioncraft_channel). It updates JSON files accordingly to save and log data.

## Features

- **Model Checking**: Supports multiple types of models including `SD-3.0`, `SD-1.5`, `SDXL-1.0`, `SD-2.0`, and others.
- **LORA Checking**: Supports `sd` and `sdxl` LORA types.
- **Sampler and LLM Model Checking**: Checks for new or missing samplers and LLM models.
- **Logging**: Logs newly detected and missing items to a log file.
- **Data Management**: Automatically updates or creates JSON files based on the latest fetched data.

## Usage

### Using the Python Script

1. **Install Python**: Ensure that you have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. **Clone the Repository**: Clone or download this repository to your local machine.
3. **Navigate to the Directory**: Open a terminal or command prompt and navigate to the directory containing the `visioncraft_checker.py` file.
4. **Install Dependencies**: Install the required dependencies using pip:
    ```bash
    pip install requests
    ```
5. **Run the Script**: Execute the Python script by running the following command:
    ```bash
    python visioncraft_checker.py
    ```
6. **Follow On-Screen Instructions**: Choose what you want to check (models, LORAs, samplers, or LLM models). You can also check all at once.

### Using the Executable File

1. **Download Executable**: Download the executable file (`visioncraft_checker.exe`) from the [releases](https://github.com/popcord/VisionCraft-Models-Checker/releases/) page.
2. **Run the Executable**: Double-click the executable file to run it.

### Example Output

The script will provide output indicating new or missing models, LORAs, samplers, or LLM models. You will be prompted to update the JSON file if there are changes.

## Logging

- **Log File**: Changes are logged to a file named `log.txt` and additionally to separate log files for models and LORAs (`models_change_log.txt` and `loras_change_log.txt`).
- **New Items**: Newly detected models, LORAs, samplers, or LLM models are listed.
- **Missing Items**: Items that are missing compared to the previous check are also listed.

## Notes

- Ensure that you have an active internet connection while running the script or executable.
- The script will create or update JSON files in the same directory to store model information.

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <h1>Example</h1>
  <img src="https://raw.githubusercontent.com/popcord/VisionCraft-Checker/v1.4/image/screen.png" />
</div>

---

<div align="center">
  <h1>Viewers</h1>
  <img src="https://profile-counter.glitch.me/VisionCraft-Checker/count.svg" />
</div>
