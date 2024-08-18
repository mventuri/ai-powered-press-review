import requests
import anthropic
import logging

# Set up logging to capture errors in a file named "error.log"
logging.basicConfig(filename="error.log", level=logging.ERROR)

def generate_report(query):
    try:
        # Step 1: Make a GET request to the news API with the given query
        response = requests.get('https://newsapi.org/v2/everything?q=' + query + '&apiKey=<YOUR_API_KEY>')
        
        # Step 2: Parse the JSON response from the API into a Python dictionary
        response_data = response.json()

        # Convert the JSON data to a string format for use in the prompt
        response_data_to_str = str(response_data)

        # Step 3: Initialize the Anthropic client
        client = anthropic.Anthropic()

        # Step 4: Create a prompt for the AI model to generate a financial press review
        prompt = (
            "You are a senior financial journalist tasked with writing a comprehensive press review. "
            "Focus on the key news provided and analyze their potential impact on the financial markets, "
            "specific industries, or relevant companies. Ensure the press review is structured, and concise. "
            "Start the paragraph with the sentence 'This is the press review about " + query + "'. "
            "You'll find the key news in the following json file: " + response_data_to_str
        )

        # Step 5: Use the prompt to create a message with the AI model
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            system=(
                "You are a senior financial journalist. Provide thorough insightful financial press review and advice. "
                "Use technical language where appropriate, and consider the broader economic context in your responses."
            ),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        # Step 6: Extract the generated text from the message response
        plain_text = message.content[0].text

        # Step 7: Append the generated report to a file named "report.txt"
        with open("report.txt", "a") as file:
            file.write(plain_text + "\n")
    
    except requests.exceptions.RequestException as e:
        # Log any HTTP request errors to "error.log"
        logging.error(f"An error occurred during the HTTP request: {e}")
    except Exception as e:
        # Log any unexpected errors to "error.log"
        logging.error(f"An unexpected error occurred: {e}")

# Generate reports for the needed queries
generate_report("finance")
