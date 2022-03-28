from bottle import post, request, response
import re
import g
import time
import jwt
import mysql.connector

##############################

@post("/users")
def _():
    # VALIDATE
    # first name
    if ( not request.forms.get("user_first_name") 
         or not re.match(g.REGEX_NAME, request.forms.get("user_first_name")) ):
        response.status = 400
        return {"info" : "First name must contain between 2 and 20 characters"}
    user_first_name = request.forms.get("user_first_name")
    
    # last name
    if (not request.forms.get("user_first_name") 
        or not re.match(g.REGEX_NAME, request.forms.get("user_first_name"))):
        response.status = 400
        return {"info" : "Last name must contain between 2 and 20 characters"}
    user_last_name = request.forms.get("user_last_name")
    
    # email
    if (not request.forms.get("user_email")
        or not re.match(g.REGEX_EMAIL, request.forms.get("user_email"))
        or len(request.forms.get("user_email")) > 50):
        response.status = 400
        return {"info" : "Please enter a valid email (max 50 chars)"}
    user_email = request.forms.get("user_email")

    # password
    if (not request.forms.get("user_password")
        or not re.match(g.REGEX_PASSWORD, request.forms.get("user_password"))):
        response.status = 400
        return {"info" : "Please enter a valid password)"}
    user_password = request.forms.get("user_password")

    # Create remaining values
    user_tag = f"{user_first_name}{user_last_name}"
    user_created_at = int(time.time())
    user_updated_at = 0
    
    # User tuple
    user = ( 
        user_first_name, 
        user_last_name, 
        user_email, 
        user_password, 
        user_tag, 
        user_created_at, 
        user_updated_at
    )


    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # INSERT user
        cursor.execute("""INSERT INTO users (user_first_name, user_last_name, 
                user_email, user_password, user_tag, user_created_at, user_updated_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s)""", user)
        db.commit()
        user_id = cursor.lastrowid

        # INSERT session
        cursor.execute("""INSERT INTO sessions (user_id)
                        VALUES(%s)""", (user_id,))
        db.commit()
        session_id = cursor.lastrowid

        # Create jwt to client
        jwt_user = {
            "session_id" : session_id,
            "user_id" : user_id,
            "user_first_name" : user_first_name,
            "user_last_name" : user_last_name,
            "user_email" : user_email,
            "user_tag" : user_tag,
            "user_created_at" : user_created_at,
            "user_updated_at" : user_updated_at
            }

        encoded_jwt = jwt.encode(jwt_user, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt)
        response.status = 200
        return {"info" : f"User width id:{user_id} created"}

    except Exception as ex:
        # If email exist in db
        if "user_email" in str(ex):
            response.status = 400
            return {"info" : "Email already registered" }
        response.status = 500
        return {"info" : "Server error"}

    finally:
        cursor.close()
        db.close()


