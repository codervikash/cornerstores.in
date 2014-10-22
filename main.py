import os
import cgi
import urllib
import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import memcache


#for loding jinda enviornment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])


#database for people using less online shopping
class survey_less(ndb.Model):
    lname = ndb.StringProperty()
    lemail = ndb.StringProperty()
    #new entry
    lgender = ndb.StringProperty()
    lid = ndb.IntegerProperty()
    lage = ndb.IntegerProperty()

    lResidence = ndb.StringProperty()
    lsmart = ndb.StringProperty()
    lques_1 = ndb.TextProperty()
    lques_2 = ndb.TextProperty()
    lques_3 = ndb.TextProperty()
    lques_4 = ndb.TextProperty()
    lques_5 = ndb.TextProperty()
    lques_6 = ndb.TextProperty()
    lques_7 = ndb.TextProperty()
    lques_8 = ndb.TextProperty()
    lques_9 = ndb.TextProperty()


#database for people frequently using online shopping
class survey_more(ndb.Model):
    mname = ndb.StringProperty()
    memail = ndb.StringProperty()
    #new entry
    mgender = ndb.StringProperty()
    mid = ndb.IntegerProperty()
    mage = ndb.IntegerProperty()

    mResidence = ndb.StringProperty()
    msmart = ndb.StringProperty()
    mques_1 = ndb.TextProperty()
    mques_2 = ndb.TextProperty()
    mques_3 = ndb.TextProperty()
    mques_4 = ndb.TextProperty()
    mques_5 = ndb.TextProperty()
    mques_6 = ndb.TextProperty()
    mques_7 = ndb.TextProperty()
    mques_8 = ndb.TextProperty()
    mques_8 = ndb.TextProperty()
    mques_9 = ndb.TextProperty()


#main handler having welcome page with asking how frequent they use online shopping
class MainHandler(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class SurveyHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('survey.html')
        self.response.write(template.render())
    #post function after submission of their frequency of online shopping
    def post(self):
        #res is responce in scale of 0-100
        resp = self.request.get('res')
        if (resp <= 50):
            self.redirect('/offline')

        else:
            self.redirect('/smart')



#handler for people using less online shopping
class OfflineHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('offline.html')
        self.response.write(template.render(var))

    def post(self):
        #thankyou page for user without oauth
        mails = self.request.get('email')
        uname = self.request.get('name')
        auser = survey_less.query(survey_less.lemail == mails).get()
        #condition if user has already filled the form
        if auser is None:
            surveys_less = survey_less(lname=uname,
                                    llemail=mails,
                                    Residence=self.request.get('residence'),
                                    lsmart=self.request.get('smart'),
                                    lques_1=self.request.get('lques_1'),
                                    lques_2=self.request.get('lques_2'),
                                    lques_3=self.request.get('lques_3'),
                                    lques_4=self.request.get('lques_4'),
                                    lques_5=self.request.get('lques_5'),
                                    lques_6=self.request.get('lques_7'),
                                    lques_7=self.request.get('lques_7'),
                                    lques_8=self.request.get('lques_8'),
                                    lques_9=self.request.get('lques_9'))
            surveys_less.put()

            user_address = self.request.get('email')
            message = mail.EmailMessage()
            message.sender="Corner Stores Support <cornerstores.in@gmail.com>"

            message.subject="Thank You for your response!!"

            message.to = user_address
            message.body = """
                Dear %s:
                    Thank you for giving your time for us.
                    Hold back till we surprise you. :)

                Thank You.
                """ % uname

            message.send()

            template = JINJA_ENVIRONMENT.get_template('thankyou.html')
            self.response.write(template.render(var))

        else:
            self.redirect('/already')



#handler for people using online shopping frequently
class SmartHandler(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('smart.html')
        self.response.write(template.render())

    def post(self):
        #code to save date submitted from form
        mails = self.request.get('email')
        auser = survey_less.query(survey_less.lemail == mails).get()
        #condition if user has already filled the form
        if auser is None:
            surveys_more = survey_more(mname=self.request.get('name'),
                                    memail=mails,
                                    mResidence=self.request.get('residence'),
                                    msmart=self.request.get('smart'),
                                    mques_1=self.request.get('mques_1'),
                                    mques_2=self.request.get('mques_2'),
                                    mques_3=self.request.get('mques_3'),
                                    mques_4=self.request.get('mques_4'),
                                    mques_5=self.request.get('mques_5'),
                                    mques_6=self.request.get('mques_7'),
                                    mques_7=self.request.get('mques_7'),
                                    mques_8=self.request.get('mques_8'),
                                    mques_9=self.request.get('mques_9'))
            surveys_more.put()

            #for sending mail reply
            user_address = mails
            message = mail.EmailMessage()
            message.sender="Corner Stores Support <cornerstores.in@gmail.com>"

            message.subject="Thank You for your response!!"

            message.to = user_address
            message.body = """
                Dear %s:
                    Thank you for giving your time for us.
                    Hold back till we surprise you. :)

                Thank You.
                """ % uname

            message.send()

            template = JINJA_ENVIRONMENT.get_template('thankyou.html')
            self.response.write(template.render())

        else:
            self.redirect('/already')



class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(var))


class ContactHandler(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render(var))


class TeamHandler(webapp2.RequestHandler):
    def get(self):


        template = JINJA_ENVIRONMENT.get_template('team.html')
        self.response.write(template.render(var))


class BlogHandler(webapp2.RequestHandler):
    def get(self):


        template = JINJA_ENVIRONMENT.get_template('blog.html')
        self.response.write(template.render(var))





#routing handlers
app = webapp2.WSGIApplication(
    [
     ('/', MainHandler),
     ('/offline',OfflineHandler),
     ('/smart',SmartHandler),
     ('/about',AboutHandler),
     ('/contact',ContactHandler),
     ('/team',TeamHandler),
     ('/blog',BlogHandler),
     ('/survey',SurveyHandler),
     ],
    debug=True)

