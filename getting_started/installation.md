# Installation Guide

Follow the steps below to set up and start using the project.

---

## 1. Prerequisites

### Required Software:
- **Python 3.8+** (Verify your installation: `python --version`)
- **pip** (Python's package installer)
- OS-specific requirements:
    - **For Linux**: Pre-installed `gcc`, `make`.
    - **For MacOS/Windows**: Ensure command-line tools (e.g., Xcode, or Developer prompt) are present.

### Optional but Recommended:
- **Virtual Environment**: Useful to manage dependencies. Install with:
  ```bash
  pip install virtualenv
  ```

### System Libraries Required:
- **Linux**:
    ```bash
    apt install -y libssl-dev libffi-dev
    ```

### Data Requirements:
Ensure the following datasets exist in the `/datasets` directory:
- `raw_data_file.csv`
- `training_data.csv`

---

## 2. Clone the Repository

Start by cloning the source code from the repository:
```bash
git clone https://<repository_link>.git
cd <project_directory>
```

---

## 3. Configure Virtual Environment (Recommended)

Set up and activate a virtual environment:

**Linux/MacOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 4. Install Dependencies

The dependencies required for this project are listed in the `requirements.txt` file. Install them with:
```bash
pip install -r requirements.txt
```

### Example Dependencies:
- `numpy`
- `pandas`
- `tensorflow`
- `scikit-learn`

---

## 5. Configure the System

Update the relevant configuration files located in the `/config` folder:

1. **`config.json`**: Modify the following:
   ```json
   {
     "training_data_path": "./datasets/training_data.csv",
     "raw_data_path": "./datasets/raw_data_file.csv",
     "output_folder": "./output"
   }
   ```

2. Ensure that the file `training_data.csv` exists and is correctly structured.

---

## 6. Run Tests

Validate the setup by executing the test modules:
```bash
pytest tests/
```

---

## 7. Start the Application

Run the primary Python script to start the application:
```bash
python main.py
```

---

This should complete the installation process. If additional help is needed, refer to the `README.md` file or contact the project maintainers.