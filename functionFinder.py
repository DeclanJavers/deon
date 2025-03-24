import google.generativeai as gemini
import csv
import os

# Configure the Gemini API with your API key
gemini.configure(api_key="enter_your_api_key_here")

# Path to the CSV file for storing responses
RESPONSE_CSV_PATH = 'responses.csv'

# Load functions and names from a CSV file
def load_functions_from_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            functions = [{
                "name": row["name"].strip().lower(),
                "description": row["description"],
                "example_commands": [cmd.strip().lower() for cmd in row["example_commands"].split(', ')]
            } for row in reader]
            function_names = [f["name"] for f in functions]
        return functions, function_names
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return [], []

# Load file contents with error handling
def load_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return ""

def check_existing_input(input_text):
    if not os.path.exists(RESPONSE_CSV_PATH):
        return None
    with open(RESPONSE_CSV_PATH, mode='r', encoding='utf-8', errors='replace') as file:
        reader = csv.DictReader(file)
        # Verify the header names
        if reader.fieldnames != ['input', 'output']:
            print(f"CSV file headers are incorrect. Expected ['input', 'output'], got {reader.fieldnames}.")
            return None
        for row in reader:
            if row['input'] == input_text:
                return row['output']
    return None


# Append a new input-output pair to the CSV file
def append_to_csv(input_text, output_text):
    file_exists = os.path.exists(RESPONSE_CSV_PATH)
    with open(RESPONSE_CSV_PATH, mode='a', newline='') as file:
        fieldnames = ['input', 'output']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'input': input_text, 'output': output_text})

# Load functions and command names from CSV
functions, function_names = load_functions_from_csv('list_of_commands.csv')

# Generate the response based on user command
def functionFinder(action_text):
    # Check if the input is already in the CSV file
    cached_output = check_existing_input(action_text)
    if cached_output:
        print("Response retrieved from the database.")
        return cached_output

    # If input does not exist, generate a new response
    responseTxt = load_file_content('text_files/function_finder.txt')
    latestCommand = load_file_content('text_files/latest_command.txt')

    prompt = f"{responseTxt}\n\n\nHere is the latest command: {action_text}\n"
    prompt += "Choose the best function from the list:\n"
    for func in functions:
        prompt += f"- {func['name']}: {func['description']}\n"
    prompt += "Respond with the function name."
    #print('prompt = ' + prompt)

    try:
        model = gemini.GenerativeModel("gemini-1.5-flash")

        # Generate the content with the model
        response = model.generate_content(prompt)

        # Access the generated text from the response
        generated_response = response.candidates[0].content.parts[0].text.strip().lower()

        # Filter valid function names
        valid_names = [name for name in generated_response.split() if name in function_names]

        # Save the final valid response
        output = ', '.join(valid_names)
        with open('text_files/latest_function.txt', 'w') as f:
            f.write(output)

        # Store the input and output in the CSV file
        append_to_csv(action_text, output)

        # Add the found functions to the latest_function.txt file
        with open('text_files/latest_function.txt', 'a') as f:
            # Remove the contents of the latest_function.txt file
            f.truncate(0)
            f.write(output + '\n')
            print("Response added to latest_function.")
        
        print("Response generated and added to the database.")
        return output
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Test the function with different inputs
def test_responseFinder():
    test_commands = [
        "turn on the lights",
        "tell me a joke and tell me the weather",
        "set a timer for 30 minutes and turn off my lights"
    ]

    for command in test_commands:
        print(f"Command: {command}")
        response = functionFinder(command)
        if response:
            print(f"Response: {response}\n")
        else:
            print("Failed to generate a response.\n")

if __name__ == "__main__":
    test_responseFinder()
