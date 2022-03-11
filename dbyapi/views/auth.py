from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dbyapi.models import DiyUser

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
  """Handles the authentication of a diy user
  Method arguments:
  Request -- The full HTTP request object"""

  email = request.data['email']
  password = request.data['password']

  # use the built-in authenticate method to verify
  # authenticate returns the user object or None if no user is found
  authenticated_user = authenticate(email=email, password=password)

  # if authentication was successful, respond with their token
  if authenticated_user is not None:
    token = Token.objects.get(user=authenticated_user)
    data = {
      'valid': True,
      'token': token.key,
    }
    return Response(data)
  else:
    # bad login details were provided. so we can't log the user in.
    data = {'valid': False}
    return Response(data)


def register_user(request):
  """Handles the creation of a new user for authentication
  Method arguments: Request -- The full HTTP request object"""

  # create a new user by invoking the 'create_user' helper method
  # on Django's built-in User model
  new_user = User.objects.create_user(
    email=request.data['email'],
    password=request.data['password'],
    firstname=request.data['firstname'],
    lastname=request.data['lastname']
  )

  # now save the extra info in the dbyapi_diyuser table
  diyuser = DiyUser.objects.create(
    bio=request.data['bio'],
    user=new_user
  )

  # use the REST framework's token genderator on the new user account
  token = Token.objects.create(user=diyuser.user)
  # return the token to the clint
  data = {
    'valid': True,
    'token': token.key,
    'diyuser_pk': diyuser.id
  }
  return Response(data)