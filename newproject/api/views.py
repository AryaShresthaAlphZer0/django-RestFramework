from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializer import UserSerializer


@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_40_BAD_REQUEST)


@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.password == password:

        # Remember logged-in user
        request.session['user_id'] = user.id

        return Response({
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Invalid email or password'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
def Logout(request):

    request.session.flush()

    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def CurrentUser(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return Response(
            {'error': 'Not logged in'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'address': user.address,
        'email': user.email
    })