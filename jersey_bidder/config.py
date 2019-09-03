import os

#config database uri here
class Config:
    SECRET_KEY = 'c9970460fc2c3ad324add53c94e3bc2a'
    # SQLALCHEMY_DATABASE_URI = 'postgres://bobby:zmq,bs2008@localhost:5432/jersey_bidder'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:password@localhost:5432/jersey_bidder'
