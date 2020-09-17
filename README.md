![alt text](https://img.icons8.com/officel/40/000000/winter.png) ![alt text](https://img.icons8.com/emoji/48/000000/fire.png)

# Ice and Fire API 

This application is built on django-rest framework. It implements a REST API that calls an external API service to get information about books. Additionally, it implements a simple *CRUD* (Create, Read, Update, Delete) API with a local database.

The external API that is used here is the ​[Ice And Fire](https://anapioficeandfire.com/Documentation#books) API.

## Instructions

Following are the instructions that you need perform in order to run the application

1. [Clone the repository](#cloning-the-repository)
1. [Database Setup](#database-setup)
1. [Python Environment Setup](#python-environment-setup)
1. [Launching the Application](#launching-the-application)
1. [Calling the APIs](#calling-the-apis)
1. [Executing API TestCases](#executing-api-testcases)

 

## Cloning the Repository

Clone this repository and switch to the `auth_generic` branch as it currently contains the latest code. Run the following commands on your shell

``` shell
git clone https://github.com/ahmadx16/IceAndFire_Django.git
cd IceAndFire_Django/
git checkout auth_generic
```

The above commands will download the repository and switch the branch.

## Database Setup

**Note**: If you want to quickly see application up and running you may skip MySQL Connection Setup, and use the default sqlite database (you do not need to do any configuration for this).

### MySQL Connection Setup

This application is configured to work with MySQL local server. In order to connect to MySQL Server to do following steps:

1.  Install the MySQL server if it is not locally installed on your machine. You can visit [MySQL installation guide](https://dev.MySQL.com/doc/MySQL-installation-excerpt/5.7/en/) for the details of installation of server.
2. Create a database on MySQL and add the database name, user, and password on file [settings.py](IceAndFire/IceAndFire/settings.py) (from line 83-88) in the *DATABASE* dictionary . 

``` python
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

## Python Environment Setup

It is recommended to create a virtual environment before installing django. This project uses [virtualenv](https://pypi.org/project/virtualenv/) for this purpose. You can create a python virtual environment by giving path where you want to create a virtual environment and run following commands.

``` shell
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```

The above commands will create and activate a new virtual environment. Learn more about virtual environment virtualenv [here](https://pypi.org/project/virtualenv/).

**Note:** Before installing requirements below, you may want to decide a database that you want to work on with this application. File [requirements.txt](requirements.txt) contains a requirement `mysqlclient==2.0.1` which is only required when you want to use MySQL as database. If you choose MySQL  please visit [mysqlclient](https://pypi.org/project/mysqlclient/) before, to verify if you need to install MySQL development headers and libraries. Please remove `mysqlclient==2.0.1` requirement at line 5 from `requirements.txt` if you want to work with another database.

Now install application requirements using following command.

``` shell
pip install -r requirements.txt
```

## Launching the Application

Before launching the application run the following command on terminal.

``` shell
cd IceAndFire
python manage.py migrate
```

This command will create the database tables that we have specified in the models of our application.

Now run command.

``` shell
python manage.py runserver 8080
```

This command will start the backend server at 127.0.0.1:8080

## Calling the APIs

Following are the APIs that user can call when the server is started.

### Register User:

Registers a new user in the local database.

``` 
POST /users/register
```

The request needs to have JSON data in following format:

``` JSON
{
    "first_name":"First Name",
    "last_name":"Last Name",
    "username":"username",
    "password":"AStrongPass123",
    "password2":"AStrongPass123"
}
```

**Example:**

Lets call following API to provide an example.

``` shell
POST http://localhost:8080/users/register
```

with following data.

``` JSON
{
    "first_name":"First Name",
    "last_name":"Last Name",
    "username":"username",
    "password":"AStrongPass123",
    "password2":"AStrongPass123"
}
```

It will return a generated token in following format.

``` JSON
{
    "token": "870804328bda58e845530c7804bb144d52abdd94"
}
```

### Login User:

Returns a token for an authenticated user.

``` 
POST /users/login
```

The request needs to have JSON data in following format:

``` JSON
{
    "username":"username",
    "password":"AStrongPass123"
}
```

**Example:**

Lets call following API to provide an example.

``` shell
POST http://localhost:8080/users/login
```

with following data.

``` JSON
{
    "username":"username",
    "password":"AStrongPass123"
}
```

It will return the token in following format.

``` JSON
{
    "token": "870804328bda58e845530c7804bb144d52abdd94"
}
```

### Get External Books:

This API calls an [external API](https://anapioficeandfire.com/Documentation#books) and returns a filtered book information. 

``` 
GET /api/external-books?name=:nameOfABook
```

**Request Header:**

The request requires an authorization token on the header field in following format. 

``` shell
Authorization: Token {token}
```

Replace *{token}* above with the token you get when calling login or register API.

**Parameter:** 

| Name         | DataType     | Required/Optional | Description               |
|--------------|--------------|-------------------|---------------------------|
| name         | string       | required          | Name of the book          |

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

### CRUD APIs on Local Database:

Following are the APIs that interacts with the local database.

#### **Create Book API**:

Adds a new book to the database.

``` 
POST /api/v1/books
```

**Request Header:**

The request requires an authorization token on the header field in following format. 

``` shell
Authorization: Token {token}
```

Replace *{token}* above with the token you get when calling login or register API.

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
    "data":  {
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

#### **Read Book API**:

Gives information about book

``` 
GET /api/v1/books
```

**Request Header:**

The request requires an authorization token on the header field in following format. 

``` shell
Authorization: Token {token}
```

Replace *{token}* above with the token you get when calling login or register API.

**Parameters:** 

| Name         | DataType     | Required/Optional | Description               |
|--------------|--------------|-------------------|---------------------------|
| search         | string       | optional          | Searches for name/country/publisher/release year like strings in books. It does case-insensitive partial matching.

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

#### **Update Book API**:

Adds a new book to the database.

``` 
PATCH /api/v1/books/:id
```

**Request Header:**

The request requires an authorization token on the header field in following format. 

``` shell
Authorization: Token {token}
```

Replace *{token}* above with the token you get when calling login or register API.

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

#### **Delete Book API**:

Deletes the book, given an id. 

``` 
DELETE /api/v1/books/:id
```

**Request Header:**

The request requires an authorization token on the header field in following format. 

``` shell
Authorization: Token {token}
```

Replace *{token}* above with the token you get when calling login or register API.

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

#### **Show Book API**:

Gets the book info, given an id. 

``` 
GET /api/v1/books/:id
```

**Request Header:**

The request requires an authorization token on the header field in following format. 
```shell
Authorization: Token {token}
```
Replace *{token}* above with the token you get when calling login or register API.


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
