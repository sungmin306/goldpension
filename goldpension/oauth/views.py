import requests
import jwt
import time
import json


from django.conf import settings
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from user.models import UserModel
from user.views import LoginView, UserView
from user.serializers import CreateUserSerializer
from django.http import JsonResponse

class UserView2():
    permission_classes = [AllowAny]

    def get_or_create_user(self, data: dict):
        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        serializer.create(validated_data=user)

        return Response(data=user, status=status.HTTP_201_CREATED)


def login_api(social_type: str, social_id: str, email: str=None, phone: str=None):
    '''
    회원가입 및 로그인
    '''
    login_view = LoginView()
    try:
        print("try문에 들어감")
        UserModel.objects.get(social_id=social_id)
        data = {
            'social_id': social_id,
            'email': email,
        }
        response = login_view.object(data=data)

    except UserModel.DoesNotExist:
        data = {
            'social_type': social_type,
            'social_id': social_id,
            'email': email,
        }
        user_view = UserView2() # 객체생성
        print("user_view",user_view)
        login = user_view.get_or_create_user(data=data)

        response = login_view.object(data=data) if login.status_code == 201 else login
        print(response)

    return response


kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        kakao code 요청
        '''
        client_id = settings.KAKAO_REST_API_KEY
        print(client_id)
        redirect_uri = settings.KAKAO_REDIRECT_URI
        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        return res


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]
    print("kakaocallback에 들어옴")

    @swagger_auto_schema(query_serializer=CallbackUserCSRFInfoSerializer)
    def get(self, request):
        '''
        kakao access_token 및 user_info 요청
        '''
        data = request.query_params
        print(data)
        print("get 들어옴")
        print(request)
        # access_token 발급 요청
        code = data.get('code')
        print("code는",code)
        # code2 = code[6:]
        # print("##########")
        # print("code2는",code2)
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print("조건문 넘어감")
        request_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': settings.KAKAO_REDIRECT_URI,
            'client_secret': settings.KAKAO_CLIENT_SECRET_KEY,
            # 'client_id': "edf8f58de6f9fb90e53e2dd72452c71f",
            # 'redirect_uri': "http://localhost:3000/accounts/kakao/callback/",
            # 'client_secret': "NTPCyiFtCARiGAU58nf2HBaybwy329xZ", 
            'code': code,
        }
        print("request_data 는 ",request_data)
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers) # 여기서 프론트한테 간다.
        print("*****")
        print(token_res.text)
        #time.sleep(3)
        print("token_res는 ", token_res)
        token_json = token_res.json()
        access_token = token_json.get('access_token')
        print("accsess token 은", access_token)

        if not access_token:
            print("access token 없어서 조건문 들어옴")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"  # 'Bearer ' 마지막 띄어쓰기 필수
        #print("ffffffff",access_token)

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_email = kakao_account.get('email')
        print(kakao_account)
        print(kakao_account.get('profile').get('nickname'))
        user_name = kakao_account.get('profile').get('nickname')
        print("get으로 들어와서 성공해서 출렧한 이메일입니다.",end='')
        print(user_email)
        global dic
        dic = {}
        dic['name'] = user_name
        dic['email'] = user_email
        print(dic)
        return JsonResponse(dic)

naver_login_url = "https://nid.naver.com/oauth2.0/authorize"
naver_token_url = "https://nid.naver.com/oauth2.0/token"
naver_profile_url = "https://openapi.naver.com/v1/nid/me"

class NaverLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        naver code 요청

        ---
        '''
        client_id = settings.NAVER_CLIENT_ID
        redirect_uri = settings.NAVER_REDIRECT_URI
        state = settings.STATE
        # state = get_token(request)

        uri = f"{naver_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code"
        res = redirect(uri)
        return res


class NaverCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserCSRFInfoSerializer)
    def get(self, request):
        '''
        naver access_token 및 user_info 요청

        ---
        '''
        data = request.query_params
        print("get 들어옴")
        # access_token 발급 요청
        code = data.get('code')
        user_state = data.get('state')
        if (not code) or (user_state != settings.STATE):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_CLIENT_SECRET,
            'code': code,
            'state': user_state,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(naver_token_url, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}"  # 'Bearer ' 마지막 띄어쓰기 필수

        # naver 회원정보 요청
        auth_headers = {
            "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(naver_profile_url, headers=auth_headers)
        user_info_json = user_info_res.json()
        user_info = user_info_json.get('response')
        if not user_info:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        social_type = 'naver'
        social_id = f"{social_type}_{user_info.get('id')}"
        user_email = user_info.get('email')

        # 회원가입 및 로그인
        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res
    


google_login_url = "https://accounts.google.com/o/oauth2/v2/auth"
google_scope = "https://www.googleapis.com/auth/userinfo.email"
google_token_url = "https://oauth2.googleapis.com/token"
google_profile_url = "https://www.googleapis.com/oauth2/v2/tokeninfo"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        google code 요청

        ---
        '''
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        uri = f"{google_login_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={google_scope}&response_type=code"

        res = redirect(uri)
        return res


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(query_serializer=CallbackUserInfoSerializer)
    def get(self, request):
        '''
        google access_token 및 user_info 요청

        ---
        '''
        data = request.query_params

        # access_token 발급 요청
        code = data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        }
        token_res = requests.post(google_token_url, data=request_data)

        token_json = token_res.json()
        access_token = token_json['access_token']

        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # google 회원정보 요청
        query_string = {
            'access_token': access_token
        }
        user_info_res = requests.get(google_profile_url, params=query_string)
        user_info_json = user_info_res.json()
        if (user_info_res.status_code != 200) or (not user_info_json):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        social_type = 'google'
        social_id = f"{social_type}_{user_info_json.get('user_id')}"
        user_email = user_info_json.get('email')

        # 회원가입 및 로그인
        res = login_api(social_type=social_type, social_id=social_id, email=user_email)
        return res


facebook_graph_url = "https://graph.facebook.com/v12.0"
facebook_login_url = "https://www.facebook.com/v12.0/dialog/oauth"
facebook_token_url = f"{facebook_graph_url}/oauth/access_token"  
facebook_debug_token_url = "https://graph.facebook.com/debug_token"
facebook_profile_url = f"{facebook_graph_url}/me"  # 사용자 정보 요청
