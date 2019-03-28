#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from database_setup import Restaurant, Base, MenuItem
import db_utils


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("method do_GET")
        try :
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = db_utils.fetch_all_restaurants()
                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='restaurants/{}/edit'>Edit </a> ".format(restaurant.id)
                    output += "</br>"
                    output += "<a href ='restaurants/{}/delete'> Delete </a>".format(restaurant.id)
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create a New Restaurant</h1>"
                output += self.get_new_restaurant_form_body()
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            elif self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurant.name
                    output += "</h1>"
                    output += self.get_edit_restaurant_form_body(restaurant)
                    output += "</body></html>"
                    self.wfile.write(bytes(output, "utf-8"))
            elif self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete {}?".format(restaurant.name)
                    output += "</h1>"
                    output += self.get_delete_restaurant_form_body(restaurant)
                    output += "</body></html>"
                    self.wfile.write(bytes(output, "utf-8"))
            else:
                self.send_error(404, 'File Not Found: {}'.format(self.path))
        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             })
                new_restaurant_name = form.getvalue('newRestaurantName')
                db_utils.add_restaurant(new_restaurant_name)
                # redirect response to restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            elif self.path.endswith("/edit"):
                # get restaurant id
                restaurant_id = self.path.split("/")[2]
                # get updated restaurant name
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             })
                updated_name = form.getvalue('newRestaurantName')
                db_utils.update_restaurant(restaurant_id, updated_name)
                # redirect to restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            elif self.path.endswith("/delete"):
                # get restaurant id
                restaurant_id = self.path.split("/")[2]
                db_utils.delete_restaurant(restaurant_id)
                # redirect to restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        except Exception as e:
            print(e)
            self.send_error(500, 'Something went wrong: {}'.format(e))

    def get_new_restaurant_form_body(self):
        form_body = (
            "<form method='POST' enctype='multipart/form-data' "
            "action='/restaurants/new'>"
            "<input name = 'newRestaurantName' type = 'text' "
            "placeholder = 'New Restaurant Name' > "
            "<input type='submit' value='Create'>"
            "</form>"
        )
        return form_body

    def get_edit_restaurant_form_body(self, restaurant):
        form_body = (
            "<form method='POST' enctype='multipart/form-data' "
            "action='/restaurants/{}/edit'>"
            "<input name = 'newRestaurantName' type = 'text' "
            "placeholder = '{}' > "
            "<input type='submit' value='Rename'>"
            "</form>"
        )
        return form_body.format(restaurant.id, restaurant.name)

    def get_delete_restaurant_form_body(self, restaurant):
        form_body = (
            "<form method='POST' enctype='multipart/form-data' "
            "action='/restaurants/{}/delete'>"
            "<input type='submit' value='Delete'>"
            "</form>"
        )
        return form_body.format(restaurant.id)


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