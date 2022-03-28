from bottle import get, view, redirect
import g

##############################

@get("/sign-up")
@view("sign_up")
def _():
    if g.IS_VALID_SESSION_ROUTES():
        return redirect("/")
    return