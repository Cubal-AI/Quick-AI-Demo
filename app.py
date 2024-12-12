import requests
import streamlit as st

# Set up the Flask backend URL
FLASK_BACKEND_URL = "https://freyt-ai-backend-prod-gxcjgqh4bhedgzex.centralindia-01.azurewebsites.net/chat"

# Streamlit App UI
st.title("Freight AI - Chat Assistant")

# Store chat messages in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Welcome to Freight AI. I am Elsa. How can I assist you today?"):
    # Append user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Send user input to the Flask backend and get the response
        payload = {
            "user_id": "user_test",
            "chat_id": "chat_test",
            "user_input": prompt,
        }
        response = requests.post(
            FLASK_BACKEND_URL,
            json=payload
        )
        
        # Check for valid response from the Flask server
        if response.status_code == 200:
            response_data = response.json()
            # assistant_response = response_data
            assistant_response = response_data.get("assistant_response", "Sorry, I couldn't process your request.")
        else:
            assistant_response = f"Error: {response.status_code}"

    except Exception as e:
        assistant_response = f"Request failed: {str(e)}"

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Append assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
