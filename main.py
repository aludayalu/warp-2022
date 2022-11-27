import shelve,uuid,os,sys,json,base64
userdb=shelve.open("dbs/users")
groupsdb=shelve.open("dbs/groups")
from flask import *
app=Flask(__name__)

def has_keys(keys: list,args):
    for x in keys:
        if x not in args:
            return False
    return True

def make_uid(id,pwd):
    return base64.b64encode(str((id,pwd)).replace("'","").encode()).decode()

def unpack_token(token):
    new_tuple=[]
    for x in base64.b64decode(token.encode()).decode().replace("(","").replace(")","").split(","):
        new_tuple.append(x)
    return new_tuple

def new_user(token):
    try:
        userdb[token]
        return False
    except Exception as e:
        print(e)
        return True

def new_group(group_name):
    try:
        group_name[group_name]
        return False
    except:
        return True

@app.route("/signup")
def signup():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args) and new_user(make_uid(args["uname"],args["pwd"])):
        userdb[make_uid(args["uname"],args["pwd"])]={"uname":args["uname"],"pwd":args["pwd"],"groups":[],"cart":[],"balance":1000}
        try:
            userdb["users"]
        except:
            userdb["users"]={}
        users=userdb["users"]
        users[args["uname"]]=make_uid(args["uname"],args["pwd"])
        userdb["users"]=users
        return make_uid(args["uname"],args["pwd"])
    return "0"

@app.route("/login")
def login():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args) and not new_user(make_uid(args["uname"],args["pwd"])):
        return make_uid(args["uname"],args["pwd"])
    return "0"

@app.route("/groups")
def get_groups():
    args=dict(request.args)
    if has_keys(["token"],args) and not new_user(args["token"]):
        return json.dumps(userdb[args["token"]]["groups"])
    return "0"

@app.route("/create_group")
def create_groups():
    args=dict(request.args)
    if has_keys(["token","name"],args) and not new_user(args["token"]) and new_group(args["name"]):
        groupsdb[args["name"]]=[]
        user_details=userdb[args["token"]]
        user_details["groups"].append(args["name"])
        userdb[args["token"]]=user_details
        return "Success"
    return "0"

@app.route("/add_member")
def add_member():
    args=dict(request.args)
    if has_keys(["token","group","user"],args) and not new_user(args["token"]) and not new_user(args["user"]) and new_group(args["group"]) and args["group"] in userdb[args["token"]]["groups"]:
        pass
app.run(host="0.0.0.0",port=5001)