# ECI Training App

A Streamlit-based training application.

## About

This project is built with Streamlit and uses `uv` for fast, reliable Python package and environment management.

## Contributing

We welcome contributions! This project uses [uv](https://github.com/astral-sh/uv) for dependency management and development workflows.

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installing uv

If you don't have uv installed, you can install it using:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tlorans/eci_training_app.git
   cd eci_training_app
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   uv sync
   ```
   
   This command will:
   - Create a virtual environment (if it doesn't exist)
   - Install all dependencies from `pyproject.toml`
   - Lock dependencies in `uv.lock`

3. **Run the application:**
   ```bash
   uv run streamlit run Home.py
   ```

### Development Workflow

#### Adding Dependencies

To add a new dependency:
```bash
uv add package-name
```

To add a development dependency:
```bash
uv add --dev package-name
```

#### Removing Dependencies

```bash
uv remove package-name
```

#### Updating Dependencies

To update all dependencies:
```bash
uv sync --upgrade
```

To update a specific package:
```bash
uv add package-name --upgrade
```

#### Running Scripts

You can run any Python script or command within the virtual environment:
```bash
uv run python script.py
uv run streamlit run pages/1_Session_1.py
```

#### Activating the Virtual Environment

While `uv run` is recommended, you can also activate the virtual environment manually:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Project Structure

```
eci_training_app/
├── Home.py              # Main application entry point
├── main.py              # Additional main module
├── template.py          # Template file
├── pages/               # Streamlit pages
│   └── 1_Session_1.py
├── summaries/           # Summary documents
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock             # Locked dependencies (auto-generated)
└── README.md           # This file
```

### Making Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them locally:
   ```bash
   uv run streamlit run Home.py
   ```

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. Push to your fork and submit a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

### Best Practices

- Always use `uv sync` after pulling changes to ensure your dependencies are up to date
- Use `uv run` to execute commands within the project's virtual environment
- Commit both `pyproject.toml` and `uv.lock` when adding/updating dependencies
- Test your changes locally before submitting a pull request

### Troubleshooting

**Issue: `uv` command not found**
- Make sure uv is installed and added to your PATH
- Try restarting your terminal after installation

**Issue: Dependencies not installing**
- Try removing the `.venv` directory and running `uv sync` again
- Ensure you're using Python 3.13 or higher: `python --version`

**Issue: Streamlit not running**
- Verify the app starts correctly: `uv run streamlit run Home.py`
- Check for any error messages in the terminal


