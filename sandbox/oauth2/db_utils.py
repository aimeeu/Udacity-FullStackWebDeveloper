#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEVELOPER: Aimee Ukasick
# DATE CREATED: 31 Aug 2018
# PURPOSE: common functions for retrieving data


from sqlalchemy import create_engine, sql
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User


def fetch_all_restaurants():
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # return all restaurant entries
        items = session.query(Restaurant).order_by(sql.asc(Restaurant.name))
        return items
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def fetch_first_restaurant():
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # return all restaurant entries
        restaurant = session.query(Restaurant).first()
        return restaurant
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def fetch_restaurant_by_id(restaurant_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return item
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def add_restaurant(name):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_restaurant = Restaurant(name=name)
        session.add(new_restaurant)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def update_restaurant(restaurant_id, name):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
        restaurant.name = name
        session.add(restaurant)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def delete_restaurant(restaurant_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(
            id=restaurant_id).one()
        name = restaurant.name
        session.delete(restaurant)
        session.commit()
        return name
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def fetch_menu_items(restaurant):
    try:
        items = fetch_menu_items_by_id(restaurant.id)
        return items
    except Exception as e:
        print(e)
        raise e


def fetch_menu_items_by_id(restaurant_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).order_by(MenuItem.name)
        return items
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def fetch_menu_item(menu_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return item
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def add_menu_item(menu_item):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(menu_item)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def update_menu_item(edit_item, menu_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        item.name = edit_item.name
        item.description = edit_item.description
        item.price = edit_item.price
        session.add(item)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def delete_menu_item(menu_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(item)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# User Helper Functions
def create_user(login_session):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_user = User(name=login_session['username'], email=login_session[
            'email'], picture=login_session['picture'])
        session.add(new_user)
        session.commit()
        user = session.query(User).filter_by(
            email=login_session['email']).one()
        return user.id
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_user_info(user_id):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_user_id(email):
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
