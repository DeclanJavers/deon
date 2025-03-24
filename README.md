# Deon - Personal Assistant (Work in Progress)

## Overview

Deon is a modular personal assistant system designed to understand natural language commands and route them to appropriate functions. The project aims to integrate various capabilities including voice recognition, smart home control, web automation, and messaging.

**Note: This project is currently under active development and is not complete.**

## Current Features

- **Function Finder**: Maps natural language commands to appropriate functions using Google's Gemini AI
- **Response Caching**: Stores previously processed commands and responses in a CSV file for faster retrieval
- **Modular Design**: Functions are defined in a CSV file, making it easy to add new capabilities

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deon.git
   cd deon
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Gemini API key:
   - Get an API key from [Google AI Studio](https://ai.google.dev/)
   - Replace the placeholder API key in functionFinder.py

## Configuration

1. Create a list_of_commands.csv file with the following columns:
   - `name`: Function name
   - `description`: What the function does
   - `example_commands`: Example commands that trigger this function (comma-separated)

2. Create a text_files directory with:
   - `function_finder.txt`: Instructions for the AI
   - `latest_command.txt`: Storage for the most recent command
   - `latest_function.txt`: Storage for the most recent function identified

## Usage

To test the function finder:

```bash
python functionFinder.py
```

## Planned Features

Based on the requirements, Deon will eventually include:

- Voice recognition and text-to-speech capabilities
- Smart home device control
- Web browsing and automation
- Image recognition and OCR
- Telegram messaging integration
- Custom skills and extensibility

## Project Structure

```
deon/
├── functionFinder.py        # Main function matching logic
├── list_of_commands.csv     # Available functions and their descriptions
├── responses.csv            # Cache of previous commands and responses
├── requirements.txt         # Project dependencies
└── text_files/              # Text resources for the assistant
    ├── function_finder.txt  # Instructions for the AI
    ├── latest_command.txt   # Most recent command
    └── latest_function.txt  # Most recent function identified
```

## Security Note

- Never commit API keys to version control
- Use environment variables or a secure configuration file for sensitive information

## License

MIT License