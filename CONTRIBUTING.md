# Contributing Guide - Omnilector

Thank you for your interest in contributing to **Omnilector**! As an open-source project, we value any type of contribution, whether it is reporting bugs, suggesting improvements, writing documentation, or submitting Pull Requests with new code.

---

## 📋 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat everyone with respect and professionalism.

---

## 🛠️ How to Get Started

### 1. Prerequisites
Make sure you have installed:
* **Python 3.13** or higher.
* **uv** (the recommended Python package and environment manager). You can install it with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  *(On Windows you can run `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`).*

### 2. Clone the Repository
Fork the repository on GitHub and then clone it locally:
```bash
git clone https://github.com/your-username/Omnilector.git
cd Omnilector
```

### 3. Set Up the Development Environment
Install all dependencies (including development dependencies) and sync the environment:
```bash
uv sync
```

### 4. Run the Server Locally
To start the development server with automatic reload:
```bash
uv run omnilector-dev
```
The server will be available at `http://localhost:8000`.

---

## 💡 How to Contribute Changes

### Report Bugs or Suggest Features
If you find a bug or have an idea for improvement, check the **Issues** section first to see if it is already being discussed. If not, open a new Issue using the corresponding templates.

### Submit a Pull Request (PR)
1. Create a descriptive branch for your changes:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Make your changes in the code, ensuring you follow the project style guidelines.
3. Format your code and run linting checks if you have formatting tools installed.
4. Commit your changes with clear messages:
   ```bash
   git commit -m "feat: add support for a new barcode format"
   ```
5. Push your branch to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
6. Open a Pull Request against the `main` branch of the official **Omnilector** repository. Make sure to fill out the PR template with all the requested information.

Thank you again for your help in improving Omnilector!
