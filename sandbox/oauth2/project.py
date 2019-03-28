#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEVELOPER: Aimee Ukasick
# DATE CREATED: 10 Sept 2018
# PURPOSE: common functions for retrieving data

import db_utils
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify
from flask import session
from flask import make_response
import random, string
import httplib2
import json
import requests
import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# create instance with name of running application
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu"


# login
# Create a state token to prevent request forgery
# Store token in the session for later validation
@app.route('/login')
def show_login():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(32))
    session['state'] = state
    print("The current session state is {}".format(session['state']))
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dump('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # obtain authorization code
    code = request.data

    try:
        scopes = ['https://www.googleapis.com/auth/userinfo.email',
                 'https://www.googleapis.com/auth/userinfo.profile']
        # oauth_flow = flow_from_clientsecrets('client_secret.json', scope='') - does not return name
        oauth_flow = flow_from_clientsecrets('client_secret.json',scopes)
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError as fee:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        logging.error(fee)
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={' \
          '}'.format(access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    # userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    # userinfo_url = "https://www.googleapis.com/userinfo/v2/me"
    # calls to the above endpoints DO NOT RETURN NAME
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    session['picture'] = data['picture']
    session['email'] = data['email']
    session['username'] = data['name']



    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;"> '
    flash("You are now logged in as {}".format(session['username']))
    print("done!")
    return output


# revoke a current user's token and reset the session
# https://developers.google.com/identity/protocols/OAuth2WebServer
@app.route('/gdisconnect')
def gdisconnect():
    access_token = session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is {}'.format(access_token))
    # print('Username {} | email ) is {}'.format(session['username'], session['email']))
   # url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
    #    session['access_token'])
   # h = httplib2.Http()
   # result = h.request(url, 'GET')[0]
    result = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': access_token},
                           headers={
                               'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(result, 'status_code')
    if status_code == 200:
        empty_session_variables()
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    elif status_code == 400:
        empty_session_variables()
        dict = {"response_code": 400,
                "message": result.text}
        response = make_response(json.dumps(dict))
        response.headers['Content-Type'] = 'application/json'
    else:
        dict = {"response_code": status_code,
                "message": result.text}
        response = make_response(json.dumps(dict))
        response.headers['Content-Type'] = 'application/json'
    return response


def empty_session_variables():
    session.pop('access_token', None)
    session.pop('gplus_id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('picture', None)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received {}".format(access_token))


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    # The token must be stored in the session in order to properly logout
    session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += session['username']

    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must me included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"





# JSON APIs to view Restaurant Information
@app.route('/restaurant/<int:restaurant_id>/menu/json')
def fetch_restaurant_menu_json(restaurant_id):
    restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
    items = db_utils.fetch_menu_items(restaurant)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json')
def fetch_menu_item_json(restaurant_id, menu_id):
    item = db_utils.fetch_menu_item(menu_id)
    return jsonify(MenuItem=item.serialize)


@app.route('/restaurant/json')
def fetch_restaurants_json():
    restaurants = db_utils.fetch_all_restaurants()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/')
@app.route('/restaurant/')
def fetch_restaurants():
    restaurants = db_utils.fetch_all_restaurants()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        db_utils.add_restaurant(name)
        flash('New Restaurant {} Successfully Created'.format(name))
        return redirect(url_for('fetch_restaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            db_utils.edit_restaurant(restaurant_id, name)
            flash('Restaurant Successfully Edited {}'.format(name))
            return redirect(url_for('fetch_restaurants'))
    else:
        restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
        return render_template('editrestaurant.html', restaurant=restaurant)


# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = db_utils.delete_restaurant(restaurant_id)
        flash('{} Successfully Deleted'.format(name))
        return redirect(url_for('fetch_restaurants'))
    else:
        restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
        return render_template('deleterestaurant.html', restaurant=restaurant)


# Show a restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def fetch_menu(restaurant_id):
    restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
    items = db_utils.fetch_menu_items_by_id(restaurant_id)
    return render_template('menu.html', items=items,
                           restaurant_id=restaurant_id,
                           restaurant=restaurant)


# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        new_item = fill_menu_item(request.form, restaurant_id)
        name = new_item.name
        db_utils.add_menu_item(new_item)
        flash("New menu item {} successfully created".format(name))
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        item = fill_menu_item(request.form, restaurant_id)
        db_utils.update_menu_item(item, menu_id)
        flash('Menu Item {} Successfully Edited'.format(item.name))
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        edit_item = db_utils.fetch_menu_item(menu_id)
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=edit_item)


# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        db_utils.delete_menu_item(menu_id)
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        delete_item = db_utils.fetch_menu_item(menu_id)
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=delete_item)


def fill_menu_item(req_form, restaurant_id):
    item = MenuItem(name=req_form['name'], restaurant_id=restaurant_id)
    if request.form['description']:
        item.description = request.form['description']
    if request.form['price']:
        item.price = request.form['price']
    if request.form['course']:
        item.course = request.form['course']
    return item


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
