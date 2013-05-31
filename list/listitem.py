'''
Created on Apr 12, 2009

@author: par
'''

class PollResultListItem():
    answer = None
    answer_id = None
    votes = None
    votes_label = None
    
    def __init__(self, answer, answer_id, votes, total_votes, votes_label=None):
        self.answer = answer
        self.answer_id = answer_id
        self.votes = votes
        if votes_label == None:
            votes_label = votes
        self.votes_label = votes_label
        self.total_votes = total_votes
        if total_votes != 0:
            self.percent_votes = (1.0*votes/total_votes)*100
        

    
    def __str__(self):
        return "PollResultListItem (Answer:%s Answerid:%d Votes:%d Totalvotes:%d)" % (self.answer, self.answer_id, self.votes, self.total_votes)
    
    def __repr__(self):
        return "PollResultListItem (Answer:%s Answerid:%d Votes:%d Totalvotes:%d)" % (self.answer, self.answer_id, self.votes, self.total_votes)
    
    def __cmp__(x, y): #@NoSelf
        if x.votes < y.votes:
            return -1
        elif x.votes == y.votes:
            return 0
        else:
            return 1

class PollResultSpilloverListItem(PollResultListItem):
    spill_over_list = []
    
    def __init__(self, spill_over_list):
        # spillover item has to have atleast 1 vote, cuz we dont show zero votes on the charts!        
        PollResultListItem.__init__(self, answer="Spillover", answer_id=0, votes=1, total_votes=0)
        self.spill_over_list = spill_over_list
        self.spill_over_length = len(spill_over_list)
        spillans_count = 0
        for ans in spill_over_list:
            spillans_count += ans.votes
        self.percent_votes = (1.0 * spillans_count/spill_over_list[0].total_votes) * 100
        # we set the vote label appropriately here
        self.votes_label = spillans_count
        
        