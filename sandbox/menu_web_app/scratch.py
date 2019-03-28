#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def main():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    # return all restaurant entries
    items = session.query(Restaurant).all()
    for item in items:
        print(item.name)

    items = session.query(MenuItem).all()
    for item in items:
        print(item.name)

    # return all restaurant entries
    veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    for vb in veggieBurgers:
        print(vb.id)
        print(vb.price)
        print(vb.restaurant.name)
        print("\n")

    urbanVeggieBurger = session.query(MenuItem).filter_by(id = 9).one()
    print(urbanVeggieBurger.price)

    urbanVeggieBurger.price = '$2.99'
    session.add(urbanVeggieBurger)
    session.commit()

    veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    for vb in veggieBurgers:
        print(vb.id)
        print(vb.price)
        print(vb.restaurant.name)
        print("\n")

    for vb in veggieBurgers:
        if vb.price != '$2.99':
            vb.price = '$2.99'
            session.add(vb)
            session.commit()

    spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
    print(spinach.restaurant.name)
    session.delete(spinach)
    session.commit()


# Call to main function to run the program
if __name__ == "__main__":
    main()