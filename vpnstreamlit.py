import streamlit as st

# Access the IP address and port information
ip = st.server.server_address[0]
port = st.server.server_address[1]

# Display the IP address and port
st.write(f"The Streamlit app is running at http://{ip}:{port}")