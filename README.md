# Pyramid Mongoengine

pyramid-mongoengine package based in [flask-mongoengine](https://github.com/MongoEngine/flask-mongoengine)

## *** README In Progress ***

## Install

    pip install pyramid-mongoengine

## Config

Basic setup
```python

if __name__ == "__main__":
    config = Configurator()

    config.include("pyramid_mongoengine")
    config.add_connection_database()

```

`pyramid-mongoengine` provides `add_connection_database()`, he makes a connection with database
using data coming from .ini file.

```python

mongo_url = mongodb://my_ip_location_to_mongodb
mongodb_name = "my_db_application"

```

If theses data not exists in .ini, `pyramid-mongoengine` use default values

```python
# Default values
mongo_url = mongodb://localhost
mongodb_name = "test"
```
