import google.generativeai as gemini

# Initialize the Gemini API (Google Generative AI)
gemini.configure(api_key="enter_your_api_key_here")  

# Function to create the response text using the Gemini API
def generic_gemini(gemini_prompt):

    # Ensure all variables are strings
    gemini_prompt = str(gemini_prompt)

    # Create the prompt for Gemini API using f-strings
    gemini_prompt = (
        {gemini_prompt}
    )

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
        with open('text_files/newest_generic_gemini.txt', 'w') as f:  # Open the file in write mode
            f.write(generated_response)
        
        return generated_response
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

if __name__ == "__main__":
    print(generic_gemini("hello, how are you?"))
