from bottle import get, static_file

##############################

@get("/css/<file_name:re:.*\.css>")
def _(file_name):
    return static_file(file_name, root="./assets/css/")

##############################

@get("/js/<file_name:re:.*\.js>")
def _(file_name):
    return static_file(file_name, root="./assets/js/")    

##############################

@get("/images/<file_name:re:.*\.(jpg|jpeg|png)>")
def _(file_name):
    return static_file(file_name, root="./assets/images/")

##############################

@get("/icons/<file_name:re:.*\.(svg)>")
def _(file_name):
    return static_file(file_name, root="./assets/images/")