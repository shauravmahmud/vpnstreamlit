import streamlit as st

# Access the port information
port = st.server_port

# Display the port
st.write(f"The Streamlit app is running on port {port}")