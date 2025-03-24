from command_runner import command_runner
from listenForCommand import save_command_to_file
from responseFinder import responseFinder
from functionFinder import functionFinder
from openTxt import openTxt

# Function to handle completion of actions in separate threads
async def handle_completed_action(future):
    try:
        # Retrieve the result from the future once the task is completed
        executed_function_description = future.result()
        print(f"Action completed with description: {executed_function_description}")
    except Exception as e:
        # Log any errors that occur during action execution
        print(f"An error occurred while executing the action: {e}")

# Process the given command and perform actions
async def process_command(command, executor):
    if command:
        # Save the command to a file (for persistence or logging purposes)
        save_command_to_file(command)

        # Debugging output: Print the received command
        print(f"Command: {command}")

        # Identify actions based on the command
        actions = functionFinder(command)

        # Debugging: Print the identified actions
        print(f"Identified actions: {actions}")

        if actions:
            # Submit the actions to the executor for concurrent execution
            future = executor.submit(command_runner, actions)

            # Add a callback to handle completion of the future
            future.add_done_callback(lambda fut: handle_completed_action(fut))

            # Wait for the future to complete and get the result if needed
            try:
                executed_function_description = future.result()  # Simulate async wait
            except Exception as e:
                # Log any errors and set a default description
                executed_function_description = "Error occurred while executing actions."
                print(f"Error while executing actions: {e}")
        else:
            # Set a default description when no actions are found
            executed_function_description = "No actions were found for the command."

        # Always call responseFinder to generate a response
        response = responseFinder(
            openTxt('text_files/responseTxt.txt'),
            openTxt('text_files/latest_function.txt'),
            openTxt('text_files/latest_command.txt'),
            executed_function_description
        )

        return response
