
---

# Rule Engine Application

This is a **Rule Engine Application** built with a simple UI, backend API, and dynamic rule evaluation functionality. The application allows users to create logical rules, combine multiple rules, and evaluate them against dynamic user data. It is built using Python with Flask for the backend and HTML/CSS/JavaScript for the frontend.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dependencies](#dependencies)
3. [Installation and Setup](#installation-and-setup)
4. [Build Instructions](#build-instructions)
5. [How to Run the Application](#how-to-run-the-application)
6. [Design Choices](#design-choices)
7. [API Endpoints](#api-endpoints)
8. [Future Improvements](#future-improvements)

---

## Project Overview

The goal of this project is to create a dynamic **Rule Engine** that allows users to:
- **Create rules** based on user-defined conditions (e.g., `age > 30 AND department == 'Sales'`).
- **Combine multiple rules** using logical operators like `AND` or `OR`.
- **Evaluate rules** against dynamically provided user data in JSON format.

The application includes:
- **Frontend**: A simple web-based interface for interacting with the rule engine.
- **Backend**: A Flask-based REST API to handle rule creation, combination, and evaluation.
- **Rule Engine**: The core logic of parsing, combining, and evaluating rules is handled by the rule engine in Python.

---

## Dependencies

Before running the application, you need to install the following dependencies:

### Python Libraries
1. **Flask**: A lightweight WSGI web application framework.
   - Install Flask using:
   ```bash
   pip install Flask
   ```

### Optional
If you want to use a virtual environment for Python, you can create one using:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Node (Optional for Frontend Enhancements)
- **Node.js and npm**: Required if you want to extend the frontend using advanced build tools like Webpack or TailwindCSS (currently, not required for the simple HTML/CSS setup).
  - [Download Node.js and npm](https://nodejs.org/en/download/)

---

## Installation and Setup

### Step 1: Clone the Repository
Clone this project from the repository:
```bash
git clone https://github.com/your-username/rule-engine-app.git
cd rule-engine-app
```

### Step 2: Install Dependencies
If you’re using a virtual environment, activate it, then install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, you can create it with:
```bash
pip freeze > requirements.txt
```

### Step 3: Set Up the Application Structure
Ensure the following file structure is in place:

```
project_folder/
├── app.py              # Flask backend with API routes
├── rule_engine.py      # Core rule engine logic (AST, evaluation, etc.)
├── templates/
│   └── index.html      # Frontend UI
├── static/             # Static files (if any, e.g., CSS/JS)
├── requirements.txt    # Python dependencies
├── README.md           # This file
```

---

## Build Instructions

To build and run the project, follow these instructions:

1. **Start the Flask Server**:
   Run the Flask application using the following command:
   ```bash
   python app.py
   ```

2. **Access the Frontend**:
   Open your browser and go to `http://127.0.0.1:5000/` to access the web-based UI for creating, combining, and evaluating rules.

---

## How to Run the Application

### Creating a Rule
1. Go to the **"Create a New Rule"** section in the UI.
2. Input a rule in the text field (e.g., `age > 30 AND department == 'Sales'`).
3. Click **"Create Rule"**.
4. The rule will be created and assigned a Rule ID, which will be displayed on the screen.

### Combining Multiple Rules
1. Go to the **"Combine Rules"** section.
2. Enter the **Rule IDs** of the rules you want to combine (comma-separated, e.g., `1, 2`).
3. Choose an operator (`AND` or `OR`).
4. Click **"Combine Rules"**.
5. The combined rule will be stored and assigned a new Rule ID.

### Evaluating a Rule
1. Go to the **"Evaluate a Rule"** section.
2. Enter the **Rule ID** of the rule you want to evaluate.
3. Provide the user data in JSON format (e.g., `{"age": 35, "department": "Sales", "salary": 60000}`).
4. Click **"Evaluate Rule"**.
5. The result of the evaluation (`True` or `False`) will be displayed.

---

## Design Choices

### 1. **Rule Representation (AST)**
   The core of the rule engine is built using an **Abstract Syntax Tree (AST)**. The AST allows for flexible rule construction by parsing rule strings into tree structures. This design choice allows complex rules (with `AND`, `OR` operators) to be represented and evaluated efficiently.

### 2. **API-Driven Architecture**
   The backend exposes a set of **RESTful API endpoints** for rule creation, combination, and evaluation. This allows the application to be extended for other clients in the future (such as mobile apps or third-party integrations).

### 3. **Modular Design**
   The project is designed to be **modular**, separating the rule engine logic (`rule_engine.py`) from the web interface (`app.py` and `index.html`). This makes it easier to maintain and extend.

### 4. **Dynamic Rule Evaluation**
   Rules are evaluated dynamically using Python’s `eval()` function. However, care has been taken to ensure that values in the rules are safely substituted using the actual user data before evaluation. This approach allows any attributes to be evaluated, making the engine flexible for a wide range of use cases.

---

## API Endpoints

1. **Create Rule**: `POST /create_rule`
   - Body: `{ "rule": "age > 30 AND department == 'Sales'" }`
   - Response: `{ "rule_id": 1, "rule_ast": { ... } }`

2. **Combine Rules**: `POST /combine_rules`
   - Body: `{ "rule_ids": [1, 2], "operator": "AND" }`
   - Response: `{ "rule_id": 3, "rule_ast": { ... } }`

3. **Evaluate Rule**: `POST /evaluate_rule_from_db/<rule_id>`
   - Body: `{ "user_data": { "age": 35, "department": "Sales" } }`
   - Response: `{ "result": true }`

---

## Future Improvements

1. **Persistent Storage**: 
   - Currently, rules are stored in-memory using a Python dictionary. This can be extended to use a database (e.g., SQLite, PostgreSQL) to store rules persistently.
   
2. **Enhanced Security**:
   - The use of `eval()` for dynamic rule evaluation, while flexible, can be risky. Future versions of the application should replace `eval()` with a safer alternative like a custom expression parser.

3. **Frontend Enhancements**:
   - The current UI is simple and functional, but it can be enhanced with more styling (e.g., using frameworks like **Bootstrap** or **TailwindCSS**) and additional features like validation, better error handling, and real-time updates.

4. **User Authentication**:
   - Implement user authentication and rule ownership, allowing different users to create, manage, and evaluate their own sets of rules.

---

## License

This project is licensed under the MIT License.

---
