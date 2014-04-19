import twitter
import glob
import random

class Tweety( object ):
    def signIn(self):
        df = open('./twitter/login.dat', 'r')
        self.creds = {}
        for line in df:
            l = line.split()
            self.creds[l[0]] = l[1]
        self.tweeter = twitter.Api(consumer_key=self.creds["ckey"],
                consumer_secret=self.creds["csecret"],
                access_token_key=self.creds["atkey"],
                access_token_secret=self.creds["atsecret"])
        self.verification = self.tweeter.VerifyCredentials()
        self.name = self.verification.GetName()
        self.Id = self.verification.GetId()
        self.User = self.tweeter.GetUser(self.Id)
        self.status = self.User.GetStatus()
        self.timeHorizon = self.status.GetId()

    def loadStuff(self):
        self.TNTNum = "7871111"
        self.TNTtxt = "TNT"
        self.vocabdir = './twitter/'
        self.vocab = {}
        for name in ["startup", "snark", "broadcast", "shutdown"]:
            snippets = []
            for line in open(self.vocabdir+name+'.vocab', 'r'):
                snippets.append(line)
            self.vocab[name] = snippets


        self.graphdir = './graphs/'

    def __init__(self):
        self.signIn()
        self.loadStuff()
        print self.status.GetText()
        print self.timeHorizon
    
    def shutdown(self):
        self.tweeter.ClearCredentials()
    
    def reply(self, mention):
        status = "If I were working properly, a time and temperature status update would appear here"
        self.tweeter.PostUpdate(status, in_reply_to_status_id=mention.GetId())

    def checkFeed(self):
        newMentions = self.tweeter.GetMentions()#since_id=self.timeHorizon)
        for mention in newMentions:
            print mention.GetText()
            if (self.TNTtext in mention.GetText()) | (self.TNTNum in
                    mention.GetText()):
                print "User wants a query!"
                self.Reply(mention)


    def startGrilling(self):
        self.status = self.tweeter.PostUpdate(
            self.vocab["startup"][random.randint(0,len(self.vocab["startup"]))])
        self.timeHorizon = self.status.GetId()

    def stopGrilling(self):
        self.status = self.tweeter.PostUpdate(
            self.vocab["shutdown"][random.randint(
            0,len(self.vocab["shutdown"]))])
        self.timeHorizon = self.status.GetId()
        self.shutdown()
