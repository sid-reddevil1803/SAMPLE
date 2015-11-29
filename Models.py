# Sample comment
import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb

class Notifications(ndb.Model):
    groupName = ndb.StringProperty(required=True)
    groupId = ndb.KeyProperty(kind='Club', required=True)
    groupImage = ndb.BlobProperty()
    eventName = ndb.StringProperty()
    eventId = ndb.KeyProperty(kind ='Event')
    postName = ndb.StringProperty()
    postId = ndb.KeyProperty(kind ='Post')
    timestamp = ndb.DateTimeProperty()
    type = ndb.StringProperty(required='True')

class NotificationResponseForm(messages.Message):
    groupName = messages.StringField(1)
    groupId = messages.StringField(2)
    groupImage = messages.StringField(3)
    eventName = messages.StringField(4)
    eventId = messages.StringField(5)
    postName = messages.StringField(6)
    postId = messages.StringField(7)
    timestamp = messages.StringField(8)
    type = messages.StringField(9)




class Profile(ndb.Model):
    """Profile -- User profile object"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    photo = ndb.BlobProperty()
    batch = ndb.StringProperty()
    branch = ndb.StringProperty()
    follows = ndb.KeyProperty(kind='Club', repeated=True)  # ndb.StringProperty(repeated=True)
    tags = ndb.StringProperty(repeated=True)
    clubsJoined = ndb.KeyProperty(kind='Club',
                                  repeated=True)  # One club, many students ndb.StringProperty(repeated=True)
    #pid = ndb.StringProperty(required=True)
    gcmId = ndb.StringProperty()  # make gcmid compulsory
    isAlumni = ndb.StringProperty(required=True)
    company = ndb.StringProperty()
    location = ndb.StringProperty()
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many people
    eventsAttending = ndb.KeyProperty(kind='Event')
    #id = pid

class Club(ndb.Model):
    name = ndb.StringProperty(required=True)
    picture = ndb.BlobProperty()
    #clubId = ndb.StringProperty(required=True)
    admin = ndb.KeyProperty(kind='Profile', required=True)
    description = ndb.StringProperty()
    members = ndb.KeyProperty(kind='Profile', repeated=True)
    follows = ndb.KeyProperty(kind='Profile',
                              repeated=True)  # Only includes the set of people apart from members. By default a member of a club follows it.
    abbreviation = ndb.StringProperty()
    photo = ndb.BlobProperty()
    isAlumni = ndb.StringProperty(required=True)
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)


class ClubMiniForm(messages.Message):
    name = messages.StringField(1, required=True)
    admin = messages.StringField(2)
    description = messages.StringField(3)
    members = messages.StringField(4)
    followers = messages.StringField(
        5)  # Only includes the set of people apart from members. By default a member of a club follows it.
    abbreviation = messages.StringField(6, required=True)
    # photo = ndb.BlobProperty()
    collegeName = messages.StringField(7, required=True)
    club_id = messages.StringField(8,required=True)
    picture = messages.StringField(9)

class GetClubMiniForm(messages.Message):
    club_id = messages.StringField(1, required="True")


class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    from_pid = ndb.KeyProperty(kind="Profile",required=True)  # ancestor relationship here?
    photo = ndb.BlobProperty()
    club_id = ndb.KeyProperty(kind='Club', required=True)  # Many posts belong to one club
    likes = ndb.IntegerProperty()
    views = ndb.IntegerProperty()
    # id = postId
    likers = ndb.KeyProperty(kind='Profile', repeated=True)
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many posts
    timestamp = ndb.DateTimeProperty()

class PostForm(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    from_pid = messages.StringField(3)  # ancestor relationship here?
    photo = messages.StringField(4)
    # club_id = ndb.KeyProperty(kind='Club',required=True)#Many posts belong to one club
    likes = messages.StringField(5)
    views = messages.StringField(6)
    likers = messages.StringField(7)
    date = messages.StringField(8)
    time = messages.StringField(9)
    clubphoto = messages.StringField(10)

class EditPostForm(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    photo = messages.StringField(3)
    postId = messages.StringField(4,required=True)

class Posts(messages.Message):
    items = messages.MessageField(PostForm, 1, repeated=True)


class GetAllPosts(messages.Message):
    collegeId = messages.StringField(1)
    clubId = messages.StringField(2)


class Post_Request(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    from_pid = ndb.KeyProperty(kind='Profile', required=True)  # This is the post creator
    to_pid = ndb.KeyProperty(kind='Profile', required=True)  # many requests to one profile
    club_id = ndb.KeyProperty(kind='Club', required=True)
    status = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty()
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many post requests

class GetInformation(messages.Message):
    pid = messages.StringField(1)
    collegeId = messages.StringField(2)
    clubId = messages.StringField(3)
    date = messages.StringField(4)

class GetPostRequestsForm(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    person_from = messages.StringField(3)
    club_name = messages.StringField(4)
    postRequestId = messages.StringField(5)
    date = messages.StringField(6)
    time = messages.StringField(7)

class GetAllPostRequests(messages.Message):
    items = messages.MessageField(GetPostRequestsForm,1,repeated=True)

class UpdatePostRequests(messages.Message):
    postRequestId = messages.StringField(1,required=True)
    action = messages.StringField(2,required=True)


class PostMiniForm(messages.Message):
    """PostMiniForm -- What's shown on the UI for a post"""
    from_pid = messages.StringField(1, required=True)
    club_id = messages.StringField(2, required=True)
    title = messages.StringField(3, required=True)
    description = messages.StringField(4, required=True)
    likers = messages.StringField(5)
    date = messages.StringField(6)
    time = messages.StringField(7)
    photo = messages.StringField(8)
    # '''photo ='''


