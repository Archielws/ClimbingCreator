import os
import json
from dotenv import load_dotenv
from mistralai import Mistral
import re

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

load_dotenv()
client = Mistral(api_key=api_key)
PROMPT_TEMPLATE = """Generate me a comprehensive list (around 100) of only climbing route descriptions with their grades and name. The descriptions have to be different and should apply to different bouldering. Add some technical moves on a few of them. The name has to be fun (some of them have to be puns but not all) others have to be epic. 
Return the data as a JSON array where each object has exactly this schema:
{
    "name": "string - name of the route",
    "grade": "string - climbing grade (use english (V1, V2,..) sport climbing grades)",
    "description": "string - the full description of the climbing route as in the guidebook"
}
Make sure there are no duplicates.
Do not include any other fields or explanatory text, just the JSON array that can be parsed into a json.loads().
"""

def generate_climbing_routes():
    # Call the OpenAI API to generate the climbing routes
    response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": PROMPT_TEMPLATE,
        },
    ])
    print("Response received from MistralAI API.")

    content = response.choices[0].message.content
    content_clean = re.sub(r'^```json|^```|```$', '', content.strip(), flags=re.MULTILINE).strip()

    # Try parsing the content into JSON
    try:
        routes_data = json.loads(content_clean)
        print("Successfully parsed the response into JSON.")
        
        # Save the data to a file
        with open("climbing_routes.json", "w") as json_file:
            json.dump(routes_data, json_file, indent=2)
        print("Climbing routes data saved to 'climbing_routes.json'.")
    except json.JSONDecodeError:
        print("Failed to parse the response into valid JSON.")
        print("Response was:", content)
        print(type(content))


# Run the function to generate and save the routes data
generate_climbing_routes()

