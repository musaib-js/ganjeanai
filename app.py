import streamlit as st
from QueryClassification import classify_and_extract, extract_indian_phone_and_order_numbers
from ResponseSynthesis import synthesize_response

new_classes = ["new test", "new order", "new appointment"]

detail_classes = ["get test report", "get appointment details", "get order details"]

foul_classes = ["foul"]



# Placeholder function for Gemini chatbot response
def chatbot_response(user_input):
    classification, warning = classify_and_extract(user_input)
    phone_numbers, order_numbers = extract_indian_phone_and_order_numbers(user_input)
    phone_number = phone_numbers[0] if phone_numbers else None
    order_number = order_numbers[0] if order_numbers else None  
    
    if classification in new_classes and not phone_number:
        response = synthesize_response(user_input, details="To book a new appointment/test/order please provide your phone number.")
        return response
    elif classification in detail_classes and not order_number:
        response = synthesize_response(user_input, details="To get details, please provide your order number.")
        return response
    elif classification in new_classes and phone_number:
        response = synthesize_response(user_input, details="Appointment/Order/Test booked successfully. Your phone number is: " + phone_number)
        return response
    elif classification in detail_classes and order_number:
        mock_test_report = {
            "Test Name": "Blood Test",
            "Test Date": "2022-01-01",
            "Collection Date": "2022-01-01",
            "Collection Time": "09:00 AM",
            "Collected By": "Sahil Sadiq",
            "Collected At": "Home",
            "Test Result": "Normal",
            "Test Center": "Ganjean Health, Sopore"
        }
        
        mock_order_details = {
            "Order ID": "GAN1234567890",
            "Order Date": "2022-01-01",
            "Order Status": "Delivered",
            "Order Items": [
                {
                    "Item Name": "PCM-500",
                    "Item Quantity": 1,
                    "Item Price": 500
                },
                 {
                    "Item Name": "Pantop 40",
                    "Item Quantity": 5,
                    "Item Price": 500
                }
            ],
            "Total Amount": 1000
        }
        
        mock_appointment_details = {
            "Appointment ID": "GAN1234567890",
            "Appointment Date": "2022-01-01",
            "Appointment Time": "09:00 AM",
            "Appointment Status": "Confirmed",
            "Appointment Center": "Ganjean Health, Sopore"
        }
        details = mock_test_report if classification == "get test report" else mock_order_details if classification == "get order details" else mock_appointment_details
        response = synthesize_response(user_input, details=details)
        return response
    if warning:
        return synthesize_response(user_input, details=warning)
    else:
        return classification

# Streamlit app
st.title("Ganjean Health Chatbot")
st.write("Welcome to Ganjean AI! How can I help you today?")

# User input text area
user_input = st.text_input("You:", key="user_input")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "text": user_input})
    # Get chatbot response
    response = chatbot_response(user_input)
    # Append chatbot response
    st.session_state.messages.append({"role": "bot", "text": response})

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Ganjean AI** {msg['text']}")
