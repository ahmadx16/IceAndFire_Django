
expected_create_book = {
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
                "release_date": "2000-02-02"
            }
        }
    ]
}

expected_read_book = {
    "status_code": 200,
    "status": "success",
    "data": [
        {
            "name": "Good Book",
            "isbn": "978-0553108033",
            "authors": [
                "Martin",
                "ToocoMan"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "2000-02-02"

        }
    ]
}

create_book_data = {
    "name": "Good Book",
    "isbn": "978-0553108033",
    "authors": ["Martin", "ToocoMan"],
    "country": "United States",
    "number_of_pages": 694,
    "publisher": "Bantam Books",
    "release_date": "2000-02-02"
}

update_book_data = {
    "name": "Good Book(updated)"
}

expected_book_update = {
    "status_code": 200,
    "status": "success",
    'message': 'The book Good Book was updated successfully',
    "data":
        {
            "name": "Good Book(updated)",
            "isbn": "978-0553108033",
            "authors": [
                "Martin",
                "ToocoMan"
            ],
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "2000-02-02"

        }

}

expected_delete_book = {
    "status_code": 200,
    "status": "success",
    "message": "The book Good Book was deleted successfully",
    "data": []
}