from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from podo_app.models import Profile, ProfileCity, City, Product
import requests
import json
import responses

Kakao_response_good={
        "id": 1574749689,
        "connected_at": "2020-12-26T09:26:07Z",
        "properties": {
            "nickname": "임종원",
            "profile_image": "kalaklakl",
            "thumbnail_image": "http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg"
        },
        "kakao_account": {
            "profile_needs_agreement": False,
            "profile": {
                "nickname": "임종원",
                "thumbnail_image_url": "http://k.kakaocdn.net/dn/boreK1/btqSaUGPrly/STWzMEuUCPCLlphLZhxr51/img_110x110.jpg",
                "profile_image_url": "http://k.kakaocdn.net/dn/boreK1/btqSaUGPrly/STWzMEuUCPCLlphLZhxr51/img_640x640.jpg"
            }
        }
    }
Kakao_response_bad={
        "error": "this access token does not exist"
    }

Google_response_good={
        "iss": "https://accounts.google.com",
        "azp": "407408718192.apps.googleusercontent.com",
        "aud": "407408718192.apps.googleusercontent.com",
        "sub": "110134255854457775065",
        "at_hash": "R004kD_6LAaV5ssaABo9fg",
        "name": "­임종원",
        "picture": "https://lh4.googleusercontent.com/-3QWIsZqGtxU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmVmRZeQWyesmpMuYOo0qop0a3pzA/s96-c/photo.jpg",
        "given_name": "임종원",
        "family_name": "­",
        "locale": "ko",
        "iat": "1609646968",
        "exp": "1609650568",
        "alg": "RS256",
        "kid": "26129ba543c56e9fbd53dfdcb7789f8bf8f1a1a1",
        "typ": "JWT"
        }    

Google_response_bad={
        "error": "invalid_token",
        "error_description": "Invalid Value"
    }        

class PostUserTestCase(TestCase):
    client = Client()
    @responses.activate
    def test_post_user_create_user(self):
        responses.add(
            responses.GET, 
            "https://oauth2.googleapis.com/tokeninfo?id_token=good_response", 
            json=Google_response_good
        )
        responses.add(
            responses.GET, 
            "https://oauth2.googleapis.com/tokeninfo?id_token=bad_response", 
            json=Google_response_bad
        )
        responses.add(
            responses.GET, 
            "https://kapi.kakao.com/v2/user/me",
            headers= {"Authorization": "Bearer good_response"},
            json=Kakao_response_good
        )
        responses.add(
            responses.GET, 
            "https://kapi.kakao.com/v2/user/me",
            headers= {"Authorization": "Bearer bad_response"},##
            json=Kakao_response_bad
        )

        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"good_response",
                "social":"Kakao",
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)
#specifications
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "임종원")
        self.assertEqual(data["nickname"], "임종원")
        self.assertEqual(data["image"], "http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        self.assertIn("token", data)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Kakao_1574749689")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)


        response2=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"good_response",
                "social":"Google"
            }),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)
##specifications

        data = response2.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "­임종원")
        self.assertEqual(data["nickname"], "­임종원")
        self.assertEqual(data["image"], "https://lh4.googleusercontent.com/-3QWIsZqGtxU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmVmRZeQWyesmpMuYOo0qop0a3pzA/s96-c/photo.jpg")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        self.assertIn("token", data)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Google_110134255854457775065")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)

##error responses
        response3=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"bad_response",
                "social":"Kakao"
            }),
            content_type='application/json'
        )

        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)

        data=response3.json()
        self.assertIn("error", data)

        response4=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"bad_response",
                "social":"Google",
            }),
            content_type='application/json'
        )

        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)        

        data=response4.json()
        self.assertIn("error", data)

    @responses.activate
    def test_post_user_social_login(self):
        responses.add(
            responses.GET, 
            "https://oauth2.googleapis.com/tokeninfo?id_token=good_response", 
            json=Google_response_good
        )
        responses.add(
            responses.GET, 
            "https://kapi.kakao.com/v2/user/me",
            headers= {"Authorization": "Bearer good_response"},
            json=Kakao_response_good
        )

        #create an account, and POST /user/ with the same username(Google)
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)

        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"good_response",
                "social":"Google",
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)

