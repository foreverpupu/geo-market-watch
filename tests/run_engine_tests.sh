#!/bin/bash
# Run all engine core logic tests

echo "========================================"
echo "Geo Market Watch - Engine Core Tests"
echo "========================================"
echo ""

# Run engine core tests
echo "Running engine core logic tests..."
python tests/engine/test_engine_core.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All engine tests passed!"
    exit 0
else
    echo ""
    echo "❌ Some tests failed"
    exit 1
fi
