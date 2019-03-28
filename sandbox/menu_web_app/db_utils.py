#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEVELOPER: Aimee Ukasick
# DATE CREATED: 31 Aug 2018
# PURPOSE: common functions for retrieving data


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def fetch_all_restaurants():
    session = None
    try:
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        # return all restaurant entries
        items = session.query(Restaurant).order_by(Restaurant.name)
        return items
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
        DBSession = sessionmaker(bind = engine)
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
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
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
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(restaurant)
        session.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
