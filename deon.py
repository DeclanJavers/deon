import concurrent.futures
import argparse
from command_runner import command_runner
from listenForCommand import listen_for_command, save_command_to_file
from responseFinder import responseFinder
from functionFinder import functionFinder
from tts import speak
from openTxt import openTxt

def handle_completed_action(future):
    # This will be called when the future completes
    try:
        excecuted_function_description = future.result()
        print(f"Action completed with description: {excecuted_function_description}")
    except Exception as e:
        print(f"An error occurred while executing the action: {e}")

def process_command(command, executor, testing_mode):
    if command:
        # Save the latest command to a file
        save_command_to_file(command)

        # Print the command
        print(f"Command: {command}")

        # Get the action(s) that should be executed
        actions = functionFinder(command)

        # Debugging: Print the identified actions
        print(f"Identified actions: {actions}")

        if actions:  # Ensure actions were found
            # Execute actions in a separate thread
            future = executor.submit(command_runner, actions)

            # Add a callback to handle the future's completion
            future.add_done_callback(handle_completed_action)

            # Wait for the future to complete and get the result if needed
            try:
                excecuted_function_description = future.result()
                response = responseFinder(
                    openTxt('text_files/responseTxt.txt'),
                    openTxt('text_files/latest_function.txt'),
                    openTxt('text_files/latest_command.txt'),
                    excecuted_function_description
                )
            except Exception as e:
                response = f"An error occurred: {e}"
                print(f"Error while processing command: {e}")

        else:
            # If no actions are identified, still generate a response
            response = "No valid actions identified for the command."

        # Print and speak the response immediately (regardless of testing mode)
        print(f"\nResponse: {response}\n")
        
        if not testing_mode:
            speak(response)


def main(testing_mode=True, sms_command=None):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if sms_command:
            # Process the command from SMS
            process_command(sms_command, executor, testing_mode)
        else:
            while True:
                print(f"Testing Mode: {testing_mode}")  # Debugging statement

                if testing_mode:
                    # Prompt the user to input a command in testing mode
                    command = input("Enter your command: ")
                else:
                    # Use voice command when not in testing mode
                    command = listen_for_command()
                    print(f"Command received: {command}")  # Debugging statement

                # Process the command
                process_command(command, executor, testing_mode)

# Run the main function if this script is executed
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sms_command', type=str, help='Command received from SMS')
    args = parser.parse_args()
    
    # Run in SMS mode if a command is provided, otherwise run in interactive mode
    main(testing_mode=True, sms_command=args.sms_command)
