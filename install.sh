#!/bin/bash

# Function to create and activate a virtual environment
create_and_activate_venv() {
    # Check for Python3 or Python availability
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo "Python is not installed. Please install Python 3 before proceeding."
        exit 1
    fi

    # Create a virtual environment based on the operating system
    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        python3 -m venv .venv
        source .venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        python -m venv .venv
        source .venv/Scripts/activate
    else
        echo "Unsupported OS type: $OSTYPE"
        exit 1
    fi
}

# Function to install Python requirements
install_requirements() {
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Please ensure it exists in the current directory."
        exit 1
    fi
}

# Function to run Python scripts
run_python_scripts() {
    if [ -f "add_dummy_data.py" ]; then
        python add_dummy_data.py
    else
        echo "add_dummy_data.py not found. Please ensure it exists in the current directory."
        exit 1
    fi
    
    if [ -f "app.py" ]; then
        python app.py &
    else
        echo "app.py not found. Please ensure it exists in the current directory."
        exit 1
    fi
}

# Function to setup and run frontend
setup_and_run_frontend() {
    if [ -d "frontend" ]; then
        cd frontend || exit

        # Check if node_modules exists, if not run npm install
        if [ ! -d "node_modules" ]; then
            npm install
        fi

        npm run serve
    else
        echo "Frontend directory not found. Please ensure it exists in the current directory."
        exit 1
    fi
}

# Main script execution
create_and_activate_venv
install_requirements
run_python_scripts
setup_and_run_frontend
