#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in databases"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database storage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in the database"""
        if cls is not None:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(State).all()
            objects += self.__session.query(City).all()
            objects += self.__session.query(User).all()
            objects += self.__session.query(Place).all()
            objects += self.__session.query(Amenity).all()
            objects += self.__session.query(Review).all()

        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in objects}

    def new(self, obj):
        """Adds new object to storage"""
        self.__session.add(obj)

    def save(self):
        """Saves changes to database"""
        self.__session.commit()

    def reload(self):
        """Creates a new session and reloads data from database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Removes the session"""
        self.__session.close()
