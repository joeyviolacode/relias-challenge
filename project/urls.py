from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from movies import views as movie_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("registration.backends.simple.urls")),
    path('', movie_views.Home.as_view(), name="home"),
    path('page/<int:page>', movie_views.Home.as_view(), name="home"),
    path('search', movie_views.Search.as_view(), name="search"),
    path('search/<str:query>/page/<int:page>', movie_views.Search.as_view(), name="search"),
    path('search/actor', movie_views.SearchActor.as_view(), name="search-actor"),
    path('movie/<int:id>', movie_views.MovieDetail.as_view(), name="movie-detail"),
    path('star/<str:name>/<int:id>', movie_views.StarMovies.as_view(), name="star-movies"),
    path('star/<str:name>/<int:id>/page/<int:page>', movie_views.StarMovies.as_view(), name="star-movies"),
    path('movie/<int:tmdb_id>/fave', movie_views.ToggleFavoriteMovie.as_view(), name="toggle-favorite"),
    path('favorites', movie_views.ShowFavorites.as_view(), name="favorites"),
    path('star/<int:id>', movie_views.ActorDetail.as_view(), name="actor-detail"),
    path('about', movie_views.About.as_view(), name="about"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
