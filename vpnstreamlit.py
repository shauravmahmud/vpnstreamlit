import os
import streamlit as st

# Access the port information
port = os.environ.get("PORT", "Not found")

# Display the port
st.write(f"The Streamlit app is running on port {port}")