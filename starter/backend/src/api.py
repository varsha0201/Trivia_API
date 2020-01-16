import os
import random
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

app = Flask(__name__)
# To run Server, execute from backend directory:
# Only one Time:
# export FLASK_APP=api.py
# export FLASK_ENV=development
# flask run
setup_db(app)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
    )
    return response
# ------------------------------------------------------------------------------------
# Custum Function
# ------------------------------------------------------------------------------------


def pagination_questions(request, selection):
    # Get page from request. If not given, default to 1
    page = request.args.get("page", 1, type=int)
    # Calculate start and end slicing
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # Format selection into list of dicts and slice
    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]
    return current_questions

# API questions Endpoints
# ------------------------------------------------------------------------------------


@app.route("/questions", methods=["GET"])
def get_questions():
    # Returns paginated questions
    selection = Question.query.order_by(Question.id).all()
    question_paginated = pagination_questions(request, selection)
    if len(question_paginated) == 0:
        abort(404)
    categories = Category.query.all()
    categories_all = [category.format() for category in categories]
    # Initialize empty list to be filled & returned
    categories_returned = []
    for c in categories_all:
        categories_returned.append(c["type"])
    return jsonify({
        "success": True,
        "questions": question_paginated,
        "total_questions": len(selection),
        "categories": categories_returned,
        "current_category": categories_returned,
        })


@app.route("/search", methods=["POST"])
def serach_questions():
    body = request.get_json()
    # If request does not contain valid JSON, raise 400.
    if not body:
        abort(400)
    searchterm = body.get('searchTerm')
    if searchterm:
        # If json body contains a search term, execute question search
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchterm)))
        create_question = pagination_questions(request, selection)
        # If no question could be found, return 404
        if not selection:
            abort(404)
        # Also query for categories and return as list of dict
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'questions': create_question,
            'total_questions': len(selection.all()),
            'current_category': categories_all
            })  


@app.route('/questions', methods=['POST'])
def create_question():
    body = request.get_json()
    # Get field informations from request body
    question = body.get('question')
    answer = body.get('answer')
    category = body.get('category')
    difficulty = body.get('difficulty')
    # Make sure that all requried fields are given otherwise, responds with error message.
    if not question or not answer or not category or not difficulty:
        abort(400)
    try:
        # Try to insert a new question, get all paginated questions.
        question= Question(question=question, answer=answer, difficulty=difficulty, category=category)
        question.insert()
        selection = Question.query.order_by(Question.id).all()
        current_questions = pagination_questions(request, selection)
        # Return successfully response.
        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()) 
            })
    except:
        abort(422)
# ---------------------------------------------------------------------------------
# Endpoint DELETE questions
# ---------------------------------------------------------------------------------


@app.route("/questions/<int:que_id>", methods=["DELETE"])
def delete_question(que_id):
    question = Question.query.filter(Question.id == que_id).one_or_none()

    if question is None:
        # If no question with given id was found, raise 404 and explain what went wrong.
        abort(400)

    try:
        # Try to delete a new question. If anything went wrong, raise 422 "unprocessable"
        question.delete()
        # Return succesfull response with deleted question id
        return jsonify({"success": True, "delete_question": que_id})
    except:
        abort(422)


# ----------------------------------------------------------------------------------
# Endpoint Categories
# ----------------------------------------------------------------------------------


@app.route("/categories", methods=["GET"])
def get_categories():
    # Get all categories
    category_info = Category.query.all()
    # If no categories could be found,throw 404.
    if len(category_info) == 0:
        abort(404)
    # Format it as list of cicts
    categories = [category.type for category in category_info]
    return jsonify({"success": True, "categories": categories})


