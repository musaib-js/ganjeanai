import google.generativeai as genai
import re
import dotenv
import os

dotenv.load_dotenv()


key = os.getenv("API_KEY")

genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt_template = """
You are a query classifier. Your task is to classify user queries into one or more of the following categories: "new test", "new order", "new appointment", "get test report", "get appointment details", "get order details", "foul".

You must output the classifications only, if multiple, output comma separated classifications:

Classification: <classification(s) separated by commas if multiple>

Do not include any other text or explanations.

**If the query includes foul language, warn the user politely**

Here are some examples:

User Query: I want to book a new test
Classification: new test
Order Number: None
Phone Number: None

User Query: Can I see my appointment details?
Classification: get appointment details

User Query: I need to order something new
Classification: new order

User Query: I want to book a new appointment and also order something
Classification: new appointment, new order

User Query: I need to see my test results
Classification: get test report

User Query: I want to know the details of my order GAN1234567890
Classification: get order details

User Query: I want to schedule a new test and see my previous test report
Classification: new test, get test report

User Query: I want to book a new appointment
Classification: new appointment

User Query: I want to see my order details
Classification: get order details

User Query: I want to order a new test and my phone number is 1234567890
Classification: new test, new order

User Query: I want to see my appointment
Classification: get appointment details

User Query: I want to see my test report
Classification: get test report

User Query: I want to order something
Classification: new order

User Query: I want to know the status of my order GAN9876543210 and my phone number is 0987654321
Classification: get order details

User Query: I want to book a new appointment and my phone number is 1112223333
Classification: new appointment

User Query: I want to see my order details for GAN1122334455
Classification: get order details

User Query: Do hell with you
Classification: foul
Warning: Please refrain from using foul language in your queries.

User Query: {user_query}
Classification:
"""

def classify_and_extract(user_query):
    prompt = prompt_template.format(user_query=user_query)
    response = model.generate_content(prompt)
    output = response.text.strip()


    classification_match = re.search(r"Classification: (.*)", output)
    warning_match = re.search(r"Warning: (.*)", output)

    classification = classification_match.group(1).strip() if classification_match else "None"
    warning = warning_match.group(1).strip() if warning_match else "None"

    return classification, warning

def extract_indian_phone_and_order_numbers(text):
    phone_regex = r'\b[6-9]\d{9}\b'

    order_regex = r'GANH(?:[-.\s]*\d){10}'

    phone_numbers = re.findall(phone_regex, text)

    order_numbers = [re.sub(r'[^a-zA-Z\d]', '', match) for match in re.findall(order_regex, text)]

    return phone_numbers, order_numbers
