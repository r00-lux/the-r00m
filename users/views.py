from rest_framework import generics, authentication, permissions

from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Update an authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive the authenticated user."""
        return self.request.user


# class CreateTokenView(ObtainAuthToken):
#     """Create a new auth token for a user."""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
