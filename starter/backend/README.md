# Full Stack Trivia API Backend
1.Start project locally
2.API Documentation

# Satrt Project locally
Make sure that you cd into the backend folder befor following the steup steps.Also, you need the latest version of Python3 and postgres installed on machine.

To start and run the local develoment server,

1.Initialize and activate a virtualenv:

$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --non-site-packages env
$ sorce env/bin/activate

2. Install the dependencies.
$ pip intsall -r requriments.txt

3. With Postgres running, restore a database using the tricia.psql file provided.
$ createdb trivia
$ createdb trivia_test
$ psql trivia_test < trivia.psql

4. Run the development server:
$ export FLASK_APP=api.py
$ export FLASK_ENV=development
$ flask run

Setting the FLASK_APP variable to src directs flask to use the src directory and the api.py file to find the application.


1. (optional) To execute tests, run

$ dropdb trivia_test
$ createdb trivia_test
$ psql trivia_test < trivia.psql
$ python test_flaskr.py

If you choose to run all tests, it should give this response if everything went fine:

(env) varsha@varsha:~/Desktop/trivia_api/starter/backend$ python3 test_flaskr.py 
............
----------------------------------------------------------------------
Ran 12 tests in 0.570s

OK


# API Documentation
Here you can fina all existing endpoints, which methods can be used, how to work with them & example responses you'll get.

Additionally, common pitfalls & error messages are explained,if application.

# Base URL
Since this API is not hosted on a specific domain,it can only be accessed when flask is run locally.To make requests to the API via curl or postman, you need to use the default domain on which the flask sever is running.

http://127.0.0.1:5000/ 

# How to work with each endpoint
Click on a link to directly get to the resource.

1.Questions

i. GET/questions

$ curl -X GET http://127.0.0.1:5000/questions?page=1

- Fetches a list of dictionaries od questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.

- Returns:
i.List of dict of questions with following fields:

- Request Arguments:

    integer page (optional, 10 questions per page, defaults to 1 if not given)

- Request Headers: None
- Returns:

    List of dict of questions with following fields:
        integer id
        string question
        string answer
        string category
        integer difficulty
    list categories
    list current_category
    integer total_questions
    boolean success

Example response

{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    [...] // + all questions in database
  ], 
  "success": true, 
  "total_questions": 29
}

# Error
If you try fetch a page which does not have anu]y questions, you will encounter an error which looks like this:

curl -X GET http://127.0.0.1:5000/questions?page=152525

will return 

{
  "error": 404, 
  "message": "Not Found", 
  "success": false
}

2. POST/questions

Search Questions

curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'

Create Question

curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a test question?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'

Searches database for questions with a search term, if provided. Otherwise, it will insert a new question into the database.
Request Arguments: None
Request Headers :
    if you want to search (application/json)
        string searchTerm (*required)
    if you want to insert (application/json)
        string question (*required)
        string answer (*required)
        string category (*required)
        integer difficulty (*required)
Returns:
    if you searched:
        List of dict of questions which match the searchTerm with following fields:
            integer id
            string question
            string answer
            string category
            integer difficulty
        List of dict of current_category with following fields:
            integer id
            string type
        integer total_questions
        boolean success
    if you inserted:
        List of dict of all questions with following fields:
            integer id
            string question
            string answer
            string category
            integer difficulty
        integer total_questions
        integer created id from inserted question
        boolean success


Example response

Search Questions
{
  "current_category": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

Create Question 

{
  "created": 56,  //id of question created
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    [...] // + all questions in database
  ], 
  "success": true, 
  "totalQuestions": 22
}

Errors

Search related

If you try to serach for question which does not exits,it will response with an 400 error code.

curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 

will return

{
  "error": 400, 
  "message": "bad_request", 
  "success": false
}

Insert related

curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a question without an answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'

will return

{
  "error": 400, 
  "message": "bad_request", 
  "success": false
}

3. DELETE/questions/<int:que_id>
Delete Questions

curl -X DELETE http://127.0.0.1:5000/questions/10

- Delete specific question based on given id
- Request Arguments:
  -integer question_id
-Request Headers: None
-Returns:
  - integer deleted Id from deleted question.
  - boolean success

Example response

{
  "delete_question": 10, 
  "success": true
}

Errors
If you try to delete a question which does not exist, it will throw an 404 error:

curl -X DELETE http://127.0.0.1:5000/questions/7

will return

{
  "error": 400, 
  "message": "bad_request", 
  "success": false
}

4. POST/quizzes
Play quiz game.

curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'

- Plays quiz gaem by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments:None
- Request Headers:
  i. list previous_questions with integer ids from already asked questions.
  ii. dict quiz_category(optional)with keys:
      a. string type
      b. integer id from category
- Returns:
  i. Exactly one question as dict with following fields:
    . integer id
    . string question
    . string answer
    . string category
    . integer difficulty
  ii. boolean success

Example response

{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}

Errors

If you try to play the quiz game without a valid JSON body, it will response with an 400 error.

curl -X POST http://127.0.0.1:5000/quizzes

will return

{
  "error": 400, 
  "message": "bad_request", 
  "success": false
}

5. GET/categories
Fetch all available categories

curl -X GET http://127.0.0.1:5000/categories

- Fetches a list of all categories with its type as values.
- Request Arguemnts: None
- Request Headers: None
- Returns: A list of categories with its type as values and a success value which indicates status of response.

Example response

{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true
}

Errors

Endpoint does not raise any specific errors.

6. GET/categories/<int:id>/questions
Get all questions from a specific category.

curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1

- Fetch all questions (paginated) from one specific category.
- Request Arguments:
    . integer category_id (*requried)
    . integer page(optinal, 10 questions per page, defaults to 1 if not given)
- Request Headers: None
- Returns:
    i.intger current_category id from inputted category
    ii.List of dict of all questions with following fields:
      . integre id
      . string question
      . string answer
      . string category
      . integer difficulty
    iii.integer total_questions
    iv.boolean success

Example response

{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}

Errors
This endpoint can yeild 2 common errors.For example,if you ask for questions of a catgory that does not exist it will throw as 404 error:

curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1

will return

{
  "error": 404, 
  "message": "Not Found", 
  "success": false
}