@app.route("/categories/<int:id>/questions", methods=["GET"])
def getByCategory(id):
    # Query for all Questions that much category id
    selection = Question.query.filter(Question.category == id).all()
    # Paginate and format question into list of dicts
    questions_paginated = pagination_questions(request, selection)
    if len(questions_paginated) == 0:
    # If paginated questions is empty it means the page selected does not contain any questions.
        abort(404)
    category = Category.query.get_or_404(id)
    # Return succesfully response
    return jsonify({
        "success": True,
        "questions": questions_paginated,
        "total_questions": len(selection),
        "current_category": id,
        })
    category = Category.query.filter(Category.id == category_id).one_or_none()
    if not category:
        # If no category with given id found, raise 404 and explain what went wrong. 
        abort(400)
    try:
        # Try to delete a category.If anything went wrong, raise 422 "unprocessable"
        category.delete()
        # Return successfull response with deleted category id.
        return jsonify({
            'success': True,
            'deleted': category_id
            })
    except:
        abort(422)
# ----------------------------------------------------------------------------------
# Endpoint /quizzes
# ----------------------------------------------------------------------------------


@app.route("/quizzes", methods=["POST"])
def quiz():
    body = request.get_json()

    if not body:
        # If no JSON Body was given, raise error.
        abort(400)

    # Get paramters from JSON Body.
    previous_questions = body.get("previous_questions", None)
    current_category = body.get("current_category", None)

    if not previous_questions:
        if current_category:
            # if no list with previous questions is given, but a category , just gut any question from this category.
            quesntion_raw = Question.query.filter(
                Question.category == str(current_category["id"])
            ).all()
        else:
            # if no list with previous questions is given and also no category , just gut any question.
            quesntion_raw = Question.query.all()

    else:
        if current_category:
            # if a list with previous questions is given and also a catgoey, query for questions which are not contained in previous question and are in given categoey.
            quesntion_raw = (
                Question.query.filter(Question.category == str(current_category["id"]))
                .filter(Question.id.notin_(previous_questions))
                .all()
            )
        else:
            # if a list with previous questions is given but no catgory, query for questions which are not conatined in previous question.
            quesntion_raw = Question.query.filter(
                Question.id.notin_(previous_questions)
            ).all()
    # Format questions & get a random question.
    question_formatted = [question.format() for question in quesntion_raw]
    random_question = question_formatted[random.randint(0, len(question_formatted))]

    return jsonify({"success": True, "question": random_question})


# ----------------------------------------------------------------------------------
# API error handler & formatter.
# ----------------------------------------------------------------------------------


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad_request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed."}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "internal server error"}),
        500,
    )

from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

app = Flask(__name__)
# To run Server, execute from backend directory:
# Only one Time:
# export FLASK_APP=api.py
# export FLASK_ENV=development
# flask run
setup_db(app)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
    )
    return response
# ------------------------------------------------------------------------------------
# Custum Function
# ------------------------------------------------------------------------------------


def pagination_questions(request, selection):
    # Get page from request. If not given, default to 1
    page = request.args.get("page", 1, type=int)
    # Calculate start and end slicing
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # Format selection into list of dicts and slice
    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]
    return current_questions

# API questions Endpoints
# ------------------------------------------------------------------------------------


@app.route("/questions", methods=["GET"])
def get_questions():
    # Returns paginated questions
    selection = Question.query.order_by(Question.id).all()
    question_paginated = pagination_questions(request, selection)
    if len(question_paginated) == 0:
        abort(404)
    categories = Category.query.all()
    categories_all = [category.format() for category in categories]
    # Initialize empty list to be filled & returned
    categories_returned = []
    for c in categories_all:
        categories_returned.append(c["type"])
    return jsonify({
        "success": True,
        "questions": question_paginated,
        "total_questions": len(selection),
        "categories": categories_returned,
        "current_category": categories_returned,
        })


@app.route("/search", methods=["POST"])
def serach_questions():
    body = request.get_json()
    # If request does not contain valid JSON, raise 400.
    if not body:
        abort(400)
    searchterm = body.get('searchTerm')
    if searchterm:
        # If json body contains a search term, execute question search
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchterm)))
        create_question = pagination_questions(request, selection)
        # If no question could be found, return 404
        if not selection:
            abort(404)
        # Also query for categories and return as list of dict
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'questions': create_question,
            'total_questions': len(selection.all()),
            'current_category': categories_all
            })  


