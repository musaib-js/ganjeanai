import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()


key = os.getenv("API_KEY")

genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash")

response_template = """
You are a response synthesizer. Your task is to generate a response to a user query based on the classification of the query. You must output the response only, without any additional text or explanations.
Please do not hallucinate or generate inappropriate responses.

**If the query includes foul language, warn the user politely**

Please follow the below instructions:

1. If you are given some order details as JSON, generate a response with the order details as a table that can be perfectly rendered by any UI.
2. If you are given some appointment details as JSON, generate a response with the appointment details as a table that can be perfectly rendered by any UI.
3. If you are given some test report details as JSON, generate a response with the test report details as a table that can be perfectly rendered by any UI.
4. If you are given a phone number, generate a response with the phone number.
5. Please generate a polite response if the query includes foul language.
6. At the end of the response, ask the user if they need any further assistance.
7. Start the response with "Here are the details you requested:" if the user has requested for some information followed by the generated response with two line breaks.
8. If the user just says "Hi" or "Hello", respond with "Hello! How can I help you today?".

User Query: {user_query}
Details: {details}
Response:
"""

def synthesize_response(user_query, details="None"):
    prompt = response_template.format(user_query=user_query, details=details)
    response = model.generate_content(prompt)
    output = response.text.strip()
    return output
