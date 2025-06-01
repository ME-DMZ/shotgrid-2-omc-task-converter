# ShotGrid Tasks to MovieLabs Tasks OMC v2.6 Converter

**Project Status:** `v0.0.1` (Prototype Pre-release)
**Current Release:** [v0.0.1](https://github.com/ME-DMZ/shotgrid-2-omc-task-converter/releases/tag/v0.0.1) *(This link assumes you've created a release tagged `v0.0.1`)*

**Stakeholders:** This prototype has been developed for evaluation and feedback by MovieLabs and The Bends.

## 1\. Overview

This Python-based utility converts task data exported from Autodesk ShotGrid (formerly Shotgun) in CSV format into a JSON format compliant with the MovieLabs Ontology for Media Creation (OMC) v2.6 specification, specifically targeting Task entities.

The primary goal of this `v0.0.1` prototype is to demonstrate a viable workflow for transforming production tracking data into an OMC-compatible structure. It includes a graphical user interface (GUI) and an integrated feature to validate the generated OMC JSON against the official MovieLabs online validator.

## 2\. Key Features (as of v0.0.1)

  * **CSV to OMC JSON Conversion:** Transforms ShotGrid task CSVs into a list of OMC Task entities.
  * **GUI Interface:** User-friendly interface (Tkinter) for file selection and output specification.
  * **MovieLabs OMC v2.6 Compliance Focus:** Aims to generate JSON aligning with the OMC v2.6 schema for Task entities.
  * **Data Preservation:** Includes `shotgridPassThroughData_json` to carry over original ShotGrid task fields within `customData`.
  * **Predefined Mappings:** Implements mappings for ShotGrid task statuses to OMC Task states and pipeline steps to OMC Functional Classes.
  * **Online Validation Integration:** Allows sending generated JSON to the MovieLabs OMC online validator (`/api/check`) and viewing results.
  * **Themed UI:** Features a custom "Dominant Blue" theme.
  * **Progress Tracking:** Visual feedback during conversion and validation.
  * **Basic Project Setup:** Includes `.gitignore`, `requirements.txt`, and this `README.md`.

## 3\. Getting This Version (v0.0.1)

There are two main ways to get this version:

1.  **From the GitHub Releases Page (Recommended for a stable version):**

      * Navigate to the [Releases page](https://github.com/ME-DMZ/shotgrid-2-omc-task-converter/releases) of this repository.
      * Look for release `v0.0.1` and download the source code (`.zip` or `.tar.gz`).

2.  **Clone the `main` Branch:**
    The `main` branch currently reflects the `v0.0.1` state.

    ```bash
    git clone [https://github.com/ME-DMZ/shotgrid-2-omc-task-converter.git](https://github.com/ME-DMZ/shotgrid-2-omc-task-converter.git)
    cd shotgrid-2-omc-task-converter
    ```

## 4\. Setup and Installation (for v0.0.1)

Once you have the source code:

1.  **Navigate to Project Directory:**
    Open your terminal or command prompt and go into the `shotgrid-2-omc-task-converter` directory.

2.  **Create and Activate a Virtual Environment (Strongly Recommended):**

    ```bash
    python -m venv .venv
    ```

      * Windows (Git Bash/PowerShell): `source .venv/Scripts/activate`
      * Windows (Command Prompt): `.venv\Scripts\activate.bat`
      * macOS/Linux: `source .venv/bin/activate`

3.  **Install Dependencies:**
    This project uses a `requirements.txt` file to list its dependencies. Install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

    This will install `pandas`, `requests`, and `tksvg` at the versions used for this release.
    *(Note: `tkinter` is typically included with Python. A `.gitignore` file is included in the repository to keep it clean.)*

4.  **Logo (Optional):**

      * The UI attempts to load `logo.svg` from the same directory as the script. If you have an SVG logo, place it there or update the path in the `load_logo()` function within the script `Shotgrid-to-OMC.py`. `tksvg` is required for this feature.

## 5\. Usage

1.  **Run the Script:**
    With your virtual environment activated and dependencies installed, execute the main Python script:

    ```bash
    python Shotgrid-to-OMC.py
    ```

    *(Ensure `Shotgrid-to-OMC.py` is the correct name of your main script file.)*

2.  **Using the Application:**

      * The application window will appear.
      * **Step 1: Select CSV:** Click "Browse CSV..." to select your ShotGrid task export.
      * **Step 2: Choose Output:** Click "Save JSON As..." for the generated OMC JSON.
      * **Convert:** Click "Convert to OMC v2.6 JSON" (enabled when both paths are set).
      * **Validate Online:** After conversion, click "Validate Online" to check against the MovieLabs validator. Results appear in the log and a summary popup.

## 6\. Development Notes & Project Structure (v0.0.1)

  * **Version Control:** This project uses Git. The `main` branch reflects the latest stable release (`v0.0.1`).
  * **Workflow:** Development of new features or fixes is typically done on separate branches and then merged into `main` via Pull Requests on GitHub.
  * **Releases:** Official versions like `v0.0.1` are tagged in Git and published on the GitHub Releases page.
  * **Current Code Structure:** As of `v0.0.1`, the application logic is primarily contained within the main Python script (`Shotgrid-to-OMC.py`). Future refactoring may modularize this further.

## 7\. Known Issues & Limitations (for v0.0.1)

  * **CSV Structure Dependency:** Assumes a typical ShotGrid task export CSV structure.
  * **Hardcoded Mappings:** Status and Functional Class mappings are currently hardcoded in the script.
  * **Validator Dependency:** Online validation requires an internet connection and relies on the MovieLabs service.
  * **Scope:** Focuses on "Task" entities. Does not yet handle other entity types or complex OMC Manifest relationships.

## 8\. Future Development Ideas (Post v0.0.1)

  * **Modularization:** Refactor the codebase into separate modules (`config.py`, `ui_manager.py`, `omc_converter.py`, etc.) for better organization and maintainability.
  * Configuration file for mappings.
  * Support for other ShotGrid entity types.
  * Offline schema validation.
  * Packaging as a standalone executable.
  * Batch processing.
  * Direct ShotGrid API integration.

## 9\. License

**MIT License**

Copyright (c) 2025 [Your Name or Organization Name - e.g., ME-DMZ or Your Full Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-----

*This README was last updated on June 1, 2025 (for v0.0.1).*
