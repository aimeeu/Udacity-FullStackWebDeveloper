#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("metho do_GET")
        form_html = self.get_form_body()
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Hello!</h1>"
            message += form_html
            message += "</body></html>"
            print("MESSAGE={}".format(message))
            self.wfile.write(bytes(message, "utf-8"))
            return
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Hola!</h1>"
            message += form_html
            message += "</body></html>"
            print("MESSAGE={}".format(message))
            self.wfile.write(bytes(message, "utf-8"))
            return
        else:
            self.send_error(404, 'File Not Found: {}'.format(self.path))

    def do_POST(self):
        print("method do_POST")
        form_html = self.get_form_body()
        try:
            self.send_response(200)
            self.end_headers()

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            user_text = form.getvalue('message')
            output = ""
            output += "<html><body>"
            output += "<h1>Okay, how about this:</h1>"
            output += "<h2>{}</h2>".format(user_text)
            output += form_html
            output += "<html><body>"
            print("OUTPUT={}".format(output))
            self.wfile.write(bytes(output, "utf-8"))
        except Exception as e:
            print(e)


    @staticmethod
    def get_form_body():
        form_body = (
            "<form method='POST' enctype='multipart/form-data' "
            "action='/hello'>"
            "<h2>What would you like to say?</h2> "
            "<input name='message' type='text'>"
            "<input type='submit' value='Submit'></form >"
        )
        return form_body


def main():
    try:
        port = 9080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        # sudo kill $(sudo lsof -t -i:9080)
        server.socket.close()
        # added server.server_close() because port was still open
        server.server_close()


if __name__ == '__main__':
    main()