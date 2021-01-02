from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from podo_app.models import Profile, ProfileCity, City
import requests
import json


"""
class PostUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        params={"grant_type": "refresh_token", "client_id":, "refresh_token": }###to add
        response=requests.post("https://kauth.kakao.com/oauth/token", params=params)
        response=json.loads(response.text)
        try:
            access_token=response["access_token"]
        except KeyError:
            access_token=None
        self. assertIsNotNone(access_token)
        
        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token": access_token, 
                "social": "Kakao",
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)
        

    def test_post_user_duplicated_username(self):

    def test_post_user_incomplete_request(self):

    def test_post_user_wrong_year(self):

    def test_post_user(self):
        params2={"grant_type": "refresh_token", "client_id":, "refresh_token": }###to add
        response2=requests.post("https://kauth.kakao.com/oauth/token", params=params2)
        response2=json.loads(response.text)
        try:
            access_token2=response2["access_token"]
        except KeyError:
            access_token2=None
        self. assertIsNotNone(access_token2)
        
        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token": access_token2, 
                "social": "Kakao",
            }),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)
##
        #default(participant)
        response = self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "participant",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교",
                "accepted":"False"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #when university and accepted data is not given
        response2 = self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "participantnodata",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #default(instructor)
        response3 = self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "instructor",
                "password": "password",
                "first_name": "Bavin",
                "last_name": "Dyeon",
                "email": "bdv222@snu.ac.kr",
                "role": "instructor",
                "company": "Google", 
                "year":"11"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #when company and year data is not given 
        response4 = self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "instructornodata",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "instructor",
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "participant")
        self.assertEqual(data["email"], "bdv111@snu.ac.kr")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertIn("token", data)
        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "서울대학교")
        self.assertFalse(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)
        self.assertEqual(data["instructor"], None)
        realobject=User.objects.filter(username="participant", email="bdv111@snu.ac.kr", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=ParticipantProfile.objects.filter(user=realobject[0], university="서울대학교", accepted=False)
        self.assertTrue(realobject2)
        

        insufficientdata=response2.json()
        participant2=insufficientdata["participant"]
        self.assertEqual(participant2["university"], "")
        self.assertTrue(participant2["accepted"])
        realobject=User.objects.filter(username="participantnodata", email="bdv111@snu.ac.kr", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=ParticipantProfile.objects.filter(user=realobject[0], university="", accepted=True)
        self.assertTrue(realobject2)

        data2 = response3.json()
        self.assertIn("id", data2)
        self.assertEqual(data2["username"], "instructor")
        self.assertEqual(data2["email"], "bdv222@snu.ac.kr")
        self.assertEqual(data2["first_name"], "Bavin")
        self.assertEqual(data2["last_name"], "Dyeon")
        self.assertIn("last_login", data2)
        self.assertIn("date_joined", data2)
        self.assertIn("token", data2)
        instructor = data2["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "Google")
        self.assertEqual(instructor["year"], 11)
        self.assertIsNone(instructor["charge"])
        self.assertIsNone(data2["participant"])
        realobject=User.objects.filter(username="instructor", email="bdv222@snu.ac.kr", first_name="Bavin", 
            last_name="Dyeon")
        self.assertTrue(realobject)
        realobject2=InstructorProfile.objects.filter(user=realobject[0], company="Google", year=11)
        self.assertTrue(realobject2)

        insufficientdata2=response4.json()
        instructor2=insufficientdata2["instructor"]
        self.assertEqual(instructor2["company"], "")
        self.assertIsNone(instructor2["year"])
        realobject=User.objects.filter(username="instructornodata", email="bdv111@snu.ac.kr", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=InstructorProfile.objects.filter(user=realobject[0], company="", year=None)
        self.assertTrue(realobject2)

        user_count = User.objects.count()
        self.assertEqual(user_count, 5)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 3)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 2)

class PutUserLoginTestCase(TestCase):
    client=Client()
    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user1",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )

    def test_login_user(self):
        response=self.client.put(
            '/api/v1/user/login/', 
            json.dumps({
                "username":"user1",
                "password":"password"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data =  response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "bdv111@snu.ac.kr")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "서울대학교")
        self.assertTrue(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)
        self.assertIsNone(data["instructor"])

        realobject=User.objects.filter(username="user1", email="bdv111@snu.ac.kr", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=ParticipantProfile.objects.filter(user=realobject[0], university="서울대학교", accepted=True)
        self.assertTrue(realobject2)
        
class GetUserTestCase(TestCase):
    client=Client()

    def setUp(self):
        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user1",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='user1').key
        self.userid1=response.json()["id"]

        response2=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user2",
                "password": "password",
                "first_name": "Obama",
                "last_name": "Trump",
                "email": "random123@snu.ac.kr",
                "role": "instructor",
                "company": "Google",
                "year": "2"
            }),
            content_type='application/json'
                )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='user2').key
        self.userid2=response2.json()["id"]

    def test_get_user(self):
        response=self.client.get(
            '/api/v1/user/{a}/'.format(a=self.userid1), 
            HTTP_AUTHORIZATION=self.instructor_token
                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2=self.client.get(
            '/api/v1/user/{b}/'.format(b=self.userid2), 
            HTTP_AUTHORIZATION=self.participant_token            
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        data =  response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "bdv111@snu.ac.kr")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "서울대학교")
        self.assertTrue(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)
        self.assertIsNone(data["instructor"])

        data2 =  response2.json()
        self.assertIn("id", data)
        self.assertEqual(data2["username"], "user2")
        self.assertEqual(data2["email"], "random123@snu.ac.kr")
        self.assertEqual(data2["first_name"], "Obama")
        self.assertEqual(data2["last_name"], "Trump")
        self.assertIn("last_login", data2)
        self.assertIn("date_joined", data2)
        self.assertNotIn("token", data2)

        instructor = data2["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "Google")
        self.assertEqual(instructor["year"], 2)
        self.assertEqual((instructor["charge"]), None)
        self.assertIsNone(data2["participant"])

    def test_get_user_me(self):
        #same as the above function, except for the fact that the 
        #ip given is "me"
        response=self.client.get(
            '/api/v1/user/me/', 
            HTTP_AUTHORIZATION=self.participant_token
                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2=self.client.get(
            '/api/v1/user/me/', 
            HTTP_AUTHORIZATION=self.instructor_token            
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


        data =  response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "user1")
        self.assertEqual(data["email"], "bdv111@snu.ac.kr")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "서울대학교")
        self.assertTrue(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)
        #when there is seminar
        self.assertIsNone(data["instructor"])


        data2 =  response2.json()
        self.assertIn("id", data)
        self.assertEqual(data2["username"], "user2")
        self.assertEqual(data2["email"], "random123@snu.ac.kr")
        self.assertEqual(data2["first_name"], "Obama")
        self.assertEqual(data2["last_name"], "Trump")
        self.assertIn("last_login", data2)
        self.assertIn("date_joined", data2)
        self.assertNotIn("token", data2)

        instructor = data2["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "Google")
        self.assertEqual(instructor["year"], 2)
        self.assertEqual((instructor["charge"]), None)
        self.assertIsNone(data2["participant"])

class PutUserTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "part",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )
        self.participant_token = 'Token ' + Token.objects.get(user__username='part').key

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "inst",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "instructor",
                "year": 1
            }),
            content_type='application/json'
        )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='inst').key

    def test_put_user_wrong_or_incomplete_request(self):
        #no authorization
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "first_name": "Dabin"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #existing username
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "inst"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


        #only first name
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "first_name": "Dabin"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        participant_user = User.objects.get(username='part')
        self.assertEqual(participant_user.first_name, 'Davin')

        #only last name
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "last_name": "Beon"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(participant_user.last_name, 'Byeon')

        #number in first name
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "first_name": "Davin1",
                "last_name": "Byeon"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        participant_user = User.objects.get(username='part')
        self.assertEqual(participant_user.first_name, 'Davin')

        #number in  last name
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "first_name": "Davin",
                "last_name": "Beon1"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(participant_user.last_name, 'Byeon')

        #year<0
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "inst123",
                "email": "bdv111@naver.com",
                "company": "매스프레소",
                "year": -1
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #year=0
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "year": 0
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        instructor_user = User.objects.get(username='inst')
        self.assertEqual(instructor_user.email, 'bdv111@snu.ac.kr')



    def test_put_user_me_participant(self):
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "part123",
                "email": "bdv111@naver.com",
                "university": "경북대학교"
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "part123")
        self.assertEqual(data["email"], "bdv111@naver.com")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "경북대학교")
        self.assertTrue(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)

        self.assertIsNone(data["instructor"])
        participant_user = User.objects.get(username='part123')
        self.assertEqual(participant_user.email, 'bdv111@naver.com')
        realobject=User.objects.filter(username="part123", email="bdv111@naver.com", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=ParticipantProfile.objects.filter(user=realobject[0], university="경북대학교", accepted=True)
        self.assertTrue(realobject2)

        #when university data is not given
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "part456",
                "email": "bdv111@naver.com",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        participant = data["participant"]
        self.assertEqual(participant["university"], "")
        realobject=User.objects.filter(username="part456", email="bdv111@naver.com", first_name="Davin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=ParticipantProfile.objects.filter(user=realobject[0], university="", accepted=True)
        self.assertTrue(realobject2)

        #when university is blank
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "university":""
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        participant = data["participant"]
        self.assertEqual(participant["university"], "")



    def test_put_user_me_instructor(self):
        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "inst123",
                "email": "bdv111@naver.com",
                "first_name": "Dabin",
                "last_name": "Byeon",
                "university": "서울대학교",  # this should be ignored
                "company": "매스프레소",
                "year": 2
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "inst123")
        self.assertEqual(data["email"], "bdv111@naver.com")
        self.assertEqual(data["first_name"], "Dabin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        self.assertIsNone(data["participant"])
        instructor = data["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "매스프레소")
        self.assertEqual(instructor["year"], 2)
        self.assertIsNone(instructor["charge"])

        instructor_user = User.objects.get(username='inst123')
        self.assertEqual(instructor_user.email, 'bdv111@naver.com')
        realobject=User.objects.filter(username="inst123", email="bdv111@naver.com", first_name="Dabin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=InstructorProfile.objects.filter(user=realobject[0], 
            company="매스프레소", year=2)
        self.assertTrue(realobject2)


        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "username": "inst456",
                "email": "bdv111@naver.com",
                "first_name": "Dabin",
                "last_name": "Byeon",
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        instructor = data["instructor"]
        self.assertEqual(instructor["company"], "")
        self.assertIsNone(instructor["year"])
        realobject=User.objects.filter(username="inst456", email="bdv111@naver.com", first_name="Dabin", 
            last_name="Byeon")
        self.assertTrue(realobject)
        realobject2=InstructorProfile.objects.filter(user=realobject[0], 
            company="", year=None)
        self.assertTrue(realobject2)


        response = self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "company": "",  # this should be ignored
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        instructor = data["instructor"]
        self.assertEqual(instructor["company"], "")

class PostUserParticipantTestCase(TestCase):
    client=Client()

    def setUp(self):
        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user1",
                "password": "password",
                "first_name": "Davin",
                "last_name": "Byeon",
                "email": "bdv111@snu.ac.kr",
                "role": "participant",
                "university": "서울대학교"
            }),
            content_type='application/json'
        )        
        self.participant_token = 'Token ' + Token.objects.get(user__username='user1').key

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user2",
                "password": "password",
                "first_name": "Obama",
                "last_name": "Trump",
                "email": "random123@snu.ac.kr",
                "role": "instructor",
                "company": "Google",
                "year": "2"
            }),
            content_type='application/json'
                )
        self.instructor_token = 'Token ' + Token.objects.get(user__username='user2').key

        self.client.post(
            '/api/v1/user/',
            json.dumps({
                "username": "user3",
                "password": "password",
                "first_name": "Obama",
                "last_name": "Trump",
                "email": "random123@snu.ac.kr",
                "role": "instructor",
                "company": "Google",
                "year": "2"
            }),
            content_type='application/json'
                )
        self.instructor_token2 = 'Token ' + Token.objects.get(user__username='user3').key


        user_count = User.objects.count()
        self.assertEqual(user_count, 3)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 1)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 2)


    def test_post_user_participant_wrong_role(self):
        response=self.client.post(
            '/api/v1/user/participant/',
            json.dumps({
                "university":"SNU",
                "accepted":False,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_post_user_participant(self):

        response=self.client.post(
            '/api/v1/user/participant/',
            json.dumps({
                "university":"SNU",
                "accepted":False,
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data =  response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "user2")
        self.assertEqual(data["email"], "random123@snu.ac.kr")
        self.assertEqual(data["first_name"], "Obama")
        self.assertEqual(data["last_name"], "Trump")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "SNU")
        self.assertFalse(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)
        #when there is seminar

        instructor = data["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "Google")
        self.assertEqual(instructor["year"], 2)
        self.assertEqual((instructor["charge"]), None)
        
        user_count = User.objects.count()
        self.assertEqual(user_count, 3)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 2)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 2)

        #cannot apply again
        response=self.client.post(
            '/api/v1/user/participant/',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        user_count = User.objects.count()
        self.assertEqual(user_count, 3)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 2)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 2)


        #when university and accepted information is not given
        response=self.client.post(
            '/api/v1/user/participant/',
            HTTP_AUTHORIZATION=self.instructor_token2
        )
        data =  response.json()
        
        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertEqual(participant["university"], "")
        self.assertTrue(participant["accepted"])

        user_count = User.objects.count()
        self.assertEqual(user_count, 3)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 3)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 2)
"""
