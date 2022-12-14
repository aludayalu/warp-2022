import dbm,uuid,os,sys,json,base64,traceback
userdb=dbm.open("dbs/users","c")
groupsdb=dbm.open("dbs/groups","c")
reversedb=dbm.open("dbs/reverse","c")
from flask import *
app=Flask(__name__)

app.config['MANDRILL_API_KEY'] = '...'
app.config['MANDRILL_DEFAULT_FROM']= '...'
app.config['QOLD_SUPPORT_EMAIL']='...'
app.config['CORS_HEADERS'] = 'Content-Type'

def db_add(key,val,db):
    db[key]=str(val)+" "*1000

def db_get(key,db):
    return eval(db[key].decode())

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
        db_get(token,reversedb)
        return False
    except Exception as a:
        try:
            db_get(token,userdb)
            return False
        except Exception as b:
            traceback.print_exc()
            return True

def get_token(user):
    return db_get("users",userdb)[user]

def new_group(group_name):
    try:
        db_get(group_name,groupsdb)
        return False
    except:
        return True

@app.route("/signup")
def signup():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args) and new_user(make_uid(args["uname"],args["pwd"])):
        db_add(make_uid(args["uname"],args["pwd"]),json.dumps({"uname":args["uname"],"groups":[],"cart":[],"balance":1000}),userdb)
        db_add(args["uname"],"'"+f'{make_uid(args["uname"],args["pwd"])}'+"'",reversedb)
        return make_uid(args["uname"],args["pwd"])
    return "0"

@app.route("/name")
def getname():
    args=dict(request.args)
    if has_keys(["token"],args) and not new_user(args["token"]):
        return json.dumps(db_get(args["token"],userdb)["uname"])
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
        return json.dumps(db_get(args["token"],userdb)["groups"])
    return "0"

@app.route("/create_group")
def create_groups():
    args=dict(request.args)
    if has_keys(["token","name"],args) and not new_user(args["token"]) and new_group(args["name"]):
        db_add(args["name"],"[]",groupsdb)
        user_details=db_get(args["token"],userdb)
        user_details["groups"].append(args["name"])
        db_add(args["token"],json.dumps(user_details),userdb)
        return "Success"
    return "0"

@app.route("/add_member")
def add_member():
    args=dict(request.args)
    if has_keys(["token","group","user"],args) and not new_user(args["token"]) and not new_user(args["user"]) and not new_group(args["group"]) and args["group"] in db_get(args["token"],userdb)["groups"]:
        user_details=db_get(db_get(args["user"],reversedb),userdb)
        user_details["groups"].append(args["group"])
        db_add(db_get(args["user"],reversedb),json.dumps(user_details),userdb)
        return "1"
    return "0"

@app.route("/balance")
def bal():
    args=dict(request.args)
    if has_keys(["token"],args) and not new_user(args["token"]):
        return str(db_get(args["token"],userdb)["balance"])
    return "0"

@app.route("/products")
def products():
    return json.dumps({"compass":"https://media.gettyimages.com/id/172959404/photo/compass-isolated-on-a-white-background.jpg?s=612x612&w=gi&k=20&c=8QyNNdjq0u1TILMK9qP3bBcAhNm-qh9A_1ZDEwUVo-c=","torch":"https://www.collinsdictionary.com/images/full/torch_710716630_1000.jpg","boots":"https://images-eu.ssl-images-amazon.com/images/I/71SKJzaUoBL._AC._SR360,460.jpg","almond water":"https://3.bp.blogspot.com/-1jtbg2cj_zU/UjL0CZWgCAI/AAAAAAAA7hk/m6N4Y7Nsmiw/s1600/Victoria-kitchen-01.jpg"})

@app.route("/buy")
def buy():
    args=dict(request.args)
    if has_keys(["token","product"],args) and args["product"] in ["compass","boots","almond water","torch"] and not new_user(args["token"]):
        user_details=db_get(args["token"],userdb)
        user_details["cart"].append(args["product"])
        user_details["balance"]-=1
        db_add(args["token"],json.dumps(user_details),userdb)
        return '1'
    return "0"

@app.route("/inventory")
def cart():
    args=dict(request.args)
    if has_keys(["token"],args) and not new_user(args["token"]):
        return json.dumps(db_get(args["token"],userdb)["cart"])

@app.route("/send")
def send():
    args=dict(request.args)
    if has_keys(["token","group","data"],args):
        grp=db_get(args["group"],groupsdb)
        grp.append(f"{unpack_token(args['token'])[0]} - {args['data']}")
        db_add(args["group"],json.dumps(grp),groupsdb)
        resp=make_response("1")
        resp.headers['Access-Control-Allow-Origin']="*"
        return resp
    return "0"

@app.route("/pullchat")
def pullchat():
    args=dict(request.args)
    if has_keys(["token","group"],args) and not new_user(args["token"]) and args["group"] in db_get(args["token"],userdb)["groups"]:
        resp=make_response(json.dumps(db_get(args["group"],groupsdb)))
        resp.headers['Access-Control-Allow-Origin']="*"
        return resp
    return "0"

app.run(host="0.0.0.0",port=5001)