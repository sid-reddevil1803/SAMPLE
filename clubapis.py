from datetime import datetime
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from Models import ClubRequestMiniForm, PostMiniForm
from Models import Club, Post_Request, Post
from Models import Club_Creation
from Models import Profile
from Models import CollegeDb
from Models import CollegeDbMiniForm
from Models import ClubMiniForm
from Models import GetClubMiniForm
from Models import JoinClubMiniForm
from Models import FollowClubMiniForm
from Models import ClubListResponse
from Models import ProfileMiniForm
EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID

@endpoints.api(name='clubs', version='v1', 
    allowed_client_ids=[API_EXPLORER_CLIENT_ID],
    scopes=[EMAIL_SCOPE])

class ClubApi(remote.Service):
   
   
   def createClub(self,requestentity=None):
        
        #When createClubRequest is called  

        print("Request Entity for Create Club ", requestentity)
        clubRequest = Club_Creation()
        #college = CollegeDb(name = 'NITK',student_sup='Anirudh',collegeId='NITK-123')
        #college_key = college.put()

        college = CollegeDb.query(CollegeDb.name == requestentity.college_name).fetch(1)
        print(college[0])
        college_key = college[0].key

        print("Retrieved College Key is ",college_key)

        if requestentity and college :
            for field in ('abbreviation','club_name','from_pid','to_pid','club_id','isAlumni','collegeId','club_creation_id'):
                if hasattr(requestentity, field):
                    
                    val = getattr(requestentity, field)
                    if val:
                        print("entered second val")
                        setattr(clubRequest, field, str(val))
                elif field == "from_pid":
                     print("Entered from_pid")
                     profile =  Profile(
                            name = 'SiddharthSend',
                            email = 'sid.tiger184@gmail.com',
                            phone = '7760531993',
                            password = '1803mutd1',
                            pid = '1234',
                            isAlumni='N',
                            collegeId=college_key
                            )
                     profile_key = profile.put()
                     print("Finished frompid")
                     setattr(clubRequest, field, profile_key)
                elif field == "to_pid":
                     print("Entered To PID")
                     profile =  Profile(
                               name = 'SiddharthRec',
                               email = 'sid.tiger183@gmail.com',
                               phone = '7760531994',
                               password = '1803mutd',
                               pid = '5678',
                               isAlumni='N',
                               collegeId=college_key
                               )
                     profile_key = profile.put()

                     setattr(clubRequest, field, profile_key)
                elif field == "club_id":
                     setattr(clubRequest, field, "9999")
                elif field == "isAlumni":
                     setattr(clubRequest, field, "N")
                elif field == "collegeId":
                     setattr(clubRequest, field, college_key)
                elif field == "club_creation_id":
                     setattr(clubRequest, field, "1")
        clubRequest.put()

        return clubRequest


   def createClubAfterApproval(self,requestentity=None):

        if requestentity:
            newClub = Club()
            newClub.abbreviation = requestentity.abbreviation
            newClub.clubId = requestentity.club_id
            newClub.admin = requestentity.from_pid
            newClub.collegeId = requestentity.collegeId
            newClub.name = requestentity.club_name
            newClub.isAlumni = requestentity.isAlumni

            newClub.put()

            #print("college Id of new ", newClub.collegeId.get())
            college = newClub.collegeId.get()
            #college = CollegeDb.query(CollegeDb.collegeId == newClub.collegeId.get().collegeId).fetch(1)
            print ("The retrieved college is ",college)

            if(college):
              college.group_list.append(newClub.key)
              print(college.group_list)

              college.put()

        return newClub

   #@endpoints.method(ClubRequestMiniForm,ClubMiniForm,path='getClub', http_method='POST', name='getClub')
   def getClub(self,requestentity=None):

        print("Request entity is",requestentity)

        if requestentity:
            clubQuery = Club.query(Club.name == requestentity.name).filter(Club.abbreviation == requestentity.abbreviation).fetch(1)
            print(clubQuery)

            if clubQuery:
             college = CollegeDb.query(CollegeDb.collegeId == requestentity.collegeId.get().collegeId).fetch(1)
             profile = Profile.query(Profile.pid == requestentity.admin.get().pid).fetch(1)
             retClub = ClubMiniForm()
             retClub.admin = profile[0].name
             retClub.abbreviation = requestentity.abbreviation
             retClub.name = requestentity.name
             retClub.collegeName = college[0].name



        return retClub

   @endpoints.method(GetClubMiniForm,ClubMiniForm,path='getClub', http_method='POST', name='getClub')
   def getClubApi(self,request):

        print("Request entity is",request)

        if request:
            clubQuery = Club.query(Club.name == request.name).filter(Club.abbreviation == request.abbreviation).fetch(1)
            #print(clubQuery)
            collegeidret = clubQuery[0].collegeId
            adminret = clubQuery[0].admin
            #print(collegeidret)
            #print("Admin ret",adminret)
            if clubQuery:
             college = CollegeDb.query(CollegeDb.collegeId == collegeidret.get().collegeId).fetch(1)
             profile = Profile.query(Profile.pid == adminret.get().pid).fetch(1)
             retClub = ClubMiniForm()
             retClub.clubId = clubQuery[0].clubId
             retClub.admin = profile[0].name
             retClub.abbreviation = clubQuery[0].abbreviation
             retClub.name = clubQuery[0].name
             retClub.collegeName = college[0].name



        return retClub

   @endpoints.method(JoinClubMiniForm,ClubMiniForm,path='joinClub', http_method='POST', name='joinClub')
   def joinClubApi(self,request):

        #print("Request entity is",request)

        if request:


            collegequery = CollegeDb.query(CollegeDb.name == request.college_name).fetch(1)
            collegekey = collegequery[0].key
            clubQuery = Club.query(Club.name == request.club_name).filter(Club.collegeId == collegekey).fetch(1) #rretrieved the club
            profileret = Profile.query(Profile.name == request.name).filter(Profile.email == request.email).fetch(1)
            #print("Retrieved Profile ",profileret)


            if (collegequery and clubQuery and profileret) :
                #add profile to club
                currentClub = clubQuery[0]
                currentClub.members.append(profileret[0].key)
                currentClub.followers.append(profileret[0].key)
                currentClub.put()

                currentProfile = profileret[0]
                currentProfile.clubsJoined.append(currentClub.key)
                currentProfile.follows.append(currentClub.key)
                currentProfile.put()



        return None

   @endpoints.method(FollowClubMiniForm,ClubMiniForm,path='followClub', http_method='POST', name='followClub')
   def followClubApi(self,request):

        print("Request entity is",request)

        if request:

            collegequery = CollegeDb.query(CollegeDb.name == request.college_name).fetch(1)
            collegekey = collegequery[0].key
            clubQuery = Club.query(Club.name == request.club_name).filter(Club.collegeId == collegekey).fetch(1) #rretrieved the club
            profileret = Profile.query(Profile.name == request.name).filter(Profile.email == request.email).fetch(1)
            #print("Retrieved Profile ",profileret)


            if (collegequery and clubQuery and profileret) :
                #add profile to club
                currentClub = clubQuery[0]
                currentClub.followers.append(profileret[0].key)
                currentClub.put()

                currentProfile = profileret[0]
                currentProfile.follows.append(currentClub.key)
                currentProfile.put()



        return None

   @endpoints.method(CollegeDbMiniForm,ClubListResponse,path='getClubList', http_method='POST', name='getClubList')
   def getClubListApi(self,request):


        list_of_clubs = ClubListResponse()
        print("Request entity is",request)

        if request:
            collegequery = CollegeDb.query(CollegeDb.name == request.name).fetch(1)
            print("Have i retrieved the college ", collegequery)

            if(collegequery[0]):


                for obj in collegequery[0].group_list :
                   ret_club = obj.get()

                   format_club = ClubMiniForm()

                   format_club.name = ret_club.name

                   format_club.abbreviation = ret_club.abbreviation

                   format_club.admin = ret_club.admin.get().name

                   format_club.collegeName = ret_club.collegeId.get().name

                   format_club.description = ret_club.description


                   list_of_clubs.list.append(format_club)

                print("List of Objects ",list_of_clubs)




        return list_of_clubs






   def createCollege(self, requestentity=None):
        
        newCollege = CollegeDb()
        query = CollegeDb.query()
        print "The data got on querying is " , query , " type is ", type(query), "\n"
        count = 0
        names = []
        location = []
        """profile =  Profile(name = 'RJJ',
                            email = 'rohitjjoseph@gmail.com',
                            phone = '7760532293',
                            password = '13211',
                            pid = '1234',
                            isAlumni='N',
                            collegeId= 'NIoTK')
        profile_key = profile.put()
        """
        for records in query:
           print"The name of the college is ", records.name , " and location is " , records.location
           names.append(records.name)
           location.append(records.location)
           count += 1
           print "\n"
        
        print "count is, " , count        
        
        collegeName = ""
        if requestentity:
            for field in ('name','abbreviation','location','student_sup','alumni_sup'):
                val = getattr(requestentity, field)
                if field == "name":
                    collegeName = getattr(requestentity, field).strip()
                if val:
                    val = val.strip()
                    print("Value is",val)
                    setattr(newCollege, field, str(val))
            #Now setting the attributes not recieved from the front-end.
            setattr(newCollege, 'student_count', 0)
            setattr(newCollege, 'group_count', 0)
            newlist = []
            setattr(newCollege, 'group_list', newlist)
            """ Making CollegeId"""
            newString = ""
            newString = collegeName[0]
            for x in xrange(len(collegeName)):
                if(collegeName[x]==' '):
                    newString+=collegeName[x+1]
                    
            setattr(newCollege, 'collegeId', newString)

        print(newCollege)
        flag = 0
        for var in xrange(count):
            if(newCollege.name==names[var] and newCollege.location==location[var]):
                flag=1
                
        if(flag):
            print "Sorry already existing record"
        
        else:
            print "Unique"
            newCollege.put()

        return newCollege

   def postRequest(self, requestentity=None):

        post_request = Post_Request()
        college = CollegeDb(name = 'NITK',student_sup='Anirudh',collegeId='NITK-123')
        college_key = college.put()
        query = CollegeDb.query()
        profile =  Profile(name = 'RJJ',
                            email = 'rohitjjoseph@gmail.com',
                            phone = '7760532293',
                            password = '13211',
                            pid = '1234',
                            isAlumni='N',
                            collegeId= college_key)
        profile_key = profile.put()
        print("Finished frompid")
                    #setattr(clubRequest, field, profile_key)


        if requestentity:
            for field in ('to_pid','club_id','description','status','post_request_id','collegeId','title'):
                if hasattr(requestentity, field):
                    print(field,"is there")
                    val = getattr(requestentity, field)
                    if(field=="club_id"):
                        setattr(post_request, field, college_key)
                    elif val:
                        print("Value is",val)
                        setattr(post_request, field, str(val))



                elif field == "to_pid":
                    """profile =  Profile(
                               name = 'SiddharthRec',
                               email = 'sid.tiger183@gmail.com',
                               phone = '7760531994',
                               password = '1803mutd',
                               pid = '5678',
                               isAlumni='N',
                               collegeId=college_key
                               )
                    profile_key = profile.put()"""
                    person = profile_key.get()
                    print "Person's email-id ", person.email
                    person_collegeId = person.collegeId
                    print "His college Id ", person.collegeId
                    college_details = person_collegeId.get()
                    print "The sup is ", college_details.student_sup
                    print("Finished to-pid")

                    setattr(post_request, field, profile_key)
                    setattr(post_request, 'from_pid', profile_key)
                elif field == "status":
                    setattr(post_request, field, "Yes")
                elif field == "post_request_id":
                    setattr(post_request, field, "ABCD123")
                elif field == "collegeId":
                    setattr(post_request, field, person_collegeId)

        print("About to createClubRequest")
        print(post_request)
        post_request.put()

        return post_request

   def postEntry(self,requestentity=None):

        newPost = Post()
        college = CollegeDb(name = 'NITK',student_sup='Anirudh',collegeId='NITK-123')
        college_key = college.put()
        query = CollegeDb.query()
        profile =  Profile(name = 'RJJ',
                            email = 'rohitjjoseph@gmail.com',
                            phone = '7760532293',
                            password = '13211',
                            pid = '1234',
                            isAlumni='N',
                            collegeId= college_key)
        profile_key = profile.put()
        print("Finished from pid")
                    #setattr(clubRequest, field, profile_key)

        #Change the below portion once you incorporate actual Ids.

        if requestentity:
            for field in ('title','description','club_id','from_pid','likes','postId','views','collegeId'):

                if hasattr(requestentity, field):
                    print(field,"is there")
                    val = getattr(requestentity, field)
                    if(field=="club_id"):
                        print "Club_Id stage"
                        setattr(newPost, field, college_key)

                    elif field == "from_pid":
                        print "Entered here"
                        person = profile_key.get()
                        print "Person's email-id ", person.email
                        person_collegeId = person.collegeId
                        print "His college Id ", person.collegeId
                        college_details = person_collegeId.get()
                        print "The sup is ", college_details.student_sup
                        setattr(newPost, field, "SDBJFB")
                        print "Put PID"
                        setattr(newPost,'collegeId',person_collegeId)
                        print "Put college id"

                    elif val:
                        print("Value is",val)
                        setattr(newPost, field, str(val))

                elif field == "likes":
                    setattr(newPost, field, 0)
                elif field == "postId":
                    setattr(newPost, field, "ABCD123")
                elif field == "views":
                    setattr(newPost, field, 0)


        print("About to createClubRequest")
        print(newPost)
        newPost.put()

        return newPost



   @endpoints.method(ClubRequestMiniForm,ClubMiniForm,path='club', http_method='POST', name='createClubRequest')
   def createClubRequest(self, request):

        retClub = ClubMiniForm()
        college_ret = CollegeDb.query(CollegeDb.name == request.college_name).fetch(1)

        print("College Ret",college_ret)
        if(college_ret):
           club_ret = Club.query(Club.name == request.club_name).filter(Club.abbreviation == request.abbreviation).filter(Club.collegeId == college_ret[0].key).fetch(1)

           print("Club Ret",club_ret)
           if(len(club_ret) == 0):
              clubRequest = self.createClub(request)
              #insert logic for request approval
              newClub = self.createClubAfterApproval(clubRequest)
              print ("The new club is",newClub)
              retClub = self.getClub(newClub)
        return retClub


   @endpoints.method(CollegeDbMiniForm,message_types.VoidMessage,path='collegeDB', http_method='POST', name='createCollege')
   def createCollegeDb(self, request):
        print("Entered CollegeDb Portion")
        clubRequest = self.createCollege(request)
        print("Finished entering a college")


   @endpoints.method(PostMiniForm,message_types.VoidMessage,path='postRequest', http_method='POST', name='postRequest')
   def createPostRequest(self, request):
        print("Entered Post Request Portion")
        clubRequest = self.postRequest(request)
        print("Inserted into the post request table")


   @endpoints.method(PostMiniForm,message_types.VoidMessage,path='postEntry', http_method='POST', name='postEntry')
   def createPost(self, request):
        print("Entered Post Entry Portion")
        clubRequest = self.postEntry(request)
        print("Inserted into the posts table")
        


   @endpoints.method(message_types.VoidMessage,message_types.VoidMessage,path='insertUnique', http_method='POST', name='insertUnique')
   def insertUnique(self,request):

        #This method is just a reference in order for you to reuse this code in order to insert unique entries in the DB
        college = CollegeDb(name = 'NITK',student_sup='Anirudh',collegeId='NITK-123')
        college_key = college.put()
        query = CollegeDb.query()

        profile =  Profile(name = 'RJJ',
                            email = 'rohitjjoseph@gmail.com',
                            phone = '7760532293',
                            password = '13211',
                            pid = '1234',
                            isAlumni='N',
                            collegeId= college_key)

        profileret = Profile.query(Profile.pid == profile.pid).fetch(1)

        print("A is ", profileret)
        if profileret :
          print("Not inserting")
        else :
          print("Inserting")
          profile_key = profile.put()

api = endpoints.api_server([ClubApi]) # register API	
