## Movie Search 

### How to run

This project is written in Django, so there are a few steps to get it up and running locally.  First, you'll need to make sure you have python 3 and pipenv installed.  Once that is done, clone the repo.  You'll need to rename the file "project/.env.sample" to "project/.env".

You'll also need an API key for The Movie Database.  If you have your own, feel free to use it.  If you don't, one should have been supplied for you.  That key will need to be added into the .env file as:

    MOVIE_API_KEY=<your API key>

After that, you'll need to run:

    pipenv install
    pipenv shell
    python manage.py migrate
    python manage.py runserver

You should have access to the app on 127.0.0.1:8000.

If you'd like to have a look around the admin side of the site (pretty barebones at this point), you can create a superuser with the command

    python manage.py createsuperuser

and have a look around at 127.0.0.1:8000/admin


### About

This is a code challenge I did for Relias Learning.  I've created a site where movies can be browsed and searched and actors can be searched.  Movies give information about their plot, release date, and main cast, and they can be favorited by users who are logged in to the site.  Pages are interconnected throughout, and there are checks for authenticated users at appropriate places.  

All movie information comes from The Movie Database, a free movie API.  Apply for a key here:  https://developers.themoviedb.org/3/getting-started/introduction

The DB used is SQLite just to ease setup on the receiving end.  

I've left Debug mode on in case any testers want to poke around in the Django Debug Toolbar panel on the right side.  Sometimes this starts in an open position on some browsers...not sure why.  Just an oddity.

Thanks, and enjoy.
Joey.
