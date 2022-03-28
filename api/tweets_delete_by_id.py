from bottle import delete, response
import g
import os
import mysql.connector

##############################

@delete("/tweets/<tweet_id>")
def _(tweet_id):
    # VALIDATE

    # Session valid?
    if not g.IS_VALID_SESSION_API:
        response.status = 400
        return {"info": "No valid session"}
    session_user_id = g.GET_DECODED_JWT()["user_id"]

    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor()

        # Get tweet_image
        cursor.execute("""SELECT tweet_image FROM tweets
                        WHERE tweet_id = %s""", (tweet_id,))
        tweet_image = cursor.fetchone()[0]

        # Delete tweet from db
        cursor.execute("""DELETE FROM tweets
                        WHERE tweet_id = %s AND tweet_user_id = %s""", (tweet_id, session_user_id))
        db.commit()
        counter = cursor.rowcount
        # Tweet not found
        if not counter:
            response.status = 400
            return {"info" : f"User doesn't own any tweets with id: {tweet_id}"}
        
        # Delete img from server
        if tweet_image:
            os.remove(f"assets/images/{tweet_image}")

        response.status = 200
        return {"info" : f"Tweet with id: {tweet_id} deleted"}

    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Server error"}

    finally:
        cursor.close()
        db.close()