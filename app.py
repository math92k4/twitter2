from bottle import default_app, run, get, view
import g

##############################

# Routes
import routes.static_routes
import routes.sign_up_get
import routes.sign_in_get
import routes.sign_out_get
import routes.main

# Api - endpoints
import api.users_post
import api.sessions_post
import api.tweets_post
import api.tweets_get_all
import api.tweets_get_by_user_id
import api.tweets_delete_by_id
import api.tweets_put_by_id


##############################

try:
    # Prod
    import production
    application = default_app()
except:
    # Dev
    run( host="127.0.0.1", port=5555, debug=True, reloader=True )