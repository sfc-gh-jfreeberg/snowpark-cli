# Snowpark CLI

A command-line tool for running Python files with automatically injected Snowpark Session objects.

## Installation

### Global Installation (Recommended)

To install globally so you can use `snowpark` command from any directory:

```bash
# Install globally using pip
pip install .
```

Or for development with editable install:
```bash
# Install globally in editable mode (changes reflect immediately)
pip install -e .
```

### Local Development Installation

For local development within this project directory:

```bash
# Install dependencies only
pip install -r requirements.txt

# Run directly with Python
python -m snowpark_cli.cli run <file>
```

### Verify Installation

After global installation, verify it works:

```bash
# Check if command is available
snowpark --version

# View help
snowpark --help
snowpark run --help
```

### Troubleshooting Installation

**Problem**: `PackageNotFoundError: snowpark-cli` when running `snowpark` command

**Solution**: Make sure you install globally (not in a virtual environment):

```bash
# First, deactivate any virtual environment
deactivate

# Then install globally
cd /path/to/snowpark-cli
pip install .

# Verify it's installed globally
which snowpark
snowpark --version
```

**Note**: If you want to use it within a virtual environment, you'll need to install it in each environment where you want to use it.

## Usage

### Basic Usage

`snowpark run <file>` - Runs the specified Python file and injects a Session object using the default connection in `~/.snowflake/connections.toml`.

```bash
snowpark run examples/hello_snowpark.py
```

### Optional Parameters

- `--connection` / `-c` - The name of the connection in connections.toml to use
- `--connections-file` - Path to a custom connections.toml file

```bash
# Use a specific connection
snowpark run examples/hello_snowpark.py --connection production

# Use a custom connections file
snowpark run examples/hello_snowpark.py --connections-file /path/to/connections.toml
```

## Configuration

### Connections File

Create a connections configuration file at `~/.snowflake/connections.toml`:

```toml
# Default connection name (optional)
default_connection_name = "default"

[default]
account = "your-account-identifier"
user = "your-username"
password = "your-password"
database = "your-database"
schema = "your-schema"
warehouse = "your-warehouse"
role = "your-role"

[production]
account = "prod-account-identifier"
user = "prod-username"
password = "prod-password"
database = "prod-database"
schema = "prod-schema"
warehouse = "prod-warehouse"
role = "prod-role"
```

### Session Injection

When you run a Python file with `snowpark run`, a `session` variable is automatically available in your script:

```python
# No need to import or create session manually
# The 'session' variable is injected automatically

def main():
    # Use the session directly
    df = session.create_dataframe([[1, "Alice"], [2, "Bob"]], schema=["id", "name"])
    df.show()
    
    # Run SQL queries
    result = session.sql("SELECT CURRENT_VERSION()").collect()
    print(f"Snowflake version: {result[0][0]}")

if __name__ == "__main__":
    main()
```

## Examples

See the `examples/` directory for sample Python scripts and configuration files.

## Requirements

- Python 3.8+
- snowflake-snowpark-python
- click
- toml


