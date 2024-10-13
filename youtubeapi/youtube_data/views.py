from django.conf import settings
from googleapiclient.discovery import build
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.shortcuts import redirect
from django.urls import reverse

# youtube_data/views.py

import os

# Permet d'utiliser HTTP pour OAuth en local
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def oauth2_login(request):
    flow = Flow.from_client_secrets_file(
        'client_secret.json',  # Chemin vers le fichier JSON des identifiants
        scopes=['https://www.googleapis.com/auth/youtube.readonly'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    request.session['state'] = state  # Stocker l'état pour la vérification
    return redirect(authorization_url)




def oauth2_callback(request):
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.readonly'],
        state=request.session['state'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    # Sauvegarder les informations d'identification
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect(reverse('oauth2_callback'))  # Rediriger vers une vue après l'authentification

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }



def get_user_videos(request):
    if 'credentials' not in request.session:
        return redirect('oauth2_login')

    credentials = Credentials(**request.session['credentials'])
    youtube = build('youtube', 'v3', credentials=credentials)

    request = youtube.channels().list(
        part='contentDetails',
        mine=True
    )
    response = request.execute()

    # Traiter la réponse pour obtenir les vidéos
    return Response(response)


""" class YouTubeSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', 'Django Rest Framework')
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

        request_data = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=5
        ).execute()

        return Response(request_data) """