@app.route('/questions', methods=['POST'])
def create_question():
    body = request.get_json()
    # Get field informations from request body
    question = body.get('question')
    answer = body.get('answer')
    category = body.get('category')
    difficulty = body.get('difficulty')
    # Make sure that all requried fields are given otherwise, responds with error message.
    if not question or not answer or not category or not difficulty:
        abort(400)
    try:
        # Try to insert a new question, get all paginated questions.
        question= Question(question=question, answer=answer, difficulty=difficulty, category=category)
        question.insert()
        selection = Question.query.order_by(Question.id).all()
        current_questions = pagination_questions(request, selection)
        # Return successfully response.
        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()) 
            })
    except:
        abort(422)
# ---------------------------------------------------------------------------------
# Endpoint DELETE questions
# ---------------------------------------------------------------------------------


@app.route("/questions/<int:que_id>", methods=["DELETE"])
def delete_question(que_id):
    question = Question.query.filter(Question.id == que_id).one_or_none()

    if question is None:
        # If no question with given id was found, raise 404 and explain what went wrong.
        abort(400)

    try:
        # Try to delete a new question. If anything went wrong, raise 422 "unprocessable"
        question.delete()
        # Return succesfull response with deleted question id
        return jsonify({"success": True, "delete_question": que_id})
    except:
        abort(422)


# ----------------------------------------------------------------------------------
# Endpoint Categories
# ----------------------------------------------------------------------------------


@app.route("/categories", methods=["GET"])
def get_categories():
    # Get all categories
    category_info = Category.query.all()
    # If no categories could be found,throw 404.
    if len(category_info) == 0:
        abort(404)
    # Format it as list of cicts
    categories = [category.type for category in category_info]
    return jsonify({"success": True, "categories": categories})


@app.route("/categories/<int:id>/questions", methods=["GET"])
def getByCategory(id):
    # Query for all Questions that much category id
    selection = Question.query.filter(Question.category == id).all()
    # Paginate and format question into list of dicts
    questions_paginated = pagination_questions(request, selection)
    if len(questions_paginated) == 0:
    # If paginated questions is empty it means the page selected does not contain any questions.
        abort(404)
    category = Category.query.get_or_404(id)
    # Return succesfully response
    return jsonify({
        "success": True,
        "questions": questions_paginated,
        "total_questions": len(selection),
        "current_category": id,
        })
    category = Category.query.filter(Category.id == category_id).one_or_none()
    if not category:
        # If no category with given id found, raise 404 and explain what went wrong. 
        abort(400)
    try:
        # Try to delete a category.If anything went wrong, raise 422 "unprocessable"
        category.delete()
        # Return successfull response with deleted category id.
        return jsonify({
            'success': True,
            'deleted': category_id
            })
    except:
        abort(422)
# ----------------------------------------------------------------------------------
# Endpoint /quizzes
# ----------------------------------------------------------------------------------


@app.route("/quizzes", methods=["POST"])
def quiz():
    body = request.get_json()

    if not body:
        # If no JSON Body was given, raise error.
        abort(400)

    # Get paramters from JSON Body.
    previous_questions = body.get("previous_questions", None)
    current_category = body.get("current_category", None)

    if not previous_questions:
        if current_category:
            # if no list with previous questions is given, but a category , just gut any question from this category.
            quesntion_raw = Question.query.filter(
                Question.category == str(current_category["id"])
            ).all()
        else:
            # if no list with previous questions is given and also no category , just gut any question.
            quesntion_raw = Question.query.all()

    else:
        if current_category:
            # if a list with previous questions is given and also a catgoey, query for questions which are not contained in previous question and are in given categoey.
            quesntion_raw = (
                Question.query.filter(Question.category == str(current_category["id"]))
                .filter(Question.id.notin_(previous_questions))
                .all()
            )
        else:
            # if a list with previous questions is given but no catgory, query for questions which are not conatined in previous question.
            quesntion_raw = Question.query.filter(
                Question.id.notin_(previous_questions)
            ).all()
    # Format questions & get a random question.
    question_formatted = [question.format() for question in quesntion_raw]
    random_question = question_formatted[random.randint(0, len(question_formatted))]

    return jsonify({"success": True, "question": random_question})


# ----------------------------------------------------------------------------------
# API error handler & formatter.
# ----------------------------------------------------------------------------------


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad_request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed."}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "internal server error"}),
        500,
    )
