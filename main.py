import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type= "text/css">
        .error{
            color:red;
        }
    </style>
</head>
<body>
</html>
"""

signup_form = """
<form method="post">
    <h1>Signup</h1>
        <label>Username<input type="text" name= "username" value=""></label>
        <br>
        <label>Password<input type="text" name= "password" value=""></label>
        <br>
        <label>Verify Password<input type="text" name= "verify_password" value=""></label>
        <br>
        <label>Email (Optional)<input type="text" name= "email" value=""></label>
        <div style="color: red"></div>
        <br>
        <input type= "Submit">
    </form>
    """

class Index(webapp2.RequestHandler):
    #def write_form(error=""):
        #self.response.out.write(form % {"error": error})
    username = username(self.request.get('username'))
    password = password(self.request.get('password'))
    verify_password = valid_verify_password(self.request.get('verify_password'))
    email = email(self.request.get('email'))

    def get(self):
        self.response.write(page_header + signup_form)

    def post(self):
        have_error = False

        USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            return username and USER_RE.match(username)

        USER_RE=re.compile(r"^.{3,20}$")
        def valid_password(password):
            return password and USER_RE.match(password)

        def valid_verify_password(verify_password):
            return password == verify_password

        USER_RE=re.compile(r"^[\s]+[\s]+\.[\s]+$")
        def valid_email(email):
            return not email or USER_RE.match(email)

        params = dict (username = username, email = email)

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
            self.response.write(form, **params)
        else:
            self.redirect('/welcome?username=' + username)

        #if not (valid_username and valid_password and verify_password and valid_email):
            #self.response.out.write(form)
        #else: #needs to redirect to welcome, un! page
            #self.response.out.write("Thanks for signing up!")

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write('welcome.html', username = username)
        else:
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
