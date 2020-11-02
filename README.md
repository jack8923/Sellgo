## Sellgo

Tech Stack:- **Python, Django**   

SetUp :-
1. Clone the repository.
2. Install requirements - `pip install -r requirements.txt`
3. Create PostgreSQL database "sellgo".
4. run `python manage.py make migrations`.
5. run `python manage.py migrate`.
6. run `python manage.py runserver`.

Details:-
The database contains two tables "customer" and "csv_product"
APIs:-
1. /customer  - GET all the customers and POST customers.
2. /customer/<int: pk>  - GET all the unique title orders of customer with 'id=pk'(ReadOnly API).
3. /products :- POST by uploading CSV file 

**FORMAT OF CSV FILE**

![Capture (if photo is not visible open the Capture.png file from the root directory)](Capture.png)
