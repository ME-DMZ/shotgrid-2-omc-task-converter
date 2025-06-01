# ShotGrid Tasks to MovieLabs Tasks OMC v2.6 Converter

**Project Status:** Prototype

**Stakeholders:** This prototype has been developed for evaluation and feedback by MovieLabs and The Bends.

## 1. Overview

This Python-based utility converts task data exported from Autodesk ShotGrid (formerly Shotgun) in CSV format into a JSON format compliant with the MovieLabs Ontology for Media Creation (OMC) v2.6 specification, specifically targeting Task entities.

The primary goal of this prototype is to demonstrate a viable workflow for transforming production tracking data into an OMC-compatible structure, facilitating interoperability and data exchange within media creation pipelines. It includes a graphical user interface (GUI) for ease of use and an integrated feature to validate the generated OMC JSON against the official MovieLabs online validator.

## 2. Key Features

* **CSV to OMC JSON Conversion:** Transforms ShotGrid task CSVs into a list of OMC Task entities.
* **GUI Interface:** Provides a user-friendly interface built with Tkinter for selecting input CSV files and specifying output JSON file locations.
* **MovieLabs OMC v2.6 Compliance:** Aims to generate JSON that aligns with the OMC v2.6 schema for Task entities.
* **Data Preservation:** Includes a mechanism (`shotgridPassThroughData_json`) to carry over all original ShotGrid task fields within the `customData` of each OMC Task entity, ensuring no data loss during conversion.
* **ShotGrid State Mapping:** Implements a predefined mapping from common ShotGrid task statuses to OMC Task states.
* **Pipeline Step to Functional Class Mapping:** Maps ShotGrid pipeline steps to official OMC Functional Classes.
* **Online Validation Integration:** Allows users to send the generated JSON directly to the MovieLabs OMC online validator (`/api/check`) and view the results within the application.
* **Themed UI:** Features a custom "Dominant Blue" theme for an enhanced user experience.
* **Progress Tracking:** Visual feedback during the conversion and validation processes.

## 3. Technology Stack & Requirements

* **Python 3.x**
* **Libraries:**
    * `pandas`: For CSV data manipulation.
    * `tkinter`: For the graphical user interface (usually part of Python's standard library).
    * `requests`: For making HTTP requests to the online validator.
    * `tksvg` (Optional, for logo display): For rendering SVG images in the Tkinter UI.

## 4. Setup and Installation

1.  **Clone the Repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Activate the virtual environment
    # Windows (Git Bash/PowerShell):
    source .venv/Scripts/activate
    # Windows (Command Prompt):
    .venv\Scripts\activate.bat
    # macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    A `requirements.txt` file should ideally be present. If not, install the necessary packages manually:
    ```bash
    pip install pandas requests tksvg
    ```
    *(Note: `tkinter` is typically included with Python and does not require a separate pip installation.)*

4.  **Logo (Optional):**
    * If you wish to display the logo in the UI, ensure an SVG file named `logo.svg` is present in the same directory as the main Python script (e.g., `Shotgrid-to-OMC.py`), or update the path in the `load_logo()` function within the script.

## 5. Usage

1.  **Run the Script:**
    Execute the main Python script from your terminal (ensure your virtual environment is activated if you're using one):
    ```bash
    python Shotgrid-to-OMC.py
    ```
    *(Replace `Shotgrid-to-OMC.py` with the actual script name if different.)*

2.  **Using the Application:**
    * The application window will appear.
    * **Step 1: Select ShotGrid CSV Export:** Click "Browse CSV..." to select your ShotGrid task export file.
    * **Step 2: Choose Output Location:** Click "Save JSON As..." to specify the name and location for the generated OMC JSON file.
    * **Convert:** Once both paths are set, the "Convert to OMC v2.6 JSON" button will be enabled. Click it to start the conversion. Progress will be shown in the log area.
    * **Validate Online:** After a successful conversion, the "Validate Online" button will be enabled. Click this to send the generated JSON to the MovieLabs online validator. Results (pass/fail/issues) will be displayed in the log area and a summary popup.

## 6. Development Notes & Workflow

* **Branching:** Feature development and bug fixes should be done on separate branches (e.g., `feat/new-feature`, `fix/bug-fix`).
* **Commits:** Follow conventional commit message formats (e.g., `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).
* **Pull Requests (PRs):** Merge changes into the `main` branch via Pull Requests on GitHub, allowing for review (even if self-reviewed for solo projects). "Squash and merge" is the preferred method to keep the `main` branch history clean.
* **Version Tagging:** For significant releases or milestones, create version tags (e.g., `v0.1.0`, `v1.0.0`) and corresponding GitHub Releases.

## 7. Known Issues & Limitations (Prototype Stage)

* **Error Handling for CSV Structure:** Assumes a certain CSV structure based on typical ShotGrid task exports. Robustness against highly varied CSV formats could be improved.
* **Mapping Rigidity:** Status and Functional Class mappings are currently hardcoded. Future versions could make these configurable.
* **SVG Logo Path:** Currently hardcoded to look for `logo.svg` in the script's directory.
* **Online Validator Dependency:** The online validation feature requires an active internet connection and depends on the availability of the MovieLabs validator service.
* **Limited Scope:** This prototype focuses solely on "Task" entities from ShotGrid. It does not currently handle other ShotGrid entity types or more complex OMC structures (like full Manifests with relationships beyond basic context).

## 8. Future Development Ideas

* Configuration file for mappings (status, functional classes).
* Support for other ShotGrid entity types (e.g., Assets, Shots, Versions) and their corresponding OMC representations.
* More sophisticated error reporting and user guidance for CSV parsing issues.
* Option for offline schema validation using a local OMC JSON schema file.
* Packaging the application as a standalone executable (e.g., using PyInstaller).
* Batch processing of multiple CSV files.
* Direct ShotGrid API integration (to pull data instead of relying on CSV exports).

## 9. License

(Specify your license here if you have one, e.g., MIT, Apache 2.0. If not decided, you can state "License to be determined" or omit this section for now.)

---

*This README was last updated on June 1, 2025.*
