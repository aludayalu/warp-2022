import flask,uuid,os,json
from flask import *

app=Flask(__name__)

@app.route("/signup")
def signup():
    args=dict(request.args)
    if "id" in args and "key" in args and not os.path.exists("users/"+args["id"]):
        id=str(uuid.uuid4()).replace(" ","").replace("-","")
        open("users/"+args["id"],"a").write(json.dumps({"uname":args["id"],"uid":id,"key":args["key"],"inventory":[]}))
        open("users/"+id,"a").write(json.dumps({"uname":args["id"],"uid":id,"key":args["key"],"inventory":[]}))
        return id
    else:
        return "404"

@app.route("/login")
def login():
    args=dict(request.args)
    if "id" in args and "key" in args and os.path.exists("users/"+args["id"]) and json.loads(open("users/"+args["id"]).read())["key"]==args["key"]:
        return json.loads(open("users/"+args["id"]).read())["uid"]
    else:
        return "404"

@app.route("/make_group")
def add_group():
    args=dict(request.args)
    if "token" in args and args["token"] in os.listdir("users") and "group" in args and not os.path.exists("groups/"+args["group"]):
        open("groups/"+args["group"],"a").write(json.dumps({"members":[args["token"],json.loads(open("users/"+args["token"]).read())["uname"]],"chat":[]}))
        return "Success"
    return "404"

@app.route("/send_group")
def post():
    args=dict(request.args)
    if "token" in args and args["token"] in os.listdir("users") and "group" in args and args["token"] in json.loads(open("groups/"+args["group"]).read())["members"] and "data" in args:
        group_data=json.loads(open("groups/"+args["group"]).read())
        group_data["chat"].append(args["data"])
        open("groups/"+args["group"],"r+").write(json.dumps(group_data))
        return "Success"
    else:
        return "404"

@app.route("/get_group")
def get_grp():
    args=dict(request.args)
    if "token" in args and args["token"] in os.listdir("users") and "group" in args and args["token"] in json.loads(open("groups/"+args["group"]).read())["members"]:
        return json.dumps(json.loads(open("groups/"+args["group"]).read())["chat"])
    else:
        return "404"

@app.route("/add_member")
def add_member_2_grp():
    args=dict(request.args)
    if "token" in args and args["token"] in os.listdir("users") and "group" in args and args["token"] in json.loads(open("groups/"+args["group"]).read())["members"] and "member" in args and args["member"] in os.listdir("users"):
        group_data=json.loads(open("groups/"+args["group"]).read())
        group_data["members"].append(args["member"])
        open("groups/"+args["group"],"r+").write(json.dumps(group_data))
        return "Success"
    else:
        return "404"

app.run(host="0.0.0.0")