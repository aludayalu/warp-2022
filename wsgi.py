from flask import *
app=Flask(__name__)
import requests,json,stripe
stripe.api_key = "sk_test_51Lw6HISCYPNTiYy3KS6yyhaHn0LrQrdWjLZjUOgvU1fl3chReC3kmdjkuRJwSQb3OENz7yrIqkZwGGsNkMBTVyCw00iL71l0WM"
price_10="price_1M8FpbSCYPNTiYy3l5qPsc20"

def make_link(price,cookie):
    return dict(stripe.checkout.Session.create(
        success_url="http://34.93.89.61:5000/success"+cookie,
        cancel_url="http://34.93.89.61:5000/cancel",
        line_items=[
            {
            "price": price,
            "quantity": 1,
            },
        ],
        mode="payment",
    ))["url"]

def get(endpoint,parse=True):
    if parse:
        return json.loads(requests.get("http://127.0.0.1:5001/"+endpoint).text)
    else:
        return requests.get("http://127.0.0.1:5001/"+endpoint).text

def has_keys(keys: list,args):
    for x in keys:
        if x not in args:
            return False
    return True

@app.route("/")
def home():
    return open("landing.html").read()

@app.route("/login")
def login():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args):
        resp=make_response(redirect("/"))
        ans=get(f"login?uname={args['uname']}&pwd={args['pwd']}",parse=False)
        if ans=="0":
            return redirect("/signin")
        resp.set_cookie("token",ans)
        return resp
    return redirect("/signin")

@app.route("/signup")
def signup():
    args=dict(request.args)
    if has_keys(["uname","pwd"],args):
        resp=make_response(redirect("/"))
        resp.set_cookie("token",get(f"signup?uname={args['uname']}&pwd={args['pwd']}",parse=False))
        return resp
    return redirect("/signin")

@app.route("/register")
def reg():
    return open("signup.html").read()

@app.route("/logout")
def logout():
    resp=make_response(redirect("/signin"))
    resp.set_cookie("token","")
    return resp

@app.route('/products')
def products():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/signin")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
    body{
        background-repeat: no-repeat; 
        background-size: cover; 
        }
  </style>
  <div class="topnav" id="myTopnav">
  <a href="/logout" class="active">Sign Out</a>
  <a href="/products">Products</a>
  <a href="/inventory">Inventory</a>
  <a href="/groups">Groups</a>
  <a href="/" class="active">Home</a> 
  <a class="logo" style="float: left;margin-left: 10px;font-size:xx-large;font-family: 'Lato', sans-serif;">Rimor</a>
</div>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <img src="img_url"><h2 class="posttitle">product</h2>  <div class="article" style="text-align: right; font-weight:900; color: grey;margin-right:20px;"> ₹1000 </div><div class="readmore"> <div class="hreftag" style="border-radius: 4px;"><a href="#" class="open"style="border-radius:4px;margin:20px;" >Read More</a></div> </div></div> '
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
        return redirect(make_link(price_10,"x"))
        get(request.full_path,parse=0)
        return redirect("/inventory")
    else:
        return open("login.html").read()


@app.route('/inventory')
def inventory():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/signin")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <div class="w3-top">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>
    .w3-wide {letter-spacing: 10px;}
    .w3-hover-opacity {cursor: pointer;}
  </style>
  <div class="topnav" id="myTopnav">
  <a href="/logout" class="active">Sign Out</a>
  <a href="/products">Products</a>
  <a href="/inventory">Inventory</a>
  <a href="/groups">Groups</a>
  <a href="/" class="active">Home</a> 
  <a class="logo" style="float: left;margin-left: 10px;font-size:xx-large;font-family: 'Lato', sans-serif;">Rimor</a>
</div>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <img src="img_url"><h2 class="posttitle">product</h2>  <div class="article" style="text-align: right; font-weight:900; color: grey;margin-right:20px;"> ₹1000 </div><div class="readmore"> <div class="hreftag" style="border-radius: 4px;"><a href="#id" class="open"style="border-radius:4px;margin:20px;" >Read More</a></div> </div></div> '
    products=get("inventory?token="+request.cookies.get("token"))
    images=get("products")
    for x in products:
        layout+=base.replace("product",x).replace("img_url",images[x]).replace("#id",f"/product?id="+x)
    if products==[]:
        layout+="""
<h1>You don't own any item right now.</h1>
"""
    layout+="</div>"
    layout=layout.replace("#bal",str(get("balance?token="+request.cookies.get("token"))))
    return make_response(layout)

@app.route('/groups')
def groups():
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/signin")
    layout='<link rel="stylesheet" href="blog.css">'
    layout+="""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <style>body {
  background-image: url("https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
  }</style>
  <div class="topnav" id="myTopnav">
  <a href="/logout" class="active">Sign Out</a>
  <a href="/products">Products</a>
  <a href="/inventory">Inventory</a>
  <a href="/groups">Groups</a>
  <a href="/" class="active">Home</a> 
  <a class="logo" style="float: left;margin-left: 10px;font-size:xx-large;font-family: 'Lato', sans-serif;">Rimor</a>
  <a style="float: left;margin-left: 10px;margin-top:15px;" href="/create_group">Create Group</a>
</div>
<p style="height:80px;"></p>
    """
    layout+='<div class"allposts" style="display:flex;justify-content:space-evenly;align-items:center;flex-wrap:wrap;">'
    base='<div class="card"> <img src="img_url"><h2 class="posttitle">product</h2> <div class="readmore"> <div class="hreftag" style="border-radius: 4px;"><a href="#chat" class="open"style="border-radius:4px;margin:20px;" >Open Chat</a></div> </div></div> '
    groups=get("groups?token="+request.cookies.get("token"))
    for x in groups:
        layout+=base.replace("product",x).replace("#chat","/chat?token="+request.cookies.get("token")+"&group="+x).replace("img_url","/imgs/group.png")
    layout+="</div>"
    if groups==[]:
        layout+="""
<h1>You are not in any groups as of now.</h1>
"""
    layout=layout.replace("#bal",str(get("balance?token="+request.cookies.get("token"))))
    return make_response(layout)

@app.route("/create_group")
def grp_add():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!=""):
        return redirect("/signin")
    return open("creategroup.html").read()

@app.route("/create_group_api")
def grp_add_api():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["name"],args):
        return redirect("/signin")
    get("create_group?token="+request.cookies.get("token")+"&name="+args["name"],parse=0)
    return redirect("/groups")

@app.route("/chat")
def test():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group"],args):
        return redirect("/signin")
    resp=make_response(open("chat.html").read().replace("tkn",args['token']).replace("grp",args["group"]))
    resp.headers['Access-Control-Allow-Origin']="*"
    return resp

@app.route("/addmember")
def addmember():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group"],args):
        return redirect("/signin")
    return open("addmember.html").read().replace("grp",args["group"]).replace("tkn",args["token"])

@app.route("/add_member_api")
def memberaddapi():
    args=dict(request.args)
    if not (request.cookies.get("token")!=None and request.cookies.get("token")!="") or not has_keys(["token","group","name"],args):
        return redirect("/signin")
    get(f"add_member?token={args['token']}&group={args['group']}&user={args['name']}",parse=0)
    return redirect("/chat?token="+args["token"]+"&group="+args["group"])

@app.route("/astro.gif")
def astro_svg():
    return send_file("svgs/astronaut.gif")

@app.route("/imgs/group.png")
def grppng():
    return send_file("imgs/group.png")

@app.route("/login.css")
def logincss():
    return send_file("login.css")

@app.route("/signin")
def signin():
    return open("login.html").read()

app.run(host="0.0.0.0",port=1234,debug=1)