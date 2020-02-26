import json
from django.urls import reverse
from django.test import Client, TestCase
from . import uriData
import random as r

c = Client()

class getPictureById(TestCase):
    def test_getPictureById_200(self):
        response = c.get('/api/pictures/1')
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {"picture": {
                         "pictureId": 1, "pictureData": "https://iop.conranshop.co.uk/media/catalog/product/6/3/637237.jpg", "word": "chair"}})
        self.assertIs(type(objectResponse["picture"]["pictureId"]), int)
        self.assertIs(type(objectResponse["picture"]["pictureData"]), str)
        self.assertIs(type(objectResponse["picture"]["word"]), str)
    def test_getPictureById_404_non_existent_id(self):
        response = c.get('/api/pictures/99999')
        self.assertEqual(response.status_code, 404)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": "picture id does not exist",
            "status": "404"
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), str)
    def test_getPictureById_400_non_valid_id(self):
        response = c.get('/api/pictures/wefwe3')
        self.assertEqual(response.status_code,400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": "picture id is not a number",
            "status": "400"
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), str)
        
class postPicture(TestCase):
    def test_postPicture_200_picuture1(self):
        response = c.post('/api/pictures/', {'data': uriData.data1},content_type="application/json")
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'outcome': 'hair_spray'})
        self.assertIs(type(objectResponse["outcome"]), str)
    def test_postPicture_200_picuture2(self):
        response = c.post('/api/pictures/', {'data': uriData.data2},content_type="application/json")
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'outcome': 'television'})
        self.assertIs(type(objectResponse["outcome"]), str)
    def test_postPicture_400(self):
        response = c.post('/api/pictures/', {'data': 'test'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
                         'err': 'Error occured. Please try again'})
    def test_postPicture_400_badrequest_nodata(self):
        response = c.post('/api/pictures/')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'No post data in request', 'status':400})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)

class getUserByUsername(TestCase):
    def test_getUser_200(self):
        response = c.get('/api/users/bbbbb/')
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {"user": {
                         "avatarUrl": 'test3', "language": "hola", "score": 0, "img_id":2}})
        self.assertIs(type(objectResponse["user"]["score"]), int)
        self.assertIs(type(objectResponse["user"]["avatarUrl"]), str)
        self.assertIs(type(objectResponse["user"]["language"]), str)
        self.assertIs(type(objectResponse['user']['img_id']),int)
    def test_getUser_404_non_existent_user(self):
        response = c.get('/api/users/foivhaoidhvioaurh/')
        self.assertEqual(response.status_code, 404)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": "User does not exist",
            "status": 404
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)

class patchUserByUsername(TestCase):
    def test_patchUser_200_request1(self):
        response = c.patch('/api/users/aaaaa/', {'avatarUrl':'www.testExample.com/img.jpg', 'language':'sp'}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertIs(type(objectResponse["user"]["score"]), int)
        self.assertIs(type(objectResponse["user"]["avatarUrl"]), str)
        self.assertIs(type(objectResponse["user"]["language"]), str)
        self.assertIs(type(objectResponse['user']['img_id']),int)
    def test_patchUser_200_request2(self):
        response = c.patch('/api/users/aaaaa/', {'score':2, 'img_id':0}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertIs(type(objectResponse["user"]["score"]), int)
        self.assertIs(type(objectResponse["user"]["avatarUrl"]), str)
        self.assertIs(type(objectResponse["user"]["language"]), str)
        self.assertIs(type(objectResponse['user']['img_id']),int)
    def test_patchUser_400_badrequest1(self):
        response = c.patch('/api/users/aaaaa/', {'score':2, 'language':'fr'}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": 'Can only patch (avatarUrl and language) or (img_id and score) at the same time.',
            "status": 400
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_patchUser_400_badrequest2(self):
        response = c.patch('/api/users/aaaaa/')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": 'No valid patch data in request',
            "status": 400
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_patchUser_404_nonexistant_user(self):
        response = c.patch('/api/users/sdgjfgbeliguberigu/', {'language':'en'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'User does not exist', 'status':404})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    
class postUser(TestCase):
    def test_postUser_201_makes_with_defaults(self):
        randUser = 'TestUser'+str(r.randint(1,10000))+str(r.randint(1,10000))
        response = c.post('/api/users/', {'username': randUser, 'language':'en'}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertIs(type(objectResponse["user"]["score"]), int)
        self.assertIs(type(objectResponse["user"]["avatarUrl"]), str)
        self.assertIs(type(objectResponse["user"]["language"]), str)
        self.assertIs(type(objectResponse['user']['img_id']),int)
    def test_postUser_400_badrequest_nolanguage(self):
        randUser = 'TestUser'+str(r.randint(1,10000))+str(r.randint(1,10000))
        response = c.post('/api/users/', {'username': randUser}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'Missing language from request', 'status':400})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_postUser_400_badrequest_nousername(self):
        response = c.post('/api/users/', {'language': 'en'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'Missing username from request', 'status':400})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_postUser_400_badrequest_nodata(self):
        response = c.post('/api/users/')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'No post data in request', 'status':400})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_postUser_400_user_already_exists(self):
        response = c.post('/api/users/', {'username':'ccccc', 'language':'en'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':'User already exists', 'status':400})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)        

class badMethodTests(TestCase):
    def test_badmethod_pictureID(self):
        response = c.delete('/api/pictures/1')
        self.assertEqual(response.status_code,405)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':"Requested method on URL is unavailable.", 'status':405})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_badmethod_pictureDetection(self):
        response = c.get('/api/pictures/')
        self.assertEqual(response.status_code,405)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':"Requested method on URL is unavailable.", 'status':405})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_badmethod_userCreation(self):
        response = c.get('/api/users/')
        self.assertEqual(response.status_code,405)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':"Requested method on URL is unavailable.", 'status':405})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)
    def test_badmethod_username(self):
        response = c.delete('/api/users/ccccc/')
        self.assertEqual(response.status_code,405)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'msg':"Requested method on URL is unavailable.", 'status':405})
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), int)