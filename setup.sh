#!/bin/bash

# Installation and testing script for Snowpark CLI

echo "🚀 Setting up Snowpark CLI..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  snowpark run examples/hello_snowpark.py"
echo "  snowpark run examples/hello_snowpark.py --connection production"
echo ""
echo "Note: Make sure to create ~/.snowflake/connections.toml with your Snowflake credentials"
echo "See examples/connections.toml for the required format"
