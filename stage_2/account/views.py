from .serializer import (
        UserSerializer,
        UserResponseSerializer,
        OrgSerializer,
        OrgResponseSerializer
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ParseError, NotFound
from rest_framework import status
from .models import User, Organisation
import jwt
import datetime
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
            else:
                errors = serializer.errors
                error_list = [{"field": field, "message": messages[0]} for field, messages in errors.items()]
                response_payload = {
                        "errors": error_list
                        }
                return Response(response_payload, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            response_serializer = UserResponseSerializer(user)
            payload = {
                    'id': str(user.userId),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                    }
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response_payload = {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                        "accessToken": token,
                        "user": response_serializer.data
                        }
                    }
            response = Response(response_payload, status=status.HTTP_201_CREATED)
            response.set_cookie(key='accessToken', value=token, httponly=True)
            return response
        except ParseError as e:
            response_payload = {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed('user not found!')

            if not user.check_password(password):
                raise AuthenticationFailed('incorrect password')

            payload = {
                    'id': user.userId,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                    }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response_serializer = UserResponseSerializer(user)
            response_payload = {
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "accessToken": token,
                        "user": response_serializer.data
                        }
                    }
            response = Response(response_payload, status=status.HTTP_200_OK)
            response.set_cookie(key='accessToken', value=token, httponly=True)
            return response
        except Exception as e:
            response_payload = {
                    "status": "Bad request",
                    "message": f"Authentication failed {str(e)}",
                    "statusCode": 401
                    }
            return Response(response_payload, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    def get(self, request, userId):
        try:
            token = request.COOKIES.get('accessToken')

            if not token:
                raise AuthenticationFailed("Unauthenticated request")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthorized access")
            if payload['id'] != userId:
                raise AuthenticationFailed("Restricted access")

            user = User.objects.filter(userId=payload['id']).first()
            response_serializer = UserResponseSerializer(user)
            response_payload = {
                    "status": "success",
                    "message": f"user {user.firstName} succesfully retrieved",
                    "data": response_serializer.data
                    }
            return Response(response_payload, status=status.HTTP_200_OK)
        except Exception as e:
            response_payload = {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

class OrgsView(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('accessToken')

            if not token:
                raise AuthenticationFailed("Unauthenticated request")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthorized access")

            user = User.objects.filter(userId=payload['id']).first()
            queryset = user.organisations.all()
            serializer = OrgResponseSerializer(queryset, many=True)
            response_payload = {
                    "status": "success",
                    "message": f"{user.firstName}'s Organisations",
                    "data": {
                        "organisations": serializer.data
                        }
                    }
            return Response(response_payload, status=status.HTTP_200_OK)
        except Exception as e:
            response_payload = {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            token = request.COOKIES.get('accessToken')

            if not token:
                raise AuthenticationFailed("Unauthenticated request")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthorized access")

            user = User.objects.filter(userId=payload['id']).first()
            serializer = OrgSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            org = serializer.save()
            org.users.add(user)
            org.save()
            
            response_serializer = OrgResponseSerializer(org)
            response_payload = {
                    "status": "success",
                    "message": "Organisation created successfully",
                    "data": response_serializer.data
                    }
            return Response(response_payload, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_payload = {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)


class OrgView(APIView):
    def get(self, request, orgId):
        try:
            token = request.COOKIES.get('accessToken')

            if not token:
                raise AuthenticationFailed("Unauthenticated request")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthorized access")
            user = User.objects.filter(userId=payload['id']).first()
            org = Organisation.objects.filter(orgId=orgId).first()
            if org is None:
                raise NotFound('Organisation does not exist')
            if user not in org.users.all():
                raise AuthenticationFailed("user does not belong to organisation")
            response_serializer = OrgResponseSerializer(org)
            response_payload = {
                    "status": "success",
                    "message": "Organisation found successfully",
                    "data": response_serializer.data
                    }
            return Response(response_payload, status=status.HTTP_200_OK)
        except Exception as e:
            response_payload = {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, orgId):
        try:
            token = request.COOKIES.get('accessToken')

            if not token:
                raise AuthenticationFailed("Unauthenticated request")

            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthorized access")
            user = User.objects.filter(userId=payload['id']).first()
            org = Organisation.objects.filter(orgId=orgId).first()
            if org is None:
                raise NotFound('Organisation does not exist')
            if user not in org.users.all():
                raise AuthenticationFailed("user does not belong to organisation")
            userId = request.data.get("userId")
            if not userId:
                raise ValueError("userId is required")
            user = User.objects.filter(userId=userId).first()
            if not user:
                raise NotFound("user does not exist")
            org.users.add(user)
            org.save()
            response_payload = {
                    "status": "success",
                    "message": "User added to organisation successfully",
                    }
            return Response(response_payload, status=status.HTTP_200_OK)
        except Exception as e:
            response_payload = {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                    }
            return Response(response_payload, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('accessToken')
        response.data = {
                "message": "logout successful"
                }
        return response

