import streamlit as st
from transformers import pipeline
import json

# Load configuration
with open("config.json") as f:
    config = json.load(f)

# Initialize the Hugging Face pipeline
generator = pipeline('text-generation', model=config["model_name"])

# Function to generate a personalized response using the Hugging Face model
def generate_personalized_response(customer_info, query, max_length=100):
    prompt = (
        f"Customer Name: {customer_info['name']}\n"
        f"Preferences: {customer_info['preferences']}\n"
        f"Interaction History: {customer_info['interaction_history']}\n\n"
        f"Engagement Query: {query}\n"
        f"Provide a personalized engagement message based on the above information."
    )
    response = generator(prompt, max_length=max_length, num_return_sequences=1)
    return response[0]['generated_text']

# Streamlit UI
st.title("Personalized Customer Engagement")

# Select customer
customer_ids = list(config["customers"].keys())
selected_customer_id = st.selectbox("Select Customer", customer_ids)
customer_info = config["customers"][selected_customer_id]

# Display customer details
st.write(f"Customer Name: {customer_info['name']}")
st.write(f"Preferences: {customer_info['preferences']}")
st.write(f"Interaction History: {customer_info['interaction_history']}")

# Enter engagement query
query = st.text_input("Enter your engagement query:")

# Generate response
if st.button("Generate Response"):
    if query:
        response = generate_personalized_response(customer_info, query)
        st.write("AI Response:", response)
    else:
        st.write("Please enter an engagement query.")
