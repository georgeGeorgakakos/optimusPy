#!/bin/bash
# OptimusDB Python Client - Setup Script

echo "=================================="
echo "OptimusDB Python Client Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x optimusdb_client.py
chmod +x example_usage.py
chmod +x batch_operations.py
echo "✅ Scripts are now executable"

# Test connection
echo ""
echo "Testing connection to OptimusDB..."
python3 optimusdb_client.py health

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ Setup completed successfully!"
    echo "=================================="
    echo ""
    echo "Quick start:"
    echo "  1. Get all documents:     python3 optimusdb_client.py get"
    echo "  2. Upload TOSCA file:     python3 optimusdb_client.py upload sample_tosca.yaml"
    echo "  3. Run examples:          python3 example_usage.py"
    echo "  4. View documentation:    cat README.md"
    echo ""
else
    echo ""
    echo "⚠️  Setup completed but server connection failed"
    echo "Please check if OptimusDB is running and accessible"
    echo ""
    echo "Try: python3 optimusdb_client.py health --url http://localhost:8080"
    echo ""
fi