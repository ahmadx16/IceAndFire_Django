# Ice and Fire API 

![alt text](https://img.icons8.com/officel/40/000000/winter.png) ![alt text](https://img.icons8.com/emoji/48/000000/fire.png)

This application is built on django-rest framework. It implements a REST API that calls an external API service to get information about books. Additionally, it implements a simple *CRUD* (Create, Read, Update, Delete) API with a local database.

The external API that is used here is the ​[Ice And Fire](https://anapioficeandfire.com/Documentation#books) API.

## Instructions

This application is configured to work with MySQL local server. Following are the instructions to configure MySQL server connection with the application. 

**Note**: If you want to quickly see application up and running you may skip MySQL Connection Setup, and move to the Sqlite Connection section. 

### MySQL Connection Setup

This application is configured to work with MySQL local server. In order to connect to MySQL Server to do following steps:

1.  Install the MySQL server if it is not locally installed on your machine. You can visit [MySQL installation guide](https://dev.MySQL.com/doc/MySQL-installation-excerpt/5.7/en/) for the details of installation of server.
2. Create a database on MySQL and add the database name, user, and password on file [my.cnf](IceAndFire/IceAndFire/my.cnf) file under client section

``` 
[client]
database = database_name
user = root
password = password
default-character-set = utf8
```

3. Finally, you will need to install a python interface to MySQL, which in our case is [mysqlclient 2.0.1](https://pypi.org/project/mysqlclient/). You can learn about how to install by vising the provided link.

### Sqlite Connection Setup (optional)

This step is **NOT** required if you have already setup the MySQL connection. It is a quick workaround if you do not want to go through the process of connecting with MySQL setup. In order to use sqlite as your primary database simply update file [settings.py](IceAndFire/IceAndFire/settings.py) and replace *DATABASES* dictionary from line 79-86 with following code.

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Python Environment Setup

It is recommended to create a virtual environment before installing django.

``` shell
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment
```

The above commands will create and activate a new virtual environment. Learn more about virtual environment venv [here](https://docs.python.org/3/library/venv.html).

Now install application requirements using following command.

``` shell
pip install -r requirements.txt
```

### Launching the application

Before launching the application run the following command on terminal

``` shell
cd IceAndFire
python manage.py migrate
```

This command will create the database tables that we have specifies in models of our application.

Now run command.

``` shell
python manage.py runserver 8080
```

This command will start the backend server at 127.0.0.1:8080
