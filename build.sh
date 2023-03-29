# Remove the existing dist directory
rm -rf dist

# Create new dist directory
mkdir dist

# Build the Python project
python3 -m build

# Upload the distribution archives under the dist directory
twine upload dist/*