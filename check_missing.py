#!/usr/bin/env python3
import subprocess

# Get elements from XSD
xsd_elements = set()
result = subprocess.run(['grep', '-o', 'xs:element name="[^"]*"', 'osisCore.2.1.1.xsd'], 
                       capture_output=True, text=True, cwd='C:/Files/Misc/Projects/vibe-bible')
for line in result.stdout.strip().split('\n'):
    if line:
        element = line.replace('xs:element name="', '').replace('"', '')
        xsd_elements.add(element)

# Get elements from dummy file
dummy_elements = set()
result = subprocess.run(['grep', '-o', '<[a-zA-Z][a-zA-Z0-9]*', 'output/00_dummy_vbt.osis.xml'], 
                       capture_output=True, text=True, cwd='C:/Files/Misc/Projects/vibe-bible')
for line in result.stdout.strip().split('\n'):
    if line:
        element = line.replace('<', '')
        dummy_elements.add(element)

missing = xsd_elements - dummy_elements
print("Missing elements from dummy file:")
for element in sorted(missing):
    print(f"  {element}")

print(f"\nTotal XSD elements: {len(xsd_elements)}")
print(f"Elements in dummy: {len(dummy_elements)}")
print(f"Missing: {len(missing)}")