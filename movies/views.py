from django.shortcuts import render
from .models import Movie
from users.models import User
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from project.settings import MOVIE_API_KEY
import requests
import urllib

DB_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w300/"
API_KEY = f"api_key={MOVIE_API_KEY}"
POP_SORT = "sort_by=popularity.desc"


def get_page_bounds(page, num_pages):
    previous_page, next_page = None, None
    if page + 1 <= num_pages:
        next_page = page + 1    
    if page - 1 >= 1:
        previous_page = page - 1
    return previous_page, next_page


class Home(View):
    def get(self, request, page=1):
        r = requests.get(f'{DB_URL}/discover/movie?{POP_SORT}&page={page}&{API_KEY}')
        results = r.json()
        num_pages = results["total_pages"]
        previous_page, next_page = get_page_bounds(page, num_pages)
        list = []
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
    def get(self, request, page=1, query=None):
        if query is None:
            query = request.GET.get('query')
        if query is not None:
            query_string = urllib.parse.quote(query)
            r = requests.get(f'{DB_URL}/search/movie?query={query_string}&{POP_SORT}&page={page}&{API_KEY}')
            results = r.json()
            num_pages = results["total_pages"]
            previous_page, next_page = get_page_bounds(page, num_pages)
            list = []
            for item in results["results"]:
                if item["poster_path"]:
                    list.append({"title": item["original_title"], 
                                "overview": item["overview"], 
                                "year": item["release_date"][:4],
                                "tmdb_id": item["id"], 
                                "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                                })
        else:
            movies, next_page, previous_page = None, None, None
        return render(request, 'movies/search.html', 
                    {'movies': list, "query": query or "", "next": next_page, "previous": previous_page})


class SearchActor(View):
    def get(self, request):
        query = request.GET.get('query')
        if query is not None:
            query_string = urllib.parse.quote(query)
            r = requests.get(f'{DB_URL}/search/person?query={query_string}&{POP_SORT}&{API_KEY}')
            results = r.json()
            list = []
            for item in results["results"][:15]:
                if item["profile_path"]:
                    list.append({"name": item["name"],
                                    "tmdb_id": item["id"],
                                    "image": f"{IMAGE_URL}{item['profile_path'][1:]}",
                                })
        return render(request, 'movies/search-actor.html', {"actors": list, "query": query})



class MovieDetail(View):
    def get(self, request, id):
        movie_data = requests.get(f'{DB_URL}/movie/{id}?{API_KEY}')
        movie = movie_data.json()
        if movie["poster_path"]:
            movie_info = {"title": movie["original_title"], 
                                    "overview": movie["overview"], 
                                    "year": movie["release_date"][:4],
                                    "tmdb_id": movie["id"], 
                                    "image": f"{IMAGE_URL}{movie['poster_path'][1:]}"
                                    }
        cast_data = requests.get(f"{DB_URL}/movie/{id}/credits?{API_KEY}")
        cast = cast_data.json()["cast"]
        cast_info = []
        for member in cast[:5]:
            cast_info.append({"name": member["name"], "cast_id": member["id"]})
        if request.user.is_authenticated:
            is_favorite = request.user.favorites.filter(tmdb_id=id).count() == 1
        else:
            is_favorite = False
        return render(request, 'movies/movie-detail.html', {"movie": movie_info, "cast": cast_info, "is_favorite": is_favorite})


class ActorDetail(View):
    def get(self, request, id):
        actor_data = requests.get(f'{DB_URL}/person/{id}?{API_KEY}')
        actor = actor_data.json()
        actor_info = {"name" : actor["name"],
                        "biography" : actor["biography"],
                        "image" : f"{IMAGE_URL}{actor['profile_path'][1:]}",
                        "tmdb_id": actor["id"],
                    }
        return render(request, 'movies/actor-bio.html', {"actor": actor_info})


class StarMovies(View):
    def get(self, request, name, id, page=1):
        r = requests.get(f"{DB_URL}/discover/movie?with_cast={id}&{POP_SORT}&page={page}&{API_KEY}")
        results = r.json()
        num_pages = results["total_pages"]
        previous_page, next_page = get_page_bounds(page, num_pages)
        list = []
        for item in results["results"]:
            if item["poster_path"]:
                list.append({"title": item["original_title"], 
                            "overview": item["overview"], 
                            "year": item["release_date"][:4],
                            "tmdb_id": item["id"], 
                            "image": f"{IMAGE_URL}{item['poster_path'][1:]}"
                            })
        return render(request, 'movies/star-movies.html', {"name": name, "movies": list, "star_id": id, "next": next_page, "previous": previous_page})


class ShowFavorites(View):
    def get(self, request):
        movies = request.user.favorites.all()
        return render(request, 'movies/favorites.html', {"movies": movies})


@method_decorator(login_required, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class ToggleFavoriteMovie(View):
    def post(self, request, tmdb_id):
        movie = Movie.objects.all().filter(tmdb_id=tmdb_id)
        if movie.count() == 0:
            movie_data = requests.get(f'{DB_URL}/movie/{tmdb_id}?{API_KEY}')
            movie = movie_data.json()
            if movie["poster_path"]:
                movie = Movie(title=movie["original_title"],
                                    year=movie["release_date"][:4],
                                    description=movie["overview"],
                                    tmdb_id=tmdb_id,
                                    image=f"{IMAGE_URL}{movie['poster_path'][1:]}"
                                    )
                movie.save()
        else: 
            movie = movie.first()
        user = request.user
        if movie in user.favorites.all():
            user.favorites.remove(movie)
            return JsonResponse({"favorite": False})
        else:
            user.favorites.add(movie)
            return JsonResponse({"favorite": True})