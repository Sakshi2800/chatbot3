import streamlit as st
import os
import requests

def get_groq_response(prompt):
    """
    Fetches a response from the Groq API, handling potential errors gracefully.

    Args:
        prompt (str): The user's input message.

    Returns:
        str: The chatbot's response, or an informative error message.
    """

    API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Groq API endpoint
    API_KEY = "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" # Use an environment variable for the API key

    if not API_URL or not API_KEY:
        st.error("Please set the GROQ_API_URL and GROQ_API_KEY environment variables.")
        return "Error: Missing environment variables."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",  # Replace with your model name
        "messages": [
            {"role": "system", "content": (
                "You are a thoughtful and empathetic chatbot named Buddy. Provide concise, supportive responses that are encouraging and helpful. "
                "Offer emotional support when needed, and maintain a warm and understanding tone. Balance being uplifting with being practical, "
                "so users feel supported without it being overly sentimental."
            )},
            {"role": "user", "content": prompt}
        ],
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "I'm here to help. Please share more.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the Groq API: {e}")
        return f"An error occurred: {e}"

def main():
    """
    Streamlit app to handle user interaction and chatbot responses.
    """
    st.title("Chat with Buddy")

    user_message = st.text_input("What's on your mind?")

    if user_message:
        bot_response = get_groq_response(user_message)
        st.write(f"**Buddy:** {bot_response}")

if __name__ == "__main__":
    main()