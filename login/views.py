from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
# Create your views here.

def user_login(request):

    request.params=json.loads(request.body)
    username = request.params['username']
    password = request.params['password']

    if username is None or password is None:
        return JsonResponse({"meta":{'status': 400, 'msg': 'Wrong request parameters'}})

    is_login = authenticate(request, username=username, password=password)
    if is_login is None:
        return JsonResponse({"meta":{'status': 404, 'msg': 'Username or password is wrong'}})

    login(request, is_login)

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(is_login)
    token = jwt_encode_handler(payload)

    return JsonResponse({
            'data': {'token': "JWT "+token},
            "meta":{'status': 200,
            'msg': 'Login successfully'}
        })
