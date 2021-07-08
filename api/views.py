from django.shortcuts import render,redirect
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Persona as PersonaModel
from .serializers import PersonaSerializer
from rest_framework.authtoken.views import ObtainAuthToken
#metodos varios elementos
class PersonaList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)
    def post(self, request, *args, **kwargs):
        data = {
            'nombre': request.data.get('nombre'), 
            'apellido': request.data.get('apellido'),
        }
        serializer = PersonaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        query=PersonaModel.objects.all()
        serializer=PersonaSerializer(query,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#metodos por un solo elemento
class Persona(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)
    def get_object(self, todo_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        return PersonaModel.objects.get(id=todo_id)
    #acceder a un elemento
    def get(self, request, pk):
        todo_instance=self.get_object(pk)
        if not todo_instance:
            return Response(
                {"res": "no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PersonaSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #actualizar un elemento
    def put(self,request,pk, *args, **kwargs):
        todo_instance = self.get_object(pk)
        data = {
            'nombre': request.data.get('nombre'), 
            'apellido': request.data.get('apellido'),
        }
        serializer = PersonaSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #eliminar un elemento
    def delete(self, request, pk, *args, **kwargs):
        todo_instance = self.get_object(pk)
        if not todo_instance:
            return Response(
                {"res": "el objeto no existe :o"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Se eliminó!"},
            status=status.HTTP_200_OK
        )

class Login(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if(login_serializer.is_valid()):
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                #user_serializer = UserTokenSerializer(user)
                if(created):
                    return Response({
                            'token': token.key,
                            'message': 'Inicio de Sesión Exitoso.'
                        }, status = status.HTTP_201_CREATED)
            else:
                return Response({'message':'no pudo ingresar :c'},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error':'algun error: :C'},status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message':'cerraste tu sesión con exito :D'},status = status.HTTP_200_OK)
