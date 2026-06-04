import http.server
import socketserver
import threading
from fastapi import FastAPI, Request
import uvicorn

def serveur():
    class ThreadedHTTPServer(threading.Thread):
        def run(self):
            port = 8080
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("",port),handler) as tcp_server:
                tcp_server.serve_forever()
                
    server_thread = ThreadedHTTPServer()
    server_thread.daemon = True
    server_thread.start()

    app = FastAPI()
    @app.get("/ping")
    async def root(request: Request):
        my_header = request.headers
        return {"message": my_header}
    
    uvicorn.run(app, host="127.0.0.1", port=8081)

serveur()

