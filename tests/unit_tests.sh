#!/bin/bash

set -e

echo "Performing unit tests..."

# Perform unit tests for aligner
cd ../src/aligner/unit_tests/
make & ./unit_tests_aligner

echo "Unit tests completed."
