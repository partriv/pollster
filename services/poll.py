'''
Created on Mar 8, 2009

@author: par
'''
from pollster.models import Poll, PollFile, Tag, PollAnswer,\
    PollVote, UserProfile, PollsterMessage
from pollster.utils.string import StringUtils
from pollster.utils.file import FileUtils
from random import randint
from urlparse import urlparse
from threadedcomments.models import ThreadedComment
from pollster.list.listitem import PollResultListItem,\
    PollResultSpilloverListItem
from pollster.consts import consts
from django.core.paginator import Paginator
from pollster.utils import paging_utils
from pollster.conf import settings_local
from pollster.services.userservice import UserService
from django.db.models.query_utils import Q
from pollster.models_more import Poll_Tags
from pollster.list.feed_item import VoteItem, CommentItem, CreatedItem
from django.core.mail import EmailMultiAlternatives
from pollster.factory.chart_factory import GChartFactory
import random
import traceback
import datetime
import time
import logging

class PollService():
    
    log = logging.getLogger('PollService')
    
    def get_poll_file_w_icons(self, poll_files, thumb_style="view"):
        pollFiles = []
        for pf in poll_files:
            icon = ""            
            ext = pf.file[pf.file.rfind('.'):]
            if consts.IMAGES_WHITE_LIST.count(ext) > 0:
                icon = settings_local.POLL_FILES_URL + "%s_thumb/%s" % (thumb_style, pf.file) 
            elif consts.OTHER_FILES_WHITE_LIST.count(ext) > 0:
                if ext == ".doc":
                    icon = "/i/icons/DOC_icon.jpg"
                elif ext == ".xls":
                    icon = "/i/icons/excel_icon.png"
                elif ext == ".ppt":
                    icon = "/i/icons/ppt_icon.gif"
                elif ext == ".mp3":
                    icon = "/i/icons/audio-icon.png"
                elif ext == ".pdf":
                    icon = "/i/icons/pdf.jpg"
                elif ext == ".txt":
                    icon = "/i/icons/fileicon-text.png"
            else:
                self.log.warning("Trying to pull icon of blacklisted file.  pollfile id: %d" % pf.id)
            pollFiles.append((pf, icon))
        return pollFiles
    
    def get_next_url(self, question):
        url = StringUtils.cleanForUrl(question)
        return self.get_next_url_h(url)
    
    def get_next_url_h(self, url, count=None):
        if count:
            fullUrl = "%s-%d" % (url, count)
        else:
            fullUrl = url

        cnt = Poll.objects.filter(url=fullUrl).count()   #@UndefinedVariable
        if cnt == 0:
            return fullUrl
        
        if count == None:
            count = 0
        count+=1
        return self.get_next_url_h(url, count)
    
    def uploadPollFile(self, poll, file):
        thumbs = [(settings_local.POLL_FILES_THUMBS_HOME, consts.THUMB_WIDTH_MED, consts.THUMB_HEIGHT_MED),
                  (settings_local.POLL_FILES_THUMBS_VIEW, consts.THUMB_WIDTH_LG, consts.THUMB_HEIGHT_LG)]
        name = FileUtils.uploadFile(file, upload_path=settings_local.UPLOAD_POLL_FILES_PATH, thumbnails=thumbs)
        if name:
            pf = PollFile()
            pf.poll = poll
            pf.file = name
            pf.main_file = False
            pf.save()
            return pf
        else:
            return None
    
    def filter_on_demographic_info(self, answer, demographics):
        """ 
        Selects poll votes for an answer for the criteria in demographics
        Shitty algorithm makes lots of DB queries
        """
        count = 0
        poll_votes = PollVote.objects.filter(poll_answer=answer)   #@UndefinedVariable
        for poll_vote in poll_votes:
            try:
                profile = UserProfile.objects.get(user=poll_vote.user)   #@UndefinedVariable

                for demographic in demographics:
                    demo_value = getattr(profile, demographic[0])
                    if demo_value == demographic[1]:
                        count += 1
                    try: # for foriegn keys to tag table
                        if demo_value.name == demographic[1]:
                            count += 1
                    except AttributeError:
                        pass
                    try: # many to many
                        matches = [demo.name for demo in demo_value.all() if demo.name == demographic[1]]
                        if matches:
                            count += 1
                    except AttributeError:
                        pass

            except UserProfile.DoesNotExist:   #@UndefinedVariable
                pass
        return count

    def get_poll_chart_url(self, poll_id, demographic_url_string="", type="", do_spillover=""):
        gcf = GChartFactory()
        ps = PollService()
        p = Poll.objects.get(id=poll_id)
        results = ps.get_poll_results(poll=p, drop_zero_results=True)
        pchart = gcf.get_pie_chart(results)
        print pchart.get_url()
        return pchart.get_url()

    def get_poll_results(self, poll, drop_zero_results=True):
        """
        helper method to get a hash consisting of all results and vote count
        for polling results purposes
        keys:
            answer_id - the results id
            answer - the results
            votes - number of votes
        
        This method is sort of awesome.
        """
        
        votes = []
        pa = PollAnswer.objects.filter(poll=poll)   #@UndefinedVariable
        total_votes = 0
        for answer in pa:
            vote_count = PollVote.objects.filter(poll_answer=answer).count()   #@UndefinedVariable
            total_votes += vote_count
            votes.append(vote_count)
            
        results = []
        for (vote_count, poll_answer) in zip(votes, pa):            
            if vote_count > 0:                
                result = PollResultListItem(answer=poll_answer, answer_id=poll_answer.id, votes=vote_count, total_votes=total_votes)
                results.append(result)
            else:
                if not drop_zero_results:
                    result = PollResultListItem(answer=poll_answer, answer_id=poll_answer.id, votes=vote_count, total_votes=total_votes)
                    results.append(result)
                
        results.sort(reverse=True)
        
        return results
    
    def get_min_max_from_ans_and_votes(self, answers_and_votes):
        max = None
        min = None
        for av in answers_and_votes:
            if max == None and min == None:
                max = av.votes
                min = av.votes
            if av.votes > max:
                max = av.votes
            if av.votes < min:
                min = av.votes
        return (min, max)
            

    def get_random_polls(self, numToGet, user=None):
        # pick a random one
        allPolls = Poll.objects.filter(active=True)   #@UndefinedVariable
                
        if user.is_authenticated():     
            allPolls = self.get_polls_user_has_not_voted_on(user=user, return_all=True)
    
        # TODO: ayt tweak this thing
        ids = []
        if len(allPolls):
            for i in range(0, numToGet):
                ids.append(randint(0, len(allPolls)-1))
        polls = []
        for id in ids:
            polls.append(allPolls[id])
        return polls
    
    def get_polls_user_has_not_voted_on(self, user, return_all=True):
        allPolls = list(Poll.objects.filter(active=True))   #@UndefinedVariable
        # try to select something they have not voted on       
        votes = PollVote.objects.filter(user=user)   #@UndefinedVariable
        if len(votes) < len(allPolls):                
            pollsUserVotedOn = [vote.poll for vote in votes]
            for p in pollsUserVotedOn:
                try:
                    allPolls.remove(p)
                except ValueError:
                    pass
            return allPolls
        else:
            if return_all:
                return allPolls
            else:
                return None
            

    #############$
    # LISTER
    #############$
    def getPollsForLister(self, polls=None, user=None, page_num=1, page_link_prefix=""):
        """
        @param user: ALWAYS the request.user 
        given a list of poll objects, this will return a hash with a 
        list of tuples with the following order 
        {
            "paginator":paginator object,
            "polls":[(poll, file, tags), ...]
        }        
        
        This badboy also returns some major paging shit!!!!!
        
        """
        if polls == None:
            return None
        
        request_user = user
        
        pollListerHash = {}
        
        paged_polls = Paginator(polls, consts.POLL_LISTER_RPP)
        pollListerHash["paginator"] = paged_polls
        pollListerHash["total"] = len(polls)
        polls_page = paged_polls.page(page_num)
        
        page_hash = paging_utils.setup_page_hash(paginator=paged_polls, page_num=page_num, page_link_prefix=page_link_prefix)
        pollListerHash.update(page_hash)
        
        polls = polls_page.object_list
        aug_polls = []
        
        # go over db polls
        for p in polls:
            file = None
            poll_files = p.pollfile_set.all()
            len_pf = len(poll_files)
            more_pics = None
            
            # check the files first
            # do single or more picture logic
            if len_pf > 0:
                more_pics = 1
                if len_pf > 1:
                    more_pics = 2
                for pf in poll_files:
                    if pf.main_file == True:
                        # set main thumbnail if selected
                        file = pf.file
                if file == None:
                    file = poll_files[0].file

            # get the tags
            tags = p.tags.all()
            
            # store the link domain
            domain = urlparse(p.link)
            
            # check if the REQUEST user has voted
            voted=False
            watching = False
            if request_user and request_user.is_authenticated():
                count = p.pollvote_set.filter(user=request_user).count()
                if count > 0:
                    voted=True
                rqst_us = UserService(user=request_user).getUserData()
                if rqst_us.polls_watched.filter(poll=p).count() > 0:
                    watching = True
                

            # store it all on the super tuple
            # gets unpacked in the lister
            icons = False
            if p.link or more_pics or p.video_link:
                icons = True
            poll_user_data = UserService(p.user).getUserData()
            
            results = self.get_poll_results(p, drop_zero_results=True)
            gcf = GChartFactory()
            gchart = gcf.get_chart(results, 125, 125)
            
            pollhash = {}
            pollhash['poll'] = p
            pollhash['file'] = file
            pollhash['more_pics'] = more_pics
            pollhash['tags'] = tags
            pollhash['domain'] = domain
            pollhash['voted'] = voted
            pollhash['icons'] = icons
            pollhash['poll_user_data'] = poll_user_data
            pollhash['watching'] = watching
            if p.total_votes > 0:
                pollhash['chart_url'] = gchart.get_url()
            else:
                pollhash['chart_url'] = '/i/icons/chart_ph%d.png' % random.randint(1,3)
            aug_polls.append(pollhash)
            
            #aug_polls.append((p, file, more_pics, tags, domain[1], voted, icons, poll_user_data, watching))        
        
        pollListerHash["polls"] = aug_polls
        
        return pollListerHash

    ###################################
    #   PROFILE
    ###################################
    def getPollsCreatedByUsers(self, users):
        whereStr = "("
        params = []
        for u in users:
            whereStr += "user_id = %s or "
            params.append("%" + u.id + "%")   
        whereStr = whereStr.rstrip(" or ") + ")"
        where = [whereStr]
        where.append("active=%s")
        params.append(True)
        polls = Poll.objects.extra(where=where, params=params).order_by("-date_created")   #@UndefinedVariable
        return polls  
    
    def getUserFeed(self, user, owner=False, phase=0, request_user=None):
        """
        Gets the activity feed for a user
        This method is the hoss method of all methods in methodtown
        """
        
        us = UserService(user=user)
        userdata = us.getUserData()
        userdata_friends = userdata.friends.all()
        if not owner:
            request_user_friends = UserService(user=request_user).getFriends()
            friend_ids = [friend.id for friend in request_user_friends]
            userdata_friends = userdata_friends.filter(id__in=friend_ids) 
                        
        user_feed = []
        # create the motherfuckin window bitches!!!!!!
        start_index = phase * consts.POLL_ACTIVITY_WINDOW
        end_index = (phase+1) *  consts.POLL_ACTIVITY_WINDOW
        self.log.debug("start index: %d -- end index: %d" % (start_index, end_index))
        self.log.debug("Phase: %d" % phase)
        if owner:
            # only show friends stuff on owner feed
            for f in userdata_friends:
                # get polls friends created                
                friend_polls = Poll.objects.filter(user=f, active=True).order_by('-date_created')   #@UndefinedVariable
                for fp in friend_polls:
                    timestamp = time.mktime(fp.date_created.timetuple())
                    ci = CreatedItem(timestamp=timestamp, poll=fp, date=fp.date_created)
                    ci.friend_related = True
                    user_feed.append(ci)
                    
                # get friends votes
                friend_votes = PollVote.objects.filter(user=f).order_by('-date_created')   #@UndefinedVariable
                for fv in friend_votes:
                    timestamp = time.mktime(fv.date_created.timetuple())
                    vi = VoteItem(vote=fv, timestamp=timestamp, poll=fv.poll, date=fv.date_created)
                    vi.friend_related = True
                    vi.friend_voted = True
                    user_feed.append(vi)
                
                # get friends comments
                friend_comments = ThreadedComment.objects.filter(user=f).order_by('-date_modified')
                for fc in friend_comments:
                    timestamp = time.mktime(fc.date_modified.timetuple())
                    ci = CommentItem(comment=fc, timestamp=timestamp, poll=fc.content_object, date=fc.date_modified)
                    ci.friend_related = True
                    ci.friend_commented = True
                    user_feed.append(ci)

        # get polls created by user
        user_polls = Poll.objects.filter(user=user, active=True).order_by('-date_created')   #@UndefinedVariable
        for poll in user_polls:
            self.appendPollVotesAndComments(user_feed=user_feed, poll=poll, user_related=True, start_index=start_index, end_index=end_index)
            
            # add polls user created
            timestamp = time.mktime(poll.date_created.timetuple())
            ci = CreatedItem(timestamp=timestamp, poll=poll, date=poll.date_created)
            ci.user_related = True
            user_feed.append(ci)
        
        # get user's watched polls
        watched_polls = userdata.polls_watched.order_by('-poll__date_modified')                
        for wp in watched_polls:
            self.appendPollVotesAndComments(user_feed=user_feed, poll=wp.poll, watching=True, start_index=start_index, end_index=end_index)
        
        # get users votes
        user_votes = PollVote.objects.filter(user=user).order_by('-date_created')   #@UndefinedVariable
        for uv in user_votes:
            timestamp = time.mktime(uv.date_created.timetuple())
            vi = VoteItem(vote=uv, timestamp=timestamp, poll=uv.poll, date=uv.date_created)
            try:
                vi = user_feed[user_feed.index(vi)]                                        
            except ValueError:                                
                user_feed.append(vi)
            vi.user_voted = True
        
        # get user comments
        user_comments = ThreadedComment.objects.filter(user=user).order_by('-date_modified')
        for uc in user_comments:
            timestamp = time.mktime(uc.date_modified.timetuple())
            ci = CommentItem(comment=uc, timestamp=timestamp, poll=uc.content_object, date=uc.date_modified)
            try:
                ci = user_feed[user_feed.index(ci)]                                        
            except ValueError:                                
                user_feed.append(ci)
            ci.user_commented = True
        
        # sort that shit out
        remain = len(user_feed) > end_index
        user_feed.sort()
        user_feed.reverse()
        # TODO: FOR THE LOVE OF GOD CACHE THE FUCKING USER_FEED RIGHT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!
        user_feed = user_feed[start_index:end_index]
        return user_feed, remain
    
    
    def appendPollVotesAndComments(self, user_feed, poll, user_related=False, watching=False, start_index=None, end_index=None):
        """
        This method basically makes sure we dont add certain things to the feed more than once
        like a VoteItem or a CommentItem, so we test the feed to see if it already has that item, if it does not
        then we are free to add it.
        This method only acts on a set of polls
        """
        votes = PollVote.objects.filter(poll=poll).order_by('-date_created')   #@UndefinedVariable
        for v in votes:
            timestamp = time.mktime(v.date_created.timetuple())
            vi = VoteItem(vote=v, timestamp=timestamp, poll=v.poll, date=v.date_created)                       
            try:
                vi = user_feed[user_feed.index(vi)]                                        
            except ValueError:                                
                user_feed.append(vi)
            if watching:
                vi.watching_related = watching
            if user_related:                
                vi.user_related = user_related                
    
        # get all comments for your polls
        comments = ThreadedComment.objects.filter(object_id=poll.id).order_by('-date_modified')
        for c in comments:
            timestamp = time.mktime(c.date_modified.timetuple())
            ci = CommentItem(comment=c, timestamp=timestamp, poll=c.content_object, date=c.date_modified)                            
            try:
                ci = user_feed[user_feed.index(ci)]
            except ValueError:
                user_feed.append(ci)
            if watching:
                ci.watching_related = watching
            if user_related:
                ci.user_related = user_related            
                
        return user_feed
            
        
    
    ###################################
    #   SEARCH
    ###################################  
    def searchPolls(self, search_terms=None, user=None, sort=None):
        """
        poll search
        """
        
        if search_terms == None:
            return None
        search_terms = search_terms.split(", ")
        whereStr = "("
        params = []
        for s in search_terms:
            whereStr += "question like %s or description like %s or "
            params.append("%" + s + "%")
            params.append("%" + s + "%")   
        whereStr = whereStr.rstrip(" or ") + ")"
        where = [whereStr]
        where.append("active=%s")
        params.append(True)
        if sort:
            if sort == consts.SORT_TYPE_COMMENTS:
                polls = Poll.objects.extra(where=where, params=params).order_by("-total_comments")   #@UndefinedVariable
            elif sort == consts.SORT_TYPE_VOTES:
                polls = Poll.objects.extra(where=where, params=params).order_by("-total_votes")       #@UndefinedVariable    
            elif sort == consts.SORT_TYPE_DATE:
                polls = Poll.objects.extra(where=where, params=params).order_by("-date_created")   #@UndefinedVariable
        else:
            polls = Poll.objects.extra(where=where, params=params)   #@UndefinedVariable
        return polls

    def searchPollsByTag(self, tag, sort=None):
        q = None
        # build up tag's q
        for t in tag:
            if q == None:
                q = Q(tags=t)
            else:
                q = q | Q(tags=t)
           
        if sort:
            if sort == consts.SORT_TYPE_COMMENTS:                
                polls = Poll.objects.filter(active=True).filter(q).order_by("-total_comments")   #@UndefinedVariable
            elif sort == consts.SORT_TYPE_VOTES:
                polls = Poll.objects.filter(active=True).filter(q).order_by("-total_votes")   #@UndefinedVariable
            elif sort == consts.SORT_TYPE_DATE:
                polls = Poll.objects.filter(active=True).filter(q).order_by("-date_created")   #@UndefinedVariable
        else:
            polls = Poll.objects.filter(active=True).filter(q)   #@UndefinedVariable
        return polls

    def addSortSuffix(self, prefix, sort=None):
        if sort:
            if sort == consts.SORT_TYPE_COMMENTS:
                prefix += "/sort/%s" % consts.SORT_TYPE_COMMENTS
            if sort == consts.SORT_TYPE_VOTES:
                prefix += "/sort/%s" % consts.SORT_TYPE_VOTES
            if sort == consts.SORT_TYPE_DATE:
                prefix += "/sort/%s" % consts.SORT_TYPE_DATE
        return prefix

    def getSimilarPolls(self, poll):        
        whereStr = "("
        params = []
        for tag in poll.tags.all():
            whereStr += "tag_id = %s or "
            params.append("" + str(tag.id) + "")   
        whereStr = whereStr.rstrip(" or ") + ")"
        where = [whereStr]
        #where.append("active=%s")
        #params.append(True)
        if whereStr == "()":
            return None
        poll_tags = Poll_Tags.objects.extra(where=where, params=params)[0:10]   #@UndefinedVariable
        polls = []
        for p in poll_tags:
            if p.poll.active == True and p.poll != poll:
                polls.append(p.poll)
        return polls
    
    def sendPollsterMessage(self, to_user, from_user, subject, body):
        pm = PollsterMessage()
        pm.to_user = to_user
        pm.from_user = from_user
        pm.subject = subject
        pm.body = body
        pm.read = False
        pm.save()
        
        self.send_messaged_email(to_user, from_user, subject)
        

    def send_messaged_email(self, to_user, from_user, msg_subject):
        """
        send the 'someone messaged you email
        """
        
        self.log = logging.getLogger('PollService.send_messaged_email')
        #if the person voting is not the creator, email the creator
        subject = '%s has sent you a message' % from_user.username
        body = """Hello %s!
                <br/>It looks like %s has sent you a message: %s.  You can view it here: <a href="%sprofile/%s/mail/view/">Inbox</a>.  We just thought you'd like to know!
                <br/>                
                Thanks!
                <br/>
                -Pollstruck""" % (to_user.username, from_user.username, msg_subject, settings_local.HOST_NAME, to_user.username)
        
          
        from_email, to = 'Pollstruck@gmail.com', to_user.email
        text_content = 'Hello %s!\nIt looks like %s has sent you a message: %s.  You can view it here: <a href="%sprofile/%s/mail/view/">Inbox</a>.  We just thought you\'d like to know!\nThanks!\n-Pollstruck' % (to_user.username, from_user.username, msg_subject, settings_local.HOST_NAME, to_user.username)
        html_content = body
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except:
            # swallow ALL EXCEPTIONS ALWAYS ALLOW THE VOTE TO GO THROUGH
            # THIS IS THE EXCEPTION BLACKHOLE
            self.log.error('Could not send email to %s.' % to_user.email)
            self.log.error(traceback.format_exc())
        

    ##############################################
    # BACK END UTILITY METHODS
    ###############################################
    def reconcilePollVoteCounts(self):
        polls = Poll.objects.filter(active=True)   #@UndefinedVariable
        for p in polls:                        
            p.total_votes = PollVote.objects.filter(poll=p).count()   #@UndefinedVariable
            p.save()

    def reconcileTagCount(self):
        tags = Tag.objects.all()   #@UndefinedVariable
        for tag in tags:
            tag.poll_count = Poll_Tags.objects.filter(tag=tag, poll__active=True).count()   #@UndefinedVariable
            tag.save()
    
    def reconcileUntaggedPolls(self):
        polls = Poll.objects.filter(active=1)   #@UndefinedVariable
        for p in polls:
            if p.polltag_set.all().count() == 0:
                p.active=False
                p.save()
            
    def reconcilePollCommentsCount(self):
        polls = Poll.objects.filter(active=True)   #@UndefinedVariable
        for p in polls:
            p.total_comments = ThreadedComment.objects.filter(object_id=p.id).count()
            p.save();
    
    def resizeAnswerColumn(self):
        pollanswers = PollAnswer.objects.filter()   #@UndefinedVariable
        for pa in pollanswers:
            pa.answer = pa.answer[:70]
            pa.save()
