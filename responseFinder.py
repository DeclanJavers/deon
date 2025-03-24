import google.generativeai as gemini

# Initialize the Gemini API (Google Generative AI)
gemini.configure(api_key="enter_your_api_key_here") 

# Function to create the response text using the Gemini API
def responseFinder(responseTxt, latestFunction, latestCommand, excecuted_function_description):

    # Ensure all variables are strings
    responseTxt = str(responseTxt)
    latestFunction = str(latestFunction)
    latestCommand = str(latestCommand)

    # Create the prompt for Gemini API using f-strings
    if (latestFunction == "\n"):
        print("++++++++++++++++++++==============++++++++++++++++++========")
        gemini_prompt = (
            f"{responseTxt}\n\n"
            f"Here is the latest command: {latestCommand}\n\n"
        )
    else:
        print("++++++++++++++++++++==============++++++++++++++++++========\n" + latestFunction + "|")
        gemini_prompt = (
            f"{responseTxt}\n\n"
            f"Here are the name(s) of the function you just ran, (na if no function was run): {latestFunction}\n\n"
            f"Here is the latest command: {latestCommand}\n\n"
            f"Here is the reponse from the command(s) run: {excecuted_function_description}"
        )

    #print("prompt: " + gemini_prompt)

    # Print the constructed prompt for debugging or verification
    #print(f"Here is the command: {gemini_prompt}")

    try:

        model = gemini.GenerativeModel("gemini-1.5-flash")

        safe = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]


        print(gemini_prompt)
        # Generate the content with the model
        response = model.generate_content(gemini_prompt, safety_settings=safe)

        # Access the generated text from the response dictionary
        generated_response = response.text  # Updated to access the result key
        
        # Save the response to the latest_response.txt file
        with open('text_files/latest_response.txt', 'w') as f:  # Open the file in write mode
            f.write(generated_response)
        
        return generated_response
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Test the function with different inputs
def test_responseFinder():
    # Read files for testing
    try:
        with open('text_files/responseTxt.txt', 'r') as f:
            responseTxt = f.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        responseTxt = ""

    try:
        with open('text_files/latest_command.txt', 'r') as f:
            latestCommand = f.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        latestCommand = ""

    try:
        with open('text_files/latest_function.txt', 'r') as f:
            latestFunction = f.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        latestFunction = ""

    test_commands = [
        "turning on the lights",
        "playing music",
        "cooking dinner",
        "going for a walk"
    ]

    for command in test_commands:
        print(f"Command: {command}")
        response = responseFinder(responseTxt, latestFunction, latestCommand, "there is no description availible right now")
        if response:
            print(f"Response: {response}\n")
        else:
            print("Failed to generate a response.\n")

if __name__ == "__main__":
    test_responseFinder()
