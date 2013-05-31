'''
Created on May 16, 2009

@author: par
'''

class FeedItem():
        
    def __init__(self, timestamp, poll, date):
        self.timestamp = timestamp
        self.poll = poll
        self.type = 'feed'
        self.date = date
        
    def __str__(self):
        return "(%s, %s, %d)" % (self.poll.question, self.type, self.timestamp)
    
    def __repr__(self):
        return "(%s, %s, %d)" % (self.poll.question, self.type, self.timestamp)
    
    def __cmp__(x, y): #@NoSelf
        if x.timestamp < y.timestamp:
            return -1
        elif x.timestamp == y.timestamp:
            return 0
        else:
            return 1
    
    def __eq__(x, y): #@NoSelf
        return x.timestamp == y.timestamp and x.poll == y.poll and x.type == y.type and x.date == y.date
                

class VoteItem(FeedItem):
    vote = None    
    def __init__(self, vote, timestamp, poll, date):
        FeedItem.__init__(self, timestamp, poll, date)
        self.vote = vote
        self.type = 'vote'
        self.related_user = vote.user
    
    #def __eq__(x, y):
        #return x.vote == y.vote

        
class CommentItem(FeedItem):
    def __init__(self, comment, timestamp, poll, date):
        FeedItem.__init__(self, timestamp, poll, date)
        self.comment = comment
        self.type = 'comment'
        self.related_user = comment.user
    
    #def __eq__(x, y):
        #return x.comment == y.comment
        
class CreatedItem(FeedItem):
    def __init__(self, timestamp, poll, date):
        FeedItem.__init__(self, timestamp, poll, date)
        self.type = 'created'
        self.related_user = poll.user