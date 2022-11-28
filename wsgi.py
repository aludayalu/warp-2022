from flask import *
app=Flask(__name__)
import requests,json
def get(endpoint,parse=True):
    if parse:
        return json.loads(requests.get("http://34.93.89.61/:5001/"+endpoint).text)
    else:
        return requests.get("http://34.93.89.61/:5001/"+endpoint).text

def has_keys(keys: list,args):
    for x in keys:
        if x not in args:
            return False
    return True

@app.route("/")
def home():
    if request.cookies.get("token")!=None and request.cookies.get("token")!="":
        token=request.cookies.get("token")
        return open("landing.html").read().replace("<!--insert-->","Hello "+eval(get("name?token="+token,parse=False)))
    else:
        return open("login.html").read()

@app.route("/login")
def login():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args):
        resp=make_response(redirect("/"))
        resp.set_cookie("token",get(f"login?uname={args['uname']}&pwd={args['pwd']}",parse=False))
        return resp
    return redirect("/")

@app.route("/signup")
def signup():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args):
        resp=make_response(redirect("/"))
        resp.set_cookie("token",get(f"signup?uname={args['uname']}&pwd={args['pwd']}",parse=False))
        return resp
    return redirect("/")

@app.route("/register")
def reg():
    return open("signup.html").read()

@app.route("/logout")
def logout():
    resp=make_response(redirect("/"))
    resp.set_cookie("token","")
    return resp

@app.route('/products')
def products():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
    body{
        background-repeat: no-repeat; 
        background-size: cover; 
        background-image: url("https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)");
        }
  </style>
  <div class="w3-bar" id="myNavbar">
    <a class="w3-bar-item w3-button w3-hover-black w3-hide-medium w3-hide-large w3-right" href="javascript:void(0);" onclick="toggleFunction()" title="Toggle Navigation Menu">
      <i class="fa fa-bars"></i>
    </a>
    <a href="/" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>HOME</p></a>
    <a href="/products" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>PRODUCTS</p></a>
    <a href="/inventory" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>INVENTORY</p></a>
    <a href="/groups" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>GROUPS</p></a>
    <a href="/logout" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>LOGOUT</p></a>
        <a href="#" class="w3-bar-item w3-button"><p>balance = #bal</p></a>
  </div>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <h2 class="posttitle">product</h2> <img src="img_url"> <div class="article"> Price: $1 </div><div class="readmore"> <a href="#" class="open" >Read More</a> </div></div> '
    products=get("products")
    for x in products:
        layout+=base.replace("product",x).replace("img_url",products[x]).replace("#",f"/product?id="+x)
    layout+="</div>"
    layout=layout.replace("#bal",str(get("balance?token="+request.cookies.get("token"))))
    return make_response(layout)

@app.route("/blog.css")
def css():
    return open("blog.css").read()

@app.route("/product")
def product():
    id=dict(request.args)["id"]
    return open("product.html").read().replace("product",id).replace("img_url",get("products")[id]).replace("uwu","/buy?product="+id+"&token="+request.cookies.get("token"))

@app.route("/buy")
def buy():
    args=dict(request.args)
    if has_keys(["token","product"],args):
        get(request.full_path,parse=0)
        return redirect("/inventory")
    else:
        return open("login.html").read()


@app.route('/inventory')
def inventory():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
    body{
        background-repeat: no-repeat; 
        background-size: cover; 
        background-image: url("https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)");
        }
  </style>
  <div class="w3-bar" id="myNavbar">
    <a class="w3-bar-item w3-button w3-hover-black w3-hide-medium w3-hide-large w3-right" href="javascript:void(0);" onclick="toggleFunction()" title="Toggle Navigation Menu">
      <i class="fa fa-bars"></i>
    </a>
    <a href="/" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>HOME</p></a>
    <a href="/products" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>PRODUCTS</p></a>
    <a href="/inventory" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>INVENTORY</p></a>
    <a href="/groups" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>GROUPS</p></a>
    <a href="/logout" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>LOGOUT</p></a>
    <a href="#" class="w3-bar-item w3-button"><p>balance = #bal</p></a>
  </div>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <h2 class="posttitle">product</h2> <img src="img_url"> <div class="article"> Price: $1 </div><div class="readmore"> <a href="#id" class="open" >Read More</a> </div></div> '
    products=get("inventory?token="+request.cookies.get("token"))
    images=get("products")
    for x in products:
        layout+=base.replace("product",x).replace("img_url",images[x]).replace("#id",f"/product?id="+x)
    layout+="</div>"
    layout=layout.replace("#bal",str(get("balance?token="+request.cookies.get("token"))))
    return make_response(layout)

@app.route('/groups')
def groups():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
    body{
        background-repeat: no-repeat; 
        background-size: cover; 
        background-image: url("https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)");
        }
    img {
    height: 200px;
    }
  </style>
  <div class="w3-bar" id="myNavbar">
    <a class="w3-bar-item w3-button w3-hover-black w3-hide-medium w3-hide-large w3-right" href="javascript:void(0);" onclick="toggleFunction()" title="Toggle Navigation Menu">
      <i class="fa fa-bars"></i>
    </a>
    <a href="/" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>HOME</p></a>
    <a href="/products" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>PRODUCTS</p></a>
    <a href="/inventory" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>INVENTORY</p></a>
    <a href="/groups" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>GROUPS</p></a>
    <a href="/logout" class="w3-bar-item w3-button" onclick="toggleFunction()"><p>LOGOUT</p></a>
    <a href="#" class="w3-bar-item w3-button"><p>balance = #bal</p></a>
    <a href="/create_group" class="w3-bar-item w3-button"><p>Create Group</p></a>
  </div>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <h2 class="posttitle">product</h2> <img src="img_url"><div class="readmore"> <a href="#chat" class="open" >Open Chat</a> </div></div> '
    groups=get("groups?token="+request.cookies.get("token"))
    for x in groups:
        layout+=base.replace("product",x).replace("#chat","/chat?token="+request.cookies.get("token")+"&group="+x).replace("img_url","https://img.freepik.com/free-vector/group-therapy-illustration-concept_52683-45727.jpg?w=1380&t=st=1669613150~exp=1669613750~hmac=2b64377ce8d0d96aceb6fc7257ad662e8ba5090416a40cc93bea7036e3322f34")
    layout+="</div>"
    layout=layout.replace("#bal",str(get("balance?token="+request.cookies.get("token"))))
    return make_response(layout)

@app.route("/create_group")
def grp_add():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/")
    return open("creategroup.html").read()

@app.route("/create_group_api")
def grp_add_api():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["name"],args):
        return redirect("/")
    get("create_group?token="+request.cookies.get("token")+"&name="+args["name"],parse=0)
    return redirect("/groups")

@app.route("/chat")
def test():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group"],args):
        return redirect("/")
    resp=make_response(open("chat.html").read().replace("tkn",args['token']).replace("grp",args["group"]))
    resp.headers['Access-Control-Allow-Origin']="*"
    return resp

@app.route("/addmember")
def addmember():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group"],args):
        return redirect("/")
    return open("addmember.html").read().replace("grp",args["group"]).replace("tkn",args["token"])

@app.route("/add_member_api")
def memberaddapi():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group","name"],args):
        return redirect("/")
    get(f"add_member?token={args['token']}&group={args['group']}&user={args['name']}",parse=0)
    return redirect("/chat?token="+args["token"]+"&group="+args["group"])
app.run(host="0.0.0.0",port=1234)