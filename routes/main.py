from bottle import get, view, request
import g
import jwt


##############################

@get("/")
@view("index")
def _():
    if not g.IS_VALID_SESSION_ROUTES():
        return dict(user_id = 0)

    decoded_jwt = g.GET_DECODED_JWT()
    user_id = decoded_jwt["user_id"]
    user_tag = decoded_jwt["user_tag"]
    user_char = user_tag[0]
    return dict(user_id = user_id, user_char = user_char)
