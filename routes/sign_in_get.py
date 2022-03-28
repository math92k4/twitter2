from bottle import get, view, redirect
import g

##############################

@get("/sign-in")
@view("sign_in")
def _():
    if g.IS_VALID_SESSION_ROUTES():
        return redirect("/")
    return

##############################