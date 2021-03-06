from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse
import os
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from pypika import Query, Table
from keras.applications.xception import Xception
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.xception import preprocess_input, decode_predictions
import numpy as np
from io import BytesIO
import base64
from PIL import Image
import re, json
import subprocess

DATABASE_URL = os.environ['DATABASE_URL']

badMethodJson = JsonResponse({'msg': "Requested method on URL is unavailable.", 'status':405},status=405)

@csrf_exempt
def selectUserByUsername(request,username):
    connection = psycopg2.connect(DATABASE_URL,sslmode='require')
    try:
        cursor = connection.cursor()
        users = Table('ufbe_users')
        selectUser = Query.from_(users).select('avatarUrl', 'language', 'score', 'img_id').where(users.username == username)
        cursor.execute(str(selectUser))
        userData = cursor.fetchone()
        if not userData:
            error = {'msg': 'User does not exist', 'status':404 }
            return JsonResponse(error, status=404)
        else:
            if request.method == "POST":
                return JsonResponse({'user': {'avatarUrl': userData[0],
                                              'language' : userData[1],
                                              'score' : userData[2],
                                              'img_id': userData[3]}}, status=201)
            else:
                return JsonResponse({'user': {'avatarUrl': userData[0],
                                              'language' : userData[1],
                                              'score' : userData[2],
                                              'img_id': userData[3]}})
    except (Exception, psycopg2.Error) as error:
        if hasattr(error,'pgerror'):
            errorLines = re.findall(r"[^\n]+\n",error.pgerror)
            return JsonResponse({'error': {'code':error.pgcode,
                                           'msg':errorLines[0][:-1]}})
        else:
            return JsonResponse({'error': 'some error'})
    
    finally:
        if(connection):
            cursor.close()
            connection.close()

@csrf_exempt
def patchUserByUsername(request, username):
    if not request.body:
        return JsonResponse({'msg':'No valid patch data in request', 'status':400},status=400)
    requestData = json.loads(request.body)
    connection = psycopg2.connect(DATABASE_URL,sslmode='require')
    try:
        cursor = connection.cursor()
        users = Table('ufbe_users')
        textColumnsToChange = []
        intColumnsToChange = []
        textColumnsToChange.append('avatarUrl') if 'avatarUrl' in requestData else ''
        textColumnsToChange.append('language') if 'language' in requestData else ''
        intColumnsToChange.append('score') if 'score' in requestData else ''
        intColumnsToChange.append('img_id')if 'img_id' in requestData else ''

        if not len(intColumnsToChange) == 0 and not len(textColumnsToChange) == 0:
            return JsonResponse({'msg':'Can only patch (avatarUrl and language) or (img_id and score) at the same time.', 'status':400},status=400)

        try:
            if len(textColumnsToChange) == 2:
                patchUser = Query.update(users).set(textColumnsToChange[0], requestData[textColumnsToChange[0]]).set(textColumnsToChange[1], requestData[textColumnsToChange[1]]).where(users.username == username)
                patchUser = str(patchUser)
                cursor.execute(patchUser)
            elif len(textColumnsToChange) == 1:
                patchUser = Query.update(users).set(textColumnsToChange[0], requestData[textColumnsToChange[0]]).where(users.username == username)
                patchUser = str(patchUser)
                cursor.execute(patchUser)

            elif len(intColumnsToChange) == 2:
                patchUser = """UPDATE ufbe_users SET score = score + %s, img_id = img_id + %s WHERE ufbe_users.username=%s;""",(requestData['score'],requestData['img_id'],username)
                cursor.execute(*patchUser)
            elif len(intColumnsToChange) == 1:
                patchUser = """UPDATE ufbe_users SET {0} = {1} + %s WHERE ufbe_users.username=%s;""".format(intColumnsToChange[0],intColumnsToChange[0]),(requestData[intColumnsToChange[0]],username)
                cursor.execute(*patchUser)                
      
        except Exception as error:
            cursor.execute('ROLLBACK;')
            print('**************************', error)
            return JsonResponse({'msg':'Error patching data'},status=500)
        else:
            cursor.execute('COMMIT;')
            return selectUserByUsername(request,username)
    
    except(Exception, psycopg2.Error) as error:
        print(error, '<<<<<<<<<<<<<<<<<<<<<<<')
        return JsonResponse({'msg':'error has occured'}, status=500)
  
    finally:
        if(connection):
            cursor.close()
            connection.close()
            
@csrf_exempt
def userByUsername(request, username):
    if (request.method == "GET"):
        return selectUserByUsername(request,username)
    if (request.method == "PATCH"):
        return patchUserByUsername(request,username)
    else:
        return badMethodJson
