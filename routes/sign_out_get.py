from bottle import get, redirect, request, response
import jwt
import g
import mysql.connector

##############################

@get("/sign-out")
def _():
    if not request.get_cookie("jwt"):
        return redirect("/sign-in")
    encoded_jwt = request.get_cookie("jwt")
    decoded_jwt = decoded_jwt = jwt.decode(encoded_jwt, g.JWT_SECRET, algorithms=["HS256"])
    session_id = decoded_jwt["session_id"]

    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor()
        cursor.execute("""DELETE FROM sessions
                        WHERE session_id = %s""", (session_id,))
        db.commit()
        
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info" : "Server error"}

    finally:
        cursor.close()
        db.close()

    response.set_cookie("jwt", encoded_jwt, expires=0)
    return redirect("/sign-in")