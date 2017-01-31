import webapp2
import cgi
import re

# page_header = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Signup</title>
#     <style type= "text/css">
#         .error{
#             color:red;
#         }
#     </style>
# </head>
# <body>
# signup-form
# </body>
# </html>
# """

USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE=re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE=re.compile(r"^[\S]+[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

signup_form = """
<form method="post">
    <h1>Signup</h1>
    <label>Username
    <input type="text" name= "username" value={username}></label>
    <div style="color:red">{userNameError}</div>
    <br>
    <label>Password
    <input type="password" name= "password" value=""></label>
    <div style="color:red">{passwordError}</div>
    <br>
    <label>Verify Password
    <input type="password" name= "verify" value=""></label>
    <div style="color:red">{verifyError}</div>
    <br>
    <label>Email (Optional)
    <input type="text" name= "email" value={email}></label>
    <div style="color:red">{emailError}</div>
    <br>
    <input type= "Submit">
</form>
"""

class Index(webapp2.RequestHandler):
        #def write_form(error=""):
            #self.response.out.write(form % {"error": error})

    def get(self):
        #self.response.write('page_header' + 'signup-form')
        self.response.out.write(signup_form.format(username='',email='',userNameError='',passwordError='',verifyError='',emailError=''))

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict (username=username,email=email,error_username='',error_password='',error_verify='',error_email='')

        if not valid_username(username):
            params ['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params ['error_password'] = "That was not a valid password."
            have_error = True
        elif password != verify:
            params ['error_verify'] = "Your passwords did not match."
            have_error = True

        if not valid_email(email):
            params ['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.response.out.write(signup_form.format(username=params["username"],email=params["email"],userNameError=params['error_username'],passwordError=params["error_password"],verifyError=params["error_verify"],emailError=params["error_email"]))
        else:
            self.redirect("/welcome?username=" + username)

        #if not (valid_username and valid_password and verify_password and valid_email):
            #self.response.out.write(form)
        #else: #needs to redirect to welcome, un! page
            #self.response.out.write("Thanks for signing up!")

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        welcome_message = "Welcome, " + username + "!"
        self.response.write(welcome_message)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
