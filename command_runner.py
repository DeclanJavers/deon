import importlib
import os
import asyncio

def command_runner(function_names):
    if not function_names:
        return "No commands provided."

    functions_folder = 'functions'
    output = []

    # Check and list all files in the 'functions' folder for debugging
    try:
        files_in_folder = os.listdir(functions_folder)
        print(f"[DEBUG] Files found in '{functions_folder}': {files_in_folder}")
    except FileNotFoundError:
        print(f"[DEBUG] Folder '{functions_folder}' not found.")
        return f"Folder '{functions_folder}' not found."

    # Split the function names and process each one
    for function_name in function_names.split():
        try:
            print(f"[DEBUG] Processing function: {function_name}")

            # Construct the module path based on the function name
            module_path = f"{functions_folder}.{function_name}"
            print(f"[DEBUG] Importing module: {module_path}")
            
            # Try to import the module
            function_module = importlib.import_module(module_path)
            print(f"[DEBUG] Successfully imported module: {module_path}")
            
            # Try to retrieve the function from the module
            function_to_run = getattr(function_module, function_name, None)
            if function_to_run is None:
                output.append(f"[ERROR] Function '{function_name}' not found in module '{module_path}'.")
                continue
            print(f"[DEBUG] Retrieved function '{function_name}' from module.")

            # Check if the function is callable
            if callable(function_to_run):
                if asyncio.iscoroutinefunction(function_to_run):
                    print(f"[DEBUG] Function '{function_name}' is an async function.")
                    # If it's async, run it using asyncio
                    result = asyncio.run(function_to_run())
                else:
                    print(f"[DEBUG] Function '{function_name}' is a regular callable.")
                    # If it's a normal function, just call it
                    result = function_to_run()
                output.append(f"{function_name}: {result}")
            else:
                output.append(f"[ERROR] '{function_name}' is not callable.")
        
        except ModuleNotFoundError as mnfe:
            print(f"[ERROR] Module '{module_path}' not found: {mnfe}")
            output.append(f"Module for '{function_name}' not found in '{functions_folder}'.")
        
        except AttributeError as ae:
            print(f"[ERROR] AttributeError: {ae}")
            output.append(f"Function '{function_name}' not found in '{module_path}'.")
        
        except Exception as e:
            print(f"[ERROR] Exception occurred while running '{function_name}': {e}")
            output.append(f"An error occurred while running '{function_name}': {e}")

    # Debugging: print the final output
    print(f"[DEBUG] Final output: {output}")
    return "\n".join(output)

# Example usage for testing
if __name__ == "__main__":
    # Simulate calling a function named 'set_timer'
    result = command_runner('set_timer')
    print(f"Command Runner Result:\n{result}")
