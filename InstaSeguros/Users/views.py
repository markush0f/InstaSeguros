from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView

# User = get_user_model()


# https://www.django-rest-framework.org/api-guide/viewsets/
class UserView(APIView):
    def get_user_by_id_or_404(self, pk) -> User:
        """
        This method will return the user or a 404 response
        if the user does not exist
        """
        return get_object_or_404(User, pk=pk)

    def get_user_by_username(self, username) -> User | None:
        """
        This method will return the user by username
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def create_user_serializer(self, data) -> User:
        """
        This method will create a new instance of user serailizer and return it
        """
        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer

    def get(self, request, pk=None):
        if pk:
            user = self.get_user_by_id_or_404(pk)
            print(user)
            return Response(
                {"user": UserSerializer(user).data}, status=status.HTTP_200_OK
            )
        else:
            users = User.objects.all()
            return Response(
                {"users": UserSerializer(users, many=True).data},
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        data = request.data
        user_serializer = self.create_user_serializer(data)
        user_serializer.save()
        return Response({"user": user_serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = self.get_user_by_id_or_404(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        user = self.get_user_by_id_or_404(pk)
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"user": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"user": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
