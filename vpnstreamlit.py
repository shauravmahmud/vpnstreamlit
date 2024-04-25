import socket
import streamlit as st
import requests
import subprocess
import threading
import tornado.ioloop
import tornado.web

# Tornado handlers
class ConnectVPNHandler(tornado.web.RequestHandler):
    def post(self):
        # Logic to start OpenVPN connection
        subprocess.run(["sudo", "openvpn", "--config", "your_vpn_config.ovpn"])
        self.write("VPN connected")

class DisconnectVPNHandler(tornado.web.RequestHandler):
    def post(self):
        # Logic to stop OpenVPN connection
        subprocess.run(["sudo", "pkill", "openvpn"])
        self.write("VPN disconnected")

def find_open_port(start_port=1043, end_port=65535):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                pass
    return None

def make_app():
    return tornado.web.Application([
        (r"/connect-vpn", ConnectVPNHandler),
        (r"/disconnect-vpn", DisconnectVPNHandler),
    ])

# Start Tornado server in a separate thread
def run_tornado():
    tornado_port = find_open_port()
    if tornado_port:
        app = make_app()
        app.listen(tornado_port)
        print(f"Tornado server started on port {tornado_port}")
        tornado.ioloop.IOLoop.current().start()
    else:
        print("No open ports available.")

tornado_thread = threading.Thread(target=run_tornado)
tornado_thread.start()

# Streamlit app
def main():
    st.title("Streamlit VPN Manager")

    # Sidebar menu
    menu = ["Home", "Connect to VPN", "Disconnect from VPN"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the Streamlit VPN Manager!")

    elif choice == "Connect to VPN":
        st.subheader("Connect to VPN")
        if st.button("Connect"):
            # Call API to connect to VPN
            response = requests.post(f"http://localhost:{tornado_port}/connect-vpn")
            st.write(response.text)

    elif choice == "Disconnect from VPN":
        st.subheader("Disconnect from VPN")
        if st.button("Disconnect"):
            # Call API to disconnect from VPN
            response = requests.post(f"http://localhost:{tornado_port}/disconnect-vpn")
            st.write(response.text)

if __name__ == '__main__':
    main()
