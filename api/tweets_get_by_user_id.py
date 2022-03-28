from bottle import get, response
import mysql.connector
import g
import json

##############################

@get("/tweets/by-user/<user_id>")
def _(user_id):

    print("#"*30)
    print(user_id)
    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor(dictionary=True)

        cursor.execute("""SELECT tweet_id, tweet_text, tweet_image, tweet_created_at, 
                        tweet_updated_at, tweet_user_id, user_first_name, user_last_name, user_tag 
                        FROM tweets 
                        JOIN users 
                        WHERE user_id = tweet_user_id AND user_id = %s
                        ORDER BY tweet_created_at DESC""", (user_id,))
        tweets = cursor.fetchall()
        
        return json.dumps(tweets)

    except Exception as ex:
        print(ex)
        response.status = 500
        return { "info" : "Server error"}

    finally:
        cursor.close()
        db.close()


