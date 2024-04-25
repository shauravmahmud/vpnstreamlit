import streamlit as st
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler
import os
from tornado.httpserver import HTTPServer

# Streamlit app
def main():
    st.title("Streamlit with Tornado Server")
    st.write("This is a Streamlit app running with a Tornado server.")

# Define Tornado RequestHandler
class MainHandler(RequestHandler):
    def get(self):
        self.write("This is the Tornado MainHandler")

# Define Tornado WebSocketHandler
class WebSocketEchoHandler(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(f"You said: {message}")

    def on_close(self):
        print("WebSocket closed")

# Tornado Application
def make_tornado_app():
    return Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketEchoHandler),
    ])

if __name__ == "__main__":
    # Start Streamlit app
    main()

    # Start Tornado server
    port = int(os.environ.get("PORT", 8888))
    tornado_app = make_tornado_app()
    http_server = HTTPServer(tornado_app)
    http_server.listen(port)
    IOLoop.current().start()
