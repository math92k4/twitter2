from time import process_time_ns
from bottle import post, request, response
import re
import g
import jwt
import mysql.connector


##############################

@post("/sessions")
def _():
    # VALIDATE
    # user_mail
    if (not request.forms.get("user_email")
        or not re.match(g.REGEX_EMAIL, request.forms.get("user_email"))):
        response.status = 400
        return {"info" : "user_email"}
    user_email = request.forms.get("user_email")

    # user_password
    if (not request.forms.get("user_password")
        or not re.match(g.REGEX_PASSWORD, request.forms.get("user_password"))):
        response.status = 400
        return {"info" : "user_password"}
    user_password = request.forms.get("user_password")

 
    try:
        # CONNECT TO DB
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor(dictionary = True)

        # Find matching user & get column names and values
        # TODO - join session-id and use the same if exist
        cursor.execute("""SELECT * FROM users
                        WHERE user_email = %s 
                        AND user_password = %s""", (user_email, user_password))
        user = cursor.fetchone()

        # If no values are returned
        if not user:
            response.status = 400
            return {"info" : "Wrong email or password"}
        
        # Create session
        user_id = user["user_id"]
        cursor.execute("""INSERT INTO sessions (user_id) VALUES(%s)""", (user_id,))
        db.commit()
        session_id = cursor.lastrowid

        # Insert session_id to users
        user["session_id"] = session_id

        # Create jwt
        encoded_jwt = jwt.encode(user, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt)
        response.status = 200
        return {"info" : "jwt created"}

    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info" : "Server error" }
    
    finally:
        cursor.close()
        db.close()




    
