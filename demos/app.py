from pyramid.config import Configurator
from pyramid.view import view_config
from wsgiref.simple_server import make_server

from pyramid_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    """Simple user model"""
    email = db.StringField()
    username = db.StringField()


@view_config(route_name="hello", renderer="json")
def hello(request):
    return {"msg": "Hello Pyramid MongoEngine"}


@view_config(route_name="add", request_method="POST", renderer="json")
def new_user(request):
    params = dict(request.params)
    user = User(**params)
    user.save()
    return {"new_user": user}


@view_config(route_name="show", renderer="json")
def show(request):
    username = request.matchdict["username"]
    user = User.objects.get_or_404(username=username)

    return {"user": user}


if __name__ == "__main__":
    config = Configurator()

    config.add_settings({"mongodb_name": "pyramid_mongoengine_test"})

    config.include("pyramid_mongoengine")
    config.add_connection_database()

    config.add_route("hello", "/")
    config.add_route("add", "/new/")
    config.add_route("show", "/{username}/")

    config.scan()

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
