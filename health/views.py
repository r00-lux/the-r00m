from rest_framework.views import APIView
from rest_framework.response import Response


class HealthView(APIView):
    """Health API endpoint."""
    def get(self, request, format=None):
        """Return if service is up."""
        return Response()
