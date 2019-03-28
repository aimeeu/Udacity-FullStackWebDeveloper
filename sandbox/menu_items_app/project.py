#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEVELOPER: Aimee Ukasick
# DATE CREATED: 10 Sept 2018
# PURPOSE: common functions for retrieving data

import db_utils
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# create instance with name of running application
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def fetch_menu(restaurant_id):
    restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
    items = db_utils.fetch_menu_items(restaurant)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/json')
def fetch_menus_json(restaurant_id):
    restaurant = db_utils.fetch_restaurant_by_id(restaurant_id)
    items = db_utils.fetch_menu_items(restaurant)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def fetch_menu_json(restaurant_id, menu_id):
    item = db_utils.fetch_menu_item(menu_id)
    return jsonify(MenuItem=item.serialize)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = fill_menu_item(request.form, restaurant_id)
        db_utils.add_menu_item(new_item)
        flash("New menu item created")
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    if request.method == 'POST':
        edit_item = fill_menu_item(request.form, restaurant_id)
        db_utils.update_menu_item(edit_item, menu_id)
        flash("Menu item updated")
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        edit_item = db_utils.fetch_menu_item(menu_id)
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=edit_item)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    if request.method == 'POST':
        db_utils.delete_menu_item(menu_id)
        flash("Menu item deleted")
        return redirect(url_for('fetch_menu', restaurant_id=restaurant_id))
    else:
        delete_item = db_utils.fetch_menu_item(menu_id)
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=delete_item)


def fill_menu_item(req_form, restaurant_id):
    new_item = MenuItem(name=req_form['name'],
                        restaurant_id=restaurant_id)
    new_item.description = req_form['desc']
    new_item.price = req_form['price']
    return new_item


if __name__ == '__main__':
    # secret key is used to create sessions for users
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
