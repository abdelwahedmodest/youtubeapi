from django.conf import settings
from googleapiclient.discovery import build
from rest_framework.response import Response
from rest_framework.views import APIView

class YouTubeSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', 'Django Rest Framework')
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

        request_data = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=5
        ).execute()

        return Response(request_data)

