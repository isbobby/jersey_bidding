import os

#config database uri here
class Config:
    SECRET_KEY = 'c9970460fc2c3ad324add53c94e3bc2a'
    #SQLALCHEMY_DATABASE_URI = 'postgres://bobby:zmq,bs2008@localhost:5432/jersey_bidder'
    #SQLALCHEMY_DATABASE_URI = 'postgres://postgres:password@localhost:5432/jersey_bidder'
    SQLALCHEMY_DATABASE_URI = 'postgres://nzlujsgydsuhub:3c28336b8b39e40c0a6a62c1d2c60cfdee2c169319d7ab6f67f280d60bbaa3b3@ec2-54-235-96-48.compute-1.amazonaws.com:5432/dd653s303qd6jm'
    USER_APP_NAME = "Jersey Bidder"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

#User
#login 

#main
#static faq page

#Jersey
#submit preference 
#view

#bob 2/9
#faq -> login -> view -> submit (validate) -> view -> logout -> view

#csv
#excel work book

#scripts
#generate pw -> send email

#load to DB

#website
#####separate login windows and limit login

#publish result

#scan db for jersey bidding clean up - pick up room number and export as csv

#result -> export csv (user + jersey)

#host backend at 172....