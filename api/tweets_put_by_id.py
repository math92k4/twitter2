from bottle import put, response, request
import g
import os
import uuid
import imghdr
import time
import json
import mysql.connector

##############################

@put("/tweets/<tweet_id>")
def _(tweet_id):
    # VALIDATE
    # Session
    if not g.IS_VALID_SESSION_API:
        response.status = 400
        return {"info": "No valid session"}
    session_user_id = g.GET_DECODED_JWT()["user_id"]

    try:
        db = mysql.connector.connect(**g.DB_CONFIG)
        cursor = db.cursor(dictionary = True)

        # Get tweet
        cursor.execute("""SELECT tweet_text, tweet_image FROM tweets
                        WHERE tweet_id = %s AND tweet_user_id = %s""", (tweet_id, session_user_id))
        tweet = cursor.fetchone()

        # No tweets with matchin id and user_id
        if not tweet:
            response.status = 200
            return {"info" : f"User doesn't own a tweet with id {tweet_id}"}

        # New tweet text
        if request.forms.get("tweet_text"):
            if (not len(request.forms.get("tweet_text").strip()) < 255
                or not len(request.forms.get("tweet_text").strip()) > 0):
                response.status = 400
                return {"info" : "tweet_text must contain min 1 and max 255 characters"}
            tweet["tweet_text"] = request.forms.get("tweet_text").strip()

        # New weet image
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

            # Delete old file if exist
            if tweet["tweet_image"]:
                os.remove(f"assets/images/{tweet['tweet_image']}")
            
            # Update tweet_image in tweet dict
            tweet["tweet_image"] = tweet_image
        
        # Remove image from tweet
        if tweet["tweet_image"] and not request.files.get("tweet_image"):
            os.remove(f"assets/images/{tweet['tweet_image']}")
            tweet["tweet_image"] = None

        # Set update time-stamp
        tweet["tweet_updated_at"] = int(time.time())
        
        tweet_tuple = (tweet["tweet_text"], tweet["tweet_image"], tweet["tweet_updated_at"], tweet_id, session_user_id)
        cursor.execute("""UPDATE tweets
                        SET tweet_text = %s, tweet_image = %s, tweet_updated_at = %s
                        WHERE tweet_id = %s AND tweet_user_id =%s""", tweet_tuple)
        db.commit()



        return json.dumps(tweet)

    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info" : "Server error"}

    finally:
        cursor.close()
        db.close()