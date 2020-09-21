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

    def get(self, request, page=1):
        r = requests.get(f'{DB_URL}/discover/movie?sort_by=popularity.desc&api_key={MOVIE_API_KEY}&page={page}')
        list = []
        results = r.json()

        num_pages = results["total_pages"]
        previous_page, next_page = None, None
        if page + 1 <= num_pages:
            next_page = page + 1    
        if page - 1 >= 1:
            previous_page = page - 1

        for item in results["results"]:
            if item["poster_path"]:
                list.append({"title": item["original_title"], 
                            "overview": item["overview"], 
                            "year": item["release_date"][:4],
                            "tmdb_id": item["id"], 
                            "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                            })
        return render(request, 'movies/home.html', {'movies': list, "next": next_page, "previous": previous_page})


class Search(View):
    def get(self, request):
        query = request.GET.get('query')
        if query is not None:
            query_string = urllib.parse.quote(query)
            r = requests.get(f'{DB_URL}/search/movie?query={query_string}&api_key={MOVIE_API_KEY}&sort_by=popularity.desc&is_adult=false')
            list = []
            for item in r.json()["results"]:
                if item["poster_path"]:
                    list.append({"title": item["original_title"], 
                                "overview": item["overview"], 
                                "year": item["release_date"][:4],
                                "tmdb_id": item["id"], 
                                "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                                })
        else:
            movies = None
        return render(request, 'movies/search.html', {'movies': list, "query": query or ""})

class MovieDetail(View):
    def get(self, request, id):
        movie_data = requests.get(f'{DB_URL}/movie/{id}?api_key={MOVIE_API_KEY}')
        movie = movie_data.json()
        if movie["poster_path"]:
            movie_info = {"title": movie["original_title"], 
                                    "overview": movie["overview"], 
                                    "year": movie["release_date"][:4],
                                    "tmdb_id": movie["id"], 
                                    "image": f"{IMAGE_URL}{movie['poster_path'][1:]}"
                                    }
        cast_data = requests.get(f"{DB_URL}/movie/{id}/credits?api_key={MOVIE_API_KEY}")
        cast = cast_data.json()["cast"]
        cast_info = []
        for member in cast[:5]:
            cast_info.append({"name": member["name"], "cast_id": member["id"]})
        return render(request, 'movies/movie-detail.html', {"movie": movie_info, "cast": cast_info})


class StarMovies(View):
    def get(self, request, name, id):
        star_movies_data = requests.get(f"{DB_URL}/discover/movie?with_cast={id}&sort_by=popularity.desc&api_key={MOVIE_API_KEY}")
        list = []
        for item in star_movies_data.json()["results"]:
            if item["poster_path"]:
                list.append({"title": item["original_title"], 
                            "overview": item["overview"], 
                            "year": item["release_date"][:4],
                            "tmdb_id": item["id"], 
                            "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                            })
        return render(request, 'movies/star-movies.html', {"name": name, "movies": list})