class LikePost(messages.Message):
    from_pid = messages.StringField(1, required=True)
    postId = messages.StringField(2, required=True)


class Event(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    photo = ndb.BlobProperty()
    club_id = ndb.KeyProperty(kind='Club', required=True)  # Many events belong to one club
    venue = ndb.StringProperty(required=True)
    start_time = ndb.DateTimeProperty(required=True)#make this required
    end_time = ndb.DateTimeProperty(required=True)
    attendees = ndb.KeyProperty(kind='Profile',repeated=True)
    completed = ndb.StringProperty(required=True)
    views = ndb.IntegerProperty()
    isAlumni = ndb.StringProperty(required=True)
    event_creator = ndb.KeyProperty(kind='Profile',required=True)  # ancestor relationship?
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many events
    tags = ndb.StringProperty(repeated=True)
    likers = ndb.KeyProperty(kind='Profile', repeated=True)
    timestamp = ndb.DateTimeProperty()

class EventMiniForm(messages.Message):
    title = messages.StringField(1, required=True)
    description = messages.StringField(2)
    # photo = ndb.BlobProperty()
    club_id = messages.StringField(3, required=True)  # Many events belong to one club
    # eventId = messages.StringField(4,required=True)
    venue = messages.StringField(4, required=True)
    start_date = messages.StringField(5, required=True)
    start_time = messages.StringField(6, required=True)
    end_time = messages.StringField(7, required=True)
    end_date = messages.StringField(8,required=True)
    attendees = messages.StringField(9)
    completed = messages.StringField(10, required=True)
    views = messages.StringField(11)
    isAlumni = messages.StringField(12, required=True)
    event_creator = messages.StringField(13, required=True)
    tags = messages.StringField(14)
    date = messages.StringField(15)
    time = messages.StringField(16)

class EventForm(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    # photo = ndb.BlobProperty()
    club_id = messages.StringField(3)  # Many events belong to one club
    # eventId = messages.StringField(4,required=True)
    venue = messages.StringField(4)
    start_date = messages.StringField(5)
    start_time = messages.StringField(6)
    end_time = messages.StringField(7)
    end_date = messages.StringField(8)
    attendees = messages.StringField(9)
    completed = messages.StringField(10)
    views = messages.StringField(11)
    isAlumni = messages.StringField(12)
    event_creator = messages.StringField(13)
    collegeId = messages.StringField(14)
    eventId = messages.StringField(15)
    tags = messages.StringField(16)
    date = messages.StringField(17)
    time = messages.StringField(18)
    clubphoto = messages.StringField(19)
# id=eventId

class ModifyEvent(messages.Message):
    from_pid = messages.StringField(1, required=True)
    eventId = messages.StringField(2, required=True)


class Events(messages.Message):
    items = messages.MessageField(EventForm,1,repeated=True)


"""
class PostRequestMiniForm(messages.Message):
    from_pid = messages.StringField(1,required=True)
    club_id = messages.StringField(2,required=True)
    description = messages.StringField(3,required=True)
"""


class Club_Creation(ndb.Model):
    from_pid = ndb.KeyProperty(kind='Profile', required=True)  # One profile can have many club creation requests
    to_pid = ndb.KeyProperty(kind='Profile', required=True)  # many requests to student council admin
   # club_id = ndb.StringProperty(required=True)
    picture = ndb.BlobProperty()
    description = ndb.StringProperty(required=True)
    club_name = ndb.StringProperty(required=True)
    abbreviation = ndb.StringProperty(required=True)
    isAlumni = ndb.StringProperty(required=True)
    #club_creation_id = ndb.StringProperty(required=True)
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many club creation requests
    approval_status = ndb.StringProperty()
    #id = club_creation_id


class ClubRequestMiniForm(messages.Message):
    """ClubRequestMiniForm -- What's shown on the UI for an club request"""
    # from_pid = messages.StringField(1,required=True)
    club_name = messages.StringField(1, required=True)
    abbreviation = messages.StringField(2, required=True)
    description = messages.StringField(3, required=True)
    from_pid = messages.StringField(4, required=True)
    college_id = messages.StringField(5, required=True)
    picture = messages.StringField(6)


class Join_Request(ndb.Model):
    from_pid = ndb.KeyProperty(kind='Profile', required=True)  # One profile can have many join requests
    to_pid = ndb.KeyProperty(kind='Profile', required=True)  # many requests to join one club
    club_id = ndb.KeyProperty(kind='Club', required=True)
    status = ndb.StringProperty(required=True)
    join_request_id = ndb.StringProperty(required=True)
    id = join_request_id
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many join requests


class JoinRequestMiniForm(messages.Message):
    """JoinRequestMiniForm -- What's shown on the UI for an join request"""
    from_pid = messages.StringField(1, required=True)
    club_id = messages.StringField(2, required=True)


class JoinClubMiniForm(messages.Message):
    club_id = messages.StringField(1, required=True)
    from_pid = messages.StringField(2, required=True)


class FollowClubMiniForm(messages.Message):
    club_id = messages.StringField(1, required=True)
    from_pid = messages.StringField(2, required=True)


class Comments(ndb.Model):
    pid = ndb.KeyProperty(kind='Profile', required=True)  # One profile can have many comments
    # postId = ndb.KeyProperty(kind=Post,required=True)
    comment_body = ndb.StringProperty(required=True)
    timestamp = ndb.StringProperty(required=True)
    likes = ndb.IntegerProperty()
    postId = ndb.KeyProperty(kind='Post',required=True)
    collegeId = ndb.KeyProperty(kind='CollegeDb', required=True)  # One college has many comments

class CommentsForm(messages.Message):
    pid = messages.StringField(1,required=True)
    comment_body = messages.StringField(2,required=True)
    timestamp = messages.StringField(3,required=True)
    postId = messages.StringField(4,required=True)

class CollegeDb(ndb.Model):
    name = ndb.StringProperty(required=True)
    abbreviation = ndb.StringProperty()
    location = ndb.StringProperty()
    student_count = ndb.IntegerProperty()
    group_count = ndb.IntegerProperty()
    group_list = ndb.KeyProperty(repeated=True)
    student_sup = ndb.StringProperty(required=True)
    alumni_sup = ndb.StringProperty()
    collegeId = ndb.StringProperty()
    sup_emailId = ndb.StringProperty(required=True)


class CollegeDbMiniForm(messages.Message):
    """JoinRequestMiniForm -- What's shown on the UI for an join request"""
    name = messages.StringField(1, required=True)
    abbreviation = messages.StringField(2, required=True)
    location = messages.StringField(3, required=True)
    student_sup = messages.StringField(4, required=True)
    alumni_sup = messages.StringField(5)
    email = messages.StringField(6,required=True)
    phone = messages.StringField(7,required=True)

# Define Response Classes here

class ClubListResponse(messages.Message):
    list = messages.MessageField(ClubMiniForm, 1, repeated=True)

class GetCollege(messages.Message):
    abbreviation = messages.StringField(1)
    collegeId = messages.StringField(2)
    location = messages.StringField(3)
    name = messages.StringField(4)

class ClubRetrievalMiniForm(messages.Message):
    """JoinRequestMiniForm -- What's shown on the UI for an join request"""
    college_id = messages.StringField(1, required=True)

class Colleges(messages.Message):
    collegeList = messages.MessageField(GetCollege,1,repeated=True)


class ProfileRetrievalMiniForm(messages.Message):
    email=messages.StringField(1,required=True)

class Feed(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    # photo = ndb.BlobProperty()
    club_id = messages.StringField(3)  # Many events belong to one club
    # eventId = messages.StringField(4,required=True)
    venue = messages.StringField(4)
    start_date = messages.StringField(5)
    start_time = messages.StringField(6)
    end_time = messages.StringField(7)
    end_date = messages.StringField(8)
    attendees = messages.StringField(9,repeated=True)
    completed = messages.StringField(10)
    views = messages.StringField(11)
    isAlumni = messages.StringField(12)
    event_creator = messages.StringField(13)
    collegeId = messages.StringField(14)
    pid = messages.StringField(15) #the post or event creator
    tags = messages.StringField(16)
    likers = messages.StringField(17,repeated=True)
    timestamp = messages.StringField(18)
    photo = messages.StringField(19)
    clubphoto = messages.StringField(20)

class CollegeFeed(messages.Message):
    items = messages.MessageField(Feed,1,repeated=True)

class RequestMiniForm(messages.Message):
    req_id = messages.StringField(1, required="True")

class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- What's shown on the UI"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)
    '''picture ='''
    photo = messages.StringField(3)
    tags = messages.StringField(5, repeated=True)
    batch = messages.StringField(6)
    branch = messages.StringField(7)
    follows = messages.StringField(8, repeated=True)
    clubsJoined = messages.StringField(9,repeated=True)
    collegeId = messages.StringField(10,required=True)
    isAlumni = messages.StringField(12)
    phone=messages.StringField(13,required=True)
    club_names = messages.MessageField(ClubMiniForm,14,repeated=True)
    #club_names = messages.StringField(14,repeated=True)
    follows_names = messages.StringField(15,repeated=True)
    pid = messages.StringField(16)
    gcmId = messages.StringField(17)

class MessageResponse(messages.Message):
    status = messages.StringField(1)
    text = messages.StringField(2)

class UpdateGCM(messages.Message):
    gcmId = messages.StringField(1)
    email = messages.StringField(2)