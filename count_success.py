import json

# Load the JSON data from the file
with open("success.json", "r") as file:
    data = json.load(file)

# Count the number of success entries
success_count = len(data)

print(f"Number of success entries: {success_count}")
