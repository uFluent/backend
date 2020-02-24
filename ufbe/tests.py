import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . import uriData

class getPictureById(APITestCase):
    def test_getPictureById_200(self):
        response = self.client.get('/picture/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {"picture": {
                         "pictureId": 1, "pictureData": "https://iop.conranshop.co.uk/media/catalog/product/6/3/637237.jpg", "word": "chair"}})
        self.assertIs(type(objectResponse["picture"]["pictureId"]), int)
        self.assertIs(type(objectResponse["picture"]["pictureData"]), str)
        self.assertIs(type(objectResponse["picture"]["word"]), str)
    def test_getPictureById_400_non_existent_id(self):
        response = self.client.get('/picture/99999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": "picture id does not exist",
            "status": "404"
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), str)
    def test_getPictureById_400_non_valid_id(self):
        response = self.client.get('/picture/wefwe3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
            "msg": "picture id is not a number",
            "status": "404"
        })
        self.assertIs(type(objectResponse["msg"]), str)
        self.assertIs(type(objectResponse["status"]), str)
class postPicture(APITestCase):
    def test_postPicture_200_picuture1(self):
        response = self.client.post('/api/pictures/', data={'data': uriData.data1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        objectResponse = json.loads(response.content)
        print(objectResponse)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'outcome': 'web_site'})
        self.assertIs(type(objectResponse["outcome"]), str)
    def test_postPicture_200_picuture2(self):
        response = self.client.post('/api/pictures/', data={'data': uriData.data2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {'outcome': 'dumbbell'})
        self.assertIs(type(objectResponse["outcome"]), str)
    def test_postPicture_400(self):
        response = self.client.post('/api/pictures/', data={'data': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        objectResponse = json.loads(response.content)
        objectResponse = json.loads(response.content)
        self.assertIs(type(objectResponse), type({}))
        self.assertEqual(objectResponse, {
                         'err': 'Error occured. Please try again'})
