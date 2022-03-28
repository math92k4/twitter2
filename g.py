from typing import final
from unittest import result
from bottle import request, redirect, response
import jwt
import g
import mysql.connector

##############################

# REGEX
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$"
REGEX_NAME = '^[A-Za-z]{2,20}$'

# SECRETS
JWT_SECRET = "THISkeyISIpossibleToGet123321123"

# DB CONFIGURATION
try:
    # Prod
    import production
    DB_CONFIG = {
        "host" : "",
        "user" : "",
        "password" : "",
        "database" : ""
    }
except:
    # Dev
    DB_CONFIG = {
        "host" : "localhost",
        "user" : "root",
        "port" : "8889",
        "password" : "root",
        "database" : "twittermanda2"
    }

##############################

def IS_VALID_SESSION_ROUTES():
    # No jwt
    if not request.get_cookie("jwt"):
        return False

    # Get jwt
    decoded_jwt = GET_DECODED_JWT()

    # Jwt not valid
    if decoded_jwt == False:
        return redirect("/sign-out")
    
    # Is session in db
    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        session = (decoded_jwt["session_id"], decoded_jwt["user_id"])
        cursor.execute("""SELECT * FROM sessions
                        WHERE session_id = %s AND user_id = %s""", session)
        if not cursor.fetchone():
            return redirect("/sign-out")
        
        # Succes
        return True

    except Exception as ex:
        print(ex)
        response.status = 500
        return redirect("/sign-out")
    
    finally:
        cursor.close()
        db.close()


##############################

def IS_VALID_SESSION_API():
    # No jwt
    if not request.get_cookie("jwt"):
        return False

    # Get jwt
    decoded_jwt = GET_DECODED_JWT()

    # Jwt not valid
    if decoded_jwt == False:
        return False
    
    # Is session in db
    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        session = (decoded_jwt["session_id"], decoded_jwt["user_id"])
        cursor.execute("""SELECT * FROM sessions
                        WHERE session_id = %s AND user_id = %s""", session)
        if not cursor.fetchone():
            return False
        
        # Succes
        return True

    except Exception as ex:
        print(ex)
        response.status = 500
        return False
    
    finally:
        cursor.close()
        db.close()


##############################

def GET_DECODED_JWT():
    encoded_jwt = request.get_cookie("jwt")
    decoded_jwt = jwt.decode(encoded_jwt, g.JWT_SECRET, algorithms=["HS256"])
    return decoded_jwt






