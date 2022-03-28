from bottle import post, request, response
import g
import time
import json
import os
import uuid
import imghdr
import mysql.connector

##############################

@post("/tweets")
def _():
    # VALIDATE SESSION
    if not g.IS_VALID_SESSION_API():
        response.satus = 400
        return {"info" : "Session not valid"}
    
    # get user_id
    user = g.GET_DECODED_JWT()
    tweet_user_id = user["user_id"]

    # VALIDATE FORM
    # Tweet text
    if (not request.forms.get("tweet_text") 
        or not request.forms.get("tweet_text").strip()):
        response.status = 400
        return {"info" : "tweet_text must contain min 1 and max 255 characters"}
    tweet_text = request.forms.get("tweet_text").strip()

    # Tweet image (optional)
    tweet_image = None
    if request.files.get("tweet_image"):
        image = request.files.get("tweet_image")

        # Get file extension
        file_name, file_extension = os.path.splitext(image.filename)

        # Validate extension
        if file_extension not in (".png", ".jpeg", "jpg"):
            response.status = 400
            return f"Filetype: {file_extension} not allowed"

        # Make .jpg = .jpeg for imghdr validation
        if file_extension == ".jpg":
            file_extension = ".jpeg"
        
        # Create new db-friendly file-name
        image_id = str(uuid.uuid4())
        tweet_image = f"{image_id}{file_extension}"

        # Save image in images dir
        image.save(f"assets/images/{tweet_image}")

        # Validate that the file is not manipulated (post upload)
        imghdr_extension = imghdr.what(f"assets/images/{tweet_image}")
        if not file_extension == f".{imghdr_extension}":
            os.remove(f"assets/images/{tweet_image}")
            response.status = 400
            return "File manipulated. This is not an image.."

    # Time stamps
    tweet_created_at = int(time.time())
    tweet_updated_at = 0

    # Tweet tuple
    tweet_tuple = (
        tweet_text,
        tweet_image,
        tweet_created_at,
        tweet_updated_at,
        tweet_user_id
    )

    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor(dictionary = True)

        # INSERT tweet
        cursor.execute("""INSERT INTO tweets (tweet_text, tweet_image, tweet_created_at, tweet_updated_at, tweet_user_id)
                        VALUES(%s, %s, %s, %s, %s)""", tweet_tuple)
        db.commit()
        tweet_id = cursor.lastrowid

        # SELECT created tweet
        cursor.execute("""SELECT tweet_id, tweet_text, tweet_image, tweet_created_at, 
                        tweet_updated_at, tweet_user_id, user_first_name, user_last_name, user_tag 
                        FROM tweets 
                        JOIN users
                        WHERE tweet_id = %s AND user_id = tweet_user_id""", (tweet_id,))
        tweet = cursor.fetchone()

        # Succes
        response.status = 200
        return json.dumps(tweet)


    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info" : "Server error"}
    
    finally:
        cursor.close()
        db.close()