@csrf_exempt
def getPictureById(request, pictureById):
    connection = psycopg2.connect(DATABASE_URL,sslmode='require')
    if not request.method == 'GET':
        return badMethodJson
    try:
        cursor = connection.cursor()
        if pictureById.isnumeric():
            cursor = connection.cursor()
            pictures = Table('ufbe_pictures')
            selectPicture = Query.from_(pictures).select('*').where(pictures.pictureId == pictureById)
            cursor.execute(str(selectPicture))
            pictureData = cursor.fetchone()
            if not pictureData:
                error = {'msg': 'picture id does not exist', 'status': '404'}
                return JsonResponse(error, status=404)
            else:
                return JsonResponse({'picture': {'pictureId': pictureData[0], 'pictureData': pictureData[1], 'word': pictureData[2]}}, status=200)
        else:
            error = {'msg': 'picture id is not a number', 'status': '400'}
            return JsonResponse(error, status=400)
    except Exception as err:
        return JsonResponse({'error': err})
    finally:
        if(connection):
            cursor.close()
            connection.close()
@csrf_exempt
def postPicture(request):
    if not (request.method == 'POST'):
        return badMethodJson
    try:
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'msg':'No post data in request', 'status':400},status=400)
        
        img2 = Image.open(BytesIO(base64.b64decode(data['data'])))
        print('image opened')
        if not 'fast' in data:
            img2 = img2.resize((299,299))
            print('resized')
            model = Xception(weights='imagenet')
            print('Xception run successfully')
        else:
            img2 = img2.resize((224,224))
            print('resized')
            model = MobileNetV2(weights='imagenet')
            print('MobileNet run successfully')
            
        x = image.img_to_array(img2)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        outcome = decode_predictions(preds, top=1)[0][0]
        if outcome[2] < 0.35:
            outcome = "nothing recognised"
        else:
            outcome = outcome[1]
        return JsonResponse({'outcome': str(outcome)})
    except Exception as err:
        print(err)
        return JsonResponse({'err': 'Error occured. Please try again'}, status='400')
    finally:
        subprocess.run('heroku restart --app ufluent', shell=True)
@csrf_exempt
def postByUsername(request):
    if request.method == 'POST':
        try:
            jsonRequestData = json.loads(request.body)
        except:
            return JsonResponse({'msg':'No post data in request', 'status':400},status=400)
        
        connection = psycopg2.connect(DATABASE_URL,sslmode='require')
        if not 'language' in jsonRequestData:
            return JsonResponse({'msg':'Missing language from request', 'status':400}, status=400)
        elif not 'username' in jsonRequestData:
            return JsonResponse({'msg':'Missing username from request', 'status':400}, status=400)
        try:
            cursor = connection.cursor()
            users = Table('ufbe_users')
            postUser = Query.into(users).columns('username', 'language').insert(jsonRequestData['username'], jsonRequestData['language'])
            try:
                cursor.execute(str(postUser))
            except(Exception, psycopg2.IntegrityError)as error:
                cursor.execute("ROLLBACK;")
                if error.pgcode == '23505':
                    return JsonResponse({'msg':'User already exists', 'status':400}, status=400)
            else:
                cursor.execute("COMMIT;")
                return selectUserByUsername(request,jsonRequestData['username'])
        except (Exception, psycopg2.Error) as error:
            print('Error occured ---->', error)
            if hasattr(error,'pgerror'):
                errorLines = re.findall(r"[^\n]+\n",error.pgerror)
                return JsonResponse({'error': {'code':error.pgcode,
                                               'msg':errorLines[0][:-1]}}, status=400)
            else:
                return JsonResponse({'error': 'some error'},status=400)
        finally:
            if(connection):
                cursor.close()
                connection.close()
    else:
        return badMethodJson
@csrf_exempt
def sendEndpoints(request):
    if not request.method == 'GET':
        return badMethodJson
    return JsonResponse({'endpoints': {
        'GET: /api/users/:username': {
            'description': 'returns the specified user info',
            'exampleResponse': {
                'user': {
                    'avatarUrl':'example url',
                    'language': 'en',
                    'score':0,
                    'img_id':1
                }
            }
        },
        'GET: /api/pictures/:pictureID': {
            'description': 'returns the specified picture info',
            'exampleResponse': {
                'picture': {
                    'pictureID': 1,
                    'pictureData': 'example url',
                    'word': 'example image word'
                }
            }
        },
        'PATCH: /api/users/:username': {
            'description': 'changes the specified users info, returns new user object',
            'requestLimits': 'patch request can not handle mixing data keys from the 2 example requests given',
            'exampleRequest1': {"avatarUrl":"http://exam2.com/image2.png", "language":'fr'},
            'exampleRequest2': {"score":5, "img_id":2},
            'exampleResponse': {
                'user': {
                    'avatarUrl':'new example url',
                    'language': 'fr',
                    'score':5,
                    'img_id':3
                }
            }
        },
    }})