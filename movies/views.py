from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
#from .models import Album, Comment, Photo
#from .forms import AlbumForm, CommentForm, PhotoForm
from users.models import User
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from project.settings import MOVIE_API_KEY
import requests
import urllib

DB_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w300/"
temp = "rLOk4z9zL1tTukIYV56P94aZXKk.jpg"

class Home(View):

    def get(self, request):
        query = urllib.parse.quote("Lord of the Rings")
        r = requests.get(f'{DB_URL}/search/movie?query={query}&api_key={MOVIE_API_KEY}')
        list = []
        for item in r.json()["results"]:
            if item["poster_path"]:
                list.append({"title": item["original_title"], 
                            "overview": item["overview"], 
                            "year": item["release_date"], 
                            "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                            })
        return render(request, 'movies/home.html', {'movies': list})


class Search(View):
    def get(self, request):
        query = request.GET.get('query')
        if query is not None:
            query_string = urllib.parse.quote(query)
            r = requests.get(f'{DB_URL}/search/movie?query={query_string}&api_key={MOVIE_API_KEY}')
            list = []
            for item in r.json()["results"]:
                if item["poster_path"]:
                    list.append({"title": item["original_title"], 
                                "overview": item["overview"], 
                                "year": item["release_date"], 
                                "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                                })
        else:
            movies = None
        return render(request, 'movies/search.html', {'movies': list, "query": query or ""})

