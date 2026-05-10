import os

# Function to capitalize names
def capitalize_name(name):
    return name.capitalize()

# Get input from the user for the file path
input_file_path = input("Enter the path to the text file you want to capitalize: ")

# Normalize the file path
input_file_path = os.path.abspath(input_file_path)

# Check if the file exists
if not os.path.isfile(input_file_path):
    print(f"Error: The file '{input_file_path}' does not exist.")
    exit(1)

# Read names from the input file
with open(input_file_path, 'r') as input_file:
    lines = [line.strip() for line in input_file.readlines()]

# Capitalize each name and write to a new file
output_file_name = os.path.basename(input_file_path).rsplit('.', 1)[0] + '_capitalized.txt'
output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)

with open(output_file_path, 'w') as output_file:
    for line in lines:
        capitalized_line = ' '.join(word.capitalize() for word in line.split())
        output_file.write(capitalized_line + '\n')

print(f"Names have been processed and saved to '{output_file_path}'.")
