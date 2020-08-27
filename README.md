![alt text](https://img.icons8.com/officel/40/000000/winter.png) ![alt text](https://img.icons8.com/emoji/48/000000/fire.png)

# Ice and Fire API 

This application is built on django-rest framework. It implements a REST API that calls an external API service to get information about books. Additionally, it implements a simple *CRUD* (Create, Read, Update, Delete) API with a local database.

The external API that is used here is the ​[Ice And Fire](https://anapioficeandfire.com/Documentation#books) API.

## Instructions

Following are the instructions that you need perform in order to run the application

1. [Python Environment Setup](#python-environment-setup)
1. [Database Setup](#database-setup)
1. [Launching the Application](#launching-the-application)
1. [Calling the APIs](#calling-the-apis)
1. [Executing API TestCases](#executing-api-testcases)

 

## Python Environment Setup

It is recommended to create a virtual environment before installing django. You can create a python virtual environment by giving path where you want to create a virtual environment and run following commands.

``` shell
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```

The above commands will create and activate a new virtual environment. Learn more about virtual environment venv [here](https://docs.python.org/3/library/venv.html).

Now install application requirements using following command.

``` shell
pip install -r requirements.txt
```

## Database Setup

You can configure any of the following databases.

1. [MySQL Connection Setup](#mysql-connection-setup)
1. [Sqlite Connection Setup (optional)](#sqlite-connection-setup-optional)

**Note**: If you want to quickly see application up and running you may skip MySQL Connection Setup, and move to the [Sqlite Connection section](#sqlite-connection-setup-optional).

### MySQL Connection Setup

This application is configured to work with MySQL local server. In order to connect to MySQL Server to do following steps:

1.  Install the MySQL server if it is not locally installed on your machine. You can visit [MySQL installation guide](https://dev.MySQL.com/doc/MySQL-installation-excerpt/5.7/en/) for the details of installation of server.
2. Create a database on MySQL and add the database name, user, and password on file [settings.py](IceAndFire/IceAndFire/settings.py) (from line 79-88) in the *DATABASE* dictionary . 

``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
You can learn about how to create MySQL database [here](https://dev.mysql.com/doc/refman/8.0/en/creating-database.html)

3. Finally, you will need to install a python interface to MySQL in your virtual environment, which in our case is [mysqlclient 2.0.1](https://pypi.org/project/mysqlclient/). You can learn about how to install by vising the provided link.

### Sqlite Connection Setup (optional)

This step is **NOT** required if you have already setup the MySQL connection. It is a quick workaround if you do not want to go through the process of connecting with MySQL setup. In order to use sqlite as your primary database simply update file [settings.py](IceAndFire/IceAndFire/settings.py) and replace *DATABASES* dictionary from line 79-88 with following code.

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Launching the Application

Before launching the application run the following command on terminal.

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

## Calling the APIs

Following are the APIs that user can call when the server is started.

### Get External Books:

This API calls an [external API](https://anapioficeandfire.com/Documentation#books) and returns a filtered book information. 

``` 
GET /api/external-books?name=:nameOfABook
```

**Parameter:** 

| Name         | DataType     | Required/Optional | Description               |
|--------------|--------------|-------------------|---------------------------|
| name         | string       | required          | Name of the book          |

<br>

**Example:**

Lets call following API to provide an example

``` shell
GET http://localhost:8080/api/external-books?name=A Game of Thrones
```

It will return response with `status_code=200` and following JSON data 

``` JSON
[
    {
        "name": "A Game of Thrones",
        "isbn": "978-0553103540",
        "authors": [
            "George R. R. Martin"
        ],
        "publisher": "Bantam Books",
        "country": "United States",
        "number_of_pages": 694,
        "release_date": "1996-08-01"
    }
]
```

</br>

### CRUD APIs on Local Database:

Following are the APIs that interacts with the local database.

#### **Create Book API**:

Adds a new book to the database.

``` 
POST /api/v1/books
```

The request needs to have JSON data in following format:

``` JSON
{
    "name": "Book Name",
    "isbn": "isbn number",
    "authors": ["author1", "author2"],
    "country": "United States",
    "number_of_pages": 694,
    "publisher": "Publisher name",
    "release_date": "1999-02-02"
}
```

**Example:**

Lets call following API to provide an example.

``` shell
POST http://localhost:8080/api/v1/books
```

with following data.

``` JSON
{
    "name": "Good Book",
    "isbn": "978-0553108033",
    "authors": ["Martin", "ToocoMan"],
    "country": "United States",
    "number_of_pages": 694,
    "publisher": "Bantam Books",
    "release_date": "1999-02-02"
}
```

It will return response with following JSON data 

``` JSON
{
    "status_code": 201,
    "status": "success",
    "data": [
        {
            "book": {
                "name": "Good Book",
                "isbn": "978-0553108033",
                "authors": [
                    "Martin",
                    "ToocoMan"
                ],
                "number_of_pages": 694,
                "publisher": "Bantam Books",
                "country": "United States",
                "release_date": "1999-02-02"
            }
        }
    ]
}
```

</br>

#### **Read Book API**:

Gives information about book

``` 
GET /api/v1/books
```

**Parameters:** 

| Name         | DataType     | Required/Optional | Description               |
|--------------|--------------|-------------------|---------------------------|
| name         | string       | optional          | Name of the book          |
| country      | string       | optional          | Country of the book       |
| publisher    | string       | optional          | Publisher of the book     |
| release_date | number(year) | optional          | Released year of the book |

</br>

**Example:**

Lets call following API to provide an example

``` shell
GET http://localhost:8080/api/v1/books
```

It will return response with following JSON data 

``` JSON
{
    "status_code": 200,
    "status": "success",
    "data": [
        {   
            "id": 1,
            "name": "Good Book",
            "isbn": "978-0553108033",
            "authors": [
                "Martin",
                "ToocoMan"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1999-02-02"
        }
    ]
}
```

</br>

#### **Update Book API**:

Adds a new book to the database.

``` 
PATCH /api/v1/books/:id
```

The request needs to have any of the following JSON data in following format:

``` JSON
{
    "name": "Book Name",
    "isbn": "isbn number",
    "authors": ["author1", "author2"],
    "country": "United States",
    "number_of_pages": 694,
    "publisher": "Publisher name",
    "release_date": "1999-02-02"
}
```

**Example:**

Lets call following API to provide an example.

``` shell
PATCH http://localhost:8080/api/v1/books/1
```

with following data.

``` JSON
{
    "name": "Good Book(updated)",
    "authors": ["Martin", "ToocoMan", "New Author"],
    "country": "Pakistan",
    "publisher": "Bantam Books(new)",
    "release_date": "2020-02-02"
}
```

It will return response with following JSON data 

``` JSON
{
    "status_code": 200,
    "status": "success",
    "message": "The book Good Book was updated successfully",
    "data": {
        "id": 1,
        "name": "Good Book(updated)",
        "isbn": "978-0553108033",
        "authors": [
            "Martin",
            "ToocoMan",
            "New Author"
        ],
        "number_of_pages": 694,
        "publisher": "Bantam Books(new)",
        "country": "Pakistan",
        "release_date": "2020-02-02"
    }
}
```

</br>

#### **Delete Book API**:

Deletes the book, given an id. 

``` 
DELETE /api/v1/books/:id
```

**Example:**

Lets call following API to provide an example

``` shell
DELETE http://localhost:8080/api/v1/books/1
```

It will return response with following JSON data 

``` JSON
{
    "status_code": 200,
    "status": "success",
    "message": "The book Good Book(updated) was deleted successfully",
    "data": []
}
```

</br>

#### **Show Book API**:

Gets the book info, given an id. 

``` 
GET /api/v1/books/:id
```

**Example:**

Lets call following API to provide an example

``` shell
GET http://localhost:8080/api/v1/books/1
```

It will return response with following JSON data 

``` JSON
{
    "status_code": 200,
    "status": "success",
    "data": {
        "name": "Good Book",
        "isbn": "978-0553108033",
        "authors": [
            "Martin",
            "ToocoMan"
        ],
        "number_of_pages": 694,
        "publisher": "Bantam Books",
        "country": "United States",
        "release_date": "1999-02-02"
    }
}
```

## Executing API TestCases:

There are test cases that are developed to test the functionaliity of APIs. To execute tescases run following command. If you are on root folder make sure to navigate to IceAndFire folder first using command `cd IceAndFire`

``` shell
python manage.py test
```

The above command will execute testcases and will give following response on the terminal about test execution.

``` shell
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 4.362s

OK
Destroying test database for alias 'default'...
```

The *OK* will indicate that all testcases have passed successfully. In case of error it will show *ERRORS*.
