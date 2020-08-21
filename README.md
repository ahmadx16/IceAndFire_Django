# Ice and Fire API ![alt text](https://img.icons8.com/officel/40/000000/winter.png) ![alt text](https://img.icons8.com/emoji/48/000000/fire.png)

This application is built on django-rest framework. It implements a REST API that calls an external API service to get information about books. Additionally, it implements a simple *CRUD* (Create, Read, Update, Delete) API with a local database.

The external API that is used here is the ​[Ice And Fire](https://anapioficeandfire.com/Documentation#books) API.

## Instructions

It is recommended to create a virtual environment before installing django.
```shell
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment
```
The above commands will create a new virtual environment and activate it. Learn more about virtual environment venv [here](https://docs.python.org/3/library/venv.html).

Now install application requirements using following command.

```shell
pip install -r requirements.txt
```