#specifications
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "임종원")
        self.assertEqual(data["nickname"], "임종원nickname")
        self.assertEqual(data["image"], "https://podo-bucket.s3.ap-northeast-2.amazonaws.com/media/http%3A/k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        self.assertIn("token", data)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Google_110134255854457775065")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)


        #create an account, and POST /user/ with the same username(Kakao)
        user=User.objects.create(first_name="임종원2", username="Kakao_1574749689")
        Profile.objects.create(user=user, nickname="임종원2nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_640x640.jpg")
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)

        response2=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"",
                "social":"Kakao"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(profile_count, 2)

#specifications
        data = response2.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "임종원2")
        self.assertEqual(data["nickname"], "임종원2nickname")
        self.assertEqual(data["image"], "https://podo-bucket.s3.ap-northeast-2.amazonaws.com/media/http%3A/k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_640x640.jpg")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        self.assertIn("token", data)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Kakao_1574749689")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)

    @responses.activate
    def test_post_user_no_token_response(self):
        responses.add(
            responses.GET, 
            "https://oauth2.googleapis.com/tokeninfo?id_token=no_response", 
            json=""
        )
        responses.add(
            responses.GET, 
            "https://kapi.kakao.com/v2/user/me",
            headers= {"Authorization": "Bearer no_response"},
            json=""
        )
        #when token response is None
        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"no_response",
                "social":"Kakao"
            }),
            content_type='application/json')
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            
        data=response.json()
        self.assertEqual(data["error"], "Oauth has not returned any data")

        response2=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"no_response",
                "social":"Google"
            }),
            content_type='application/json')

        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
            
        data=response2.json()
        self.assertEqual(data["error"], "Oauth has not returned any data")

    def test_post_user_wrong_social_parameter(self):
        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"",
                "social":"Github",
            }),
            content_type='application/json')

        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
        data=response.json()
        self.assertEqual(data["error"], "'social' parameter is wrong")        

    @responses.activate
    def test_post_user_no_name_given(self):
        Kakao_response_noname={
                "id": 1574749689,
                "connected_at": "2020-12-26T09:26:07Z",
                "properties": {
                    "profile_image": "http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_640x640.jpg",
                    "thumbnail_image": "http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg"
                },
                "kakao_account": {
                    "profile_needs_agreement": False,
                    "profile": {
                        "thumbnail_image_url": "http://k.kakaocdn.net/dn/boreK1/btqSaUGPrly/STWzMEuUCPCLlphLZhxr51/img_110x110.jpg",
                        "profile_image_url": "http://k.kakaocdn.net/dn/boreK1/btqSaUGPrly/STWzMEuUCPCLlphLZhxr51/img_640x640.jpg"
                    }
                }
            }
        Google_response_noname={
                "iss": "https://accounts.google.com",
                "azp": "407408718192.apps.googleusercontent.com",
                "aud": "407408718192.apps.googleusercontent.com",
                "sub": "110134255854457775065",
                "at_hash": "R004kD_6LAaV5ssaABo9fg",
                "picture": "https://lh4.googleusercontent.com/-3QWIsZqGtxU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmVmRZeQWyesmpMuYOo0qop0a3pzA/s96-c/photo.jpg",
                "family_name": "­",
                "locale": "ko",
                "iat": "1609646968",
                "exp": "1609650568",
                "alg": "RS256",
                "kid": "26129ba543c56e9fbd53dfdcb7789f8bf8f1a1a1",
                "typ": "JWT"
                }

        responses.add(
            responses.GET, 
            "https://oauth2.googleapis.com/tokeninfo?id_token=no_name", 
            json=Google_response_noname
        )
        responses.add(
            responses.GET, 
            "https://kapi.kakao.com/v2/user/me",
            headers= {"Authorization": "Bearer no_name"},
            json=Kakao_response_noname
        )


        response=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"no_name",
                "social":"Kakao"
            }),
            content_type='application/json')
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            
        data=response.json()
        self.assertEqual(data["error"], "'full_name' is required")        

        response2=self.client.post(
            '/api/v1/user/',
            json.dumps({
                "access_token":"no_name",
                "social":"Google"
            }),
            content_type='application/json')
        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
            
        data=response2.json()
        self.assertEqual(data["error"], "'full_name' is required")        

class GetUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)

    def test_get_user(self):
        response=self.client.get(
            '/api/v1/user/me/',
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "임종원")
        self.assertEqual(data["nickname"], "임종원nickname")
        self.assertEqual(data["image"], "https://podo-bucket.s3.ap-northeast-2.amazonaws.com/media/http%3A/k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Google_110134255854457775065")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)
        
    def test_get_user_unauthorized(self):
        response=self.client.get(
            '/api/v1/user/',
            content_type='application/json')
        
class PutUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)        
        
    def test_put_user(self):
        response=self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "full_name":"jongwon",
                "nickname":"Carlos"
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["full_name"], "jongwon")
        self.assertEqual(data["nickname"], "Carlos")
        self.assertEqual(data["temperature"], 36.5)
        self.assertEqual(data["products_bought"], 0)
        self.assertEqual(data["products_sold"], 0)
        realobject=User.objects.filter(id=data["id"], first_name=data["full_name"])
        self.assertTrue(realobject)
        self.assertEqual(realobject[0].username, "Google_110134255854457775065")
        realobject2=Profile.objects.filter(user=realobject[0], nickname=data["nickname"], temperature=data["temperature"], products_bought=data["products_bought"], products_sold=data["products_sold"])
        self.assertTrue(realobject2)

    def test_put_user_unauthorized(self):
        response=self.client.put(
            '/api/v1/user/me/',
            json.dumps({
                "full_name":"jongwon",
                "nickname":"Carlos",
                "image":"https://lh4.googleusercontent.com/-3QWIsZqGtxU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmVmRZeQWyesmpMuYOo0qop0a3pzA/s96-c/photo.jpg"
            }),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_user_wrong_pk(self):
        response=self.client.put(
            '/api/v1/user/1/',
            json.dumps({
                "full_name":"jongwon",
                "nickname":"Carlos",
                "image":"https://lh4.googleusercontent.com/-3QWIsZqGtxU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucmVmRZeQWyesmpMuYOo0qop0a3pzA/s96-c/photo.jpg"
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data=response.json()
        self.assertEqual(data["error"], "Can't update other user's information")

class DelUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)

    def test_del_user(self):
        response=self.client.delete(
            '/api/v1/user/me/',
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')

        user_count = User.objects.count()
        profile_count= Profile.objects.count()
        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_user_unauthorized(self):
        response=self.client.delete(
            '/api/v1/user/me/',
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_del_user_wrong_pk(self):
        response=self.client.delete(
            '/api/v1/user/1/',
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        data=response.json()
        self.assertEqual(data["error"], "Can't update other user's information")
            

class PutUserCityTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        profile=Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)
        cities=City.objects.all().order_by('id')

        ProfileCity.objects.create(profile=profile, city=cities[0])        
        ProfileCity.objects.create(profile=profile, city=cities[1])        

    def test_put_user_city(self):
    ##change both
        response=self.client.put(
            '/api/v1/user/city/',
            json.dumps({
                "city_id_1":3,
                "city_id_2":4,
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profilecity_count=ProfileCity.objects.count()
        self.assertEqual(2, profilecity_count)

        data=response.json()
        self.assertIn("id", data)
        self.assertEqual(data["nickname"], "임종원nickname")
        self.assertIn("city", data)

        city=data["city"]
        self.assertEqual(city[0]["city_id"], 3)
        self.assertEqual(city[0]["city_name"], "용산구")
        self.assertEqual(city[1]["city_id"], 4)
        self.assertEqual(city[1]["city_name"], "성동구")
#        realobject=ProfileCity.objects().filter(profile=profile)
        

    ##erase both
        response2=self.client.put(
            '/api/v1/user/city/',
            json.dumps({
                "city_id_1":0,
                "city_id_2":0,
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        profilecity_count=ProfileCity.objects.count()
        self.assertEqual(0, profilecity_count)

        data=response2.json()
        self.assertIn("id", data)
        self.assertEqual(data["nickname"], "임종원nickname")
        self.assertIn("city", data)
        self.assertListEqual(data["city"], [])

    ##create both
        response3=self.client.put(
            '/api/v1/user/city/',
            json.dumps({
                "city_id_1":5,
                "city_id_2":6,
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        profilecity_count=ProfileCity.objects.count()
        self.assertEqual(2, profilecity_count)

        data=response3.json()
        self.assertIn("id", data)
        self.assertEqual(data["nickname"], "임종원nickname")
        self.assertIn("city", data)

        city=data["city"]
        self.assertEqual(city[0]["city_id"], 5)
        self.assertEqual(city[0]["city_name"], "광진구")
        self.assertEqual(city[1]["city_id"], 6)
        self.assertEqual(city[1]["city_name"], "동대문구")
#        realobject=ProfileCity.objects().filter(profile=profile)

    def test_put_user_city_wrong_parameter(self):
        response=self.client.put(
            '/api/v1/user/city/',
            json.dumps({
                "city_id_1":44,
                "city_id_2":1,
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        profilecity_count=ProfileCity.objects.count()
        self.assertEqual(2, profilecity_count)

        data=response.json()
#actual object check 
        self.assertEqual(data["error"], "there is no city with the given id")
       
    def test_put_user_city_unauthorized(self):
        response=self.client.put(
            '/api/v1/user/city/',
            json.dumps({
                "city_id_1":3,
                "city_id_2":4,
            }),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetUserCityTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)

    def test_get_user_city(self):
        response=self.client.get(
            '/api/v1/user/city/',
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data=response.json()
        self.assertIn("city", data)        
        city=data["city"]

        cities=["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구","강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", 
        "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]
        for i in range(0, 25):
            self.assertEqual(city[i]["city_name"], cities[i])

    def test_get_user_city_unauthorized(self):
        response=self.client.get(
            '/api/v1/user/city/',
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetUserProductTestCase(TestCase):
    client = Client()
    def setUp(self):
        user=User.objects.create(first_name="임종원", username="Google_110134255854457775065")
        profile=Profile.objects.create(user=user, nickname="임종원nickname", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        self.token, created=Token.objects.get_or_create(user=user)

        user2=User.objects.create(first_name="임종원2", username="Kakao_110134255854457775065")
        profile2=Profile.objects.create(user=user, nickname="임종원nickname2", image="http://k.kakaocdn.net/dn/dfNRfx/btqRt5WG8al/33Qo8aKKPmqpZ4LWdR5jC1/img_110x110.jpg")
        city=City.objects.get(id=1)
        for i in range(1, 16):
            Product.objects.create(seller=profile, name="first_{num}".format(num=i), price=0, allow_suggest=False,  city=city, category="examplecategory", status=1)
        for i in range(1, 16):
            Product.objects.create(seller=profile2, name="second_{num}".format(num=i), price=0, allow_suggest=False, city=city, category="examplecategory", status=1)


"""
    def test_get_user_product(self):
        response=self.client.get(
            '/api/v1/user/product/',
            json.dumps({
                "page": "1",
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data=response.json()
        self.assertIn("page")
        self.assertIn("product")
        page=data["page"]
        product=data["product"]
        self.assertEqual(page["product_count"], 15)
        self.assertEqual(page["page_count"], 2)
        self.assertEqual(page["current_page"], 1)
        self.assertEqual(len(product), 10)
        for i in range(1, 11):
            self.assertEqual(product[i]["name"], "first_{num}".format(num=i))
            
        response2=self.client.get(
            '/api/v1/user/product/',
            json.dumps({
                "page":"2" 
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data=response2.json()
        self.assertIn("page")
        self.assertIn("product")
        page=data["page"]
        product=data["product"]
        self.assertEqual(page["product_count"], 15)
        self.assertEqual(page["page_count"], 2)
        self.assertEqual(page["current_page"], 2)
        self.assertEqual(len(product), 5)
        for i in range(1, 6):
            self.assertEqual(product[i]["name"], "first_{num}".format(num=i+10))

    def test_get_user_product_wrong_parameter(self):
        response=self.client.get(
            '/api/v1/user/product/',
            json.dumps({
                "page":"100"
            }),
            HTTP_AUTHORIZATION="Token {token}".format(token=self.token.key),          
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "'page' parameter is not given")

    def test_get_user_product_unauthorized(self):
        response=self.client.get(
            '/api/v1/user/product/',
            json.dumps({
                "page": "1"
            }),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
"""