from django.shortcuts import render
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import traceback

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@cache_page(100)
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    if request.method == 'GET':
        return Response(UserSerializer(user).data)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=204)
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@csrf_exempt
@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@authentication_classes([])
def custom_token_obtain(request):
    if request.method == 'OPTIONS':
        return Response(status=200)

    try:
        raw_email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"DEBUG: --- Login Attempt Start ---")
        print(f"DEBUG: raw_email='{raw_email}', password_len={len(password) if password else 0}")
        print(f"DEBUG: Request content_type={request.content_type}")
        print(f"DEBUG: Request headers={dict(request.headers)}")
        
        if not raw_email or not password:
            print("DEBUG: Missing email or password")
            return Response({"detail": "Email and password are required"}, status=400)

        email = raw_email.lower().strip()
        print(f"DEBUG: Normalized email='{email}'")
        
        # Try multiple authentication patterns
        user = authenticate(username=email, password=password)
        if not user:
            print(f"DEBUG: authenticate(username={email}) failed")
            user = authenticate(email=email, password=password)
        if not user:
            print(f"DEBUG: authenticate(email={email}) failed")
            user = authenticate(username=raw_email.strip(), password=password)
        if not user:
            print(f"DEBUG: authenticate(username={raw_email.strip()}) failed")

        # FALLBACK: Direct DB check if authenticate fails but data exists
        if not user:
            print("DEBUG: authenticate() failed, trying direct DB check...")
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj:
                from django.contrib.auth.hashers import check_password
                if user_obj.check_password(password):
                    print(f"DEBUG: Direct DB check SUCCESS for {user_obj.email}")
                    user = user_obj
                else:
                    print(f"DEBUG: Direct DB check FAILED (Password mismatch) for {user_obj.email}")
            else:
                print(f"DEBUG: Direct DB check FAILED (User not found) for {email}")

        if user:
            if not user.is_active:
                print(f"DEBUG: Auth SUCCESS but user.is_active is False")
                return Response({"detail": "Account is inactive"}, status=401)
                
            print(f"DEBUG: Final Auth SUCCESS for {user.email}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            print(f"DEBUG: Final Auth FAILURE for {email}")
            return Response({"detail": "Invalid credentials. Please contact support."}, status=401)
    except Exception as e:
        tb = traceback.format_exc()
        print(f"!!! LOGIN VIEW ERROR: {str(e)}\n{tb}")
        return Response({
            "error": str(e),
            "traceback": tb,
            "message": "Internal Server Error in custom_token_obtain"
        }, status=500)