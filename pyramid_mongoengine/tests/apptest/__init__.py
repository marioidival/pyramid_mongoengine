from __future__ import unicode_literals

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    email = db.StringField()
    username = db.StringField(required=True)


@view_config(route_name="index", renderer="json")
def index(request):
    return {"msg": "hello test app"}


@view_config(route_name="users", renderer="json", request_method="GET")
def users(request):
    if request.params.get("first"):
        users = User.objects.first_or_404()
    else:
        users = User.objects.all()
    return {"users": users}


@view_config(route_name="users", renderer="json", request_method="POST")
def new_user(request):
    params = dict(request.params)
    user = User(**params)
    user.save()
    return {"user": user}


@view_config(route_name="user", renderer="json", match_param="action=get")
def user(request):
    username = request.matchdict["username"]
    user = User.objects.get_or_404(username=username)
    return {"user": user}


@view_config(route_name="user", renderer="json", match_param="action=delete")
def delete_user(request):
    username = request.matchdict["username"]
    user = User.objects.get_or_404(username=username)

    user.delete()
    return {"success": True}


def main(global_config, **settings):
    config = Configurator()

    # global_config comes from .ini or dict
    config.add_settings(global_config)

    config.add_route("index", "/")
    config.add_route("users", "/users/")
    config.add_route("user", "/user/{username}/{action}")

    config.include("pyramid_mongoengine")
    config.add_connection_database()

    config.scan()

    return config.make_wsgi_app()
