from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do get")
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        for i in range(0, 100, 1):
            self.wfile.write(bytes("event: onProgress\n", "utf-8"))

            data = {"progress": i}
            self.wfile.write(bytes(f"data: {json.dumps(data)}\n", "utf-8"))

            self.wfile.write(bytes(f"id: {i}\n", "utf-8"))
            self.wfile.write(bytes("\n", "utf-8"))
            self.wfile.flush()

            print("progress", i)
            time.sleep(1)
        
        self.wfile.write(bytes("event: done\n", "utf-8"))
        
        self.wfile.write(bytes("data: {}\n", "utf-8"))
        self.wfile.write(bytes(f"id: 100\n", "utf-8"))
        self.wfile.write(bytes("\n", "utf-8"))
        self.wfile.flush()
        print("done")


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
