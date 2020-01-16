import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Question, Category
from src.api import app


class TriviaTestCase(unittest.TestCase):
    """Define test variables and initialize app."""
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('utrivia', 'utrivia123', 'localhost:5432', self.database_name)
        try:
            setup_db(self.app, self.database_path)
        except:
            pass
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            try:
                self.db.init_app(self.app)
            except:
                pass
            # create all tables
            self.db.create_all()
            
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db = SQLAlchemy()
            # self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()    
    # --------------------------------------------------------------------------
    # Tests for categories
    # --------------------------------------------------------------------------  
    
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(len(data['categories']) > 0)

    def test_error_405_get_all_categories(self):
        res = self.client.patch('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed.')
        self.assertEqual(data['success'], False)
    
    # ----------------------------------------------------------------------------------
    # Tests for Questions
    # ---------------------------------------------------------------------------------
        
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
    
    def test_endpoint_not_available(self):
        res = self.client.get('/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_question_by_category(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['current_category'], '1')

    def test_400_get_questions_from_category(self):
        res = self.client.get('/categories/14521524/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
    
    def test_create_question(self):
        res = self.client.post('/questions', json={
            'question': 'Test question?',
            'answer': 'yes',
            'category': '1',
            'difficulty': 1
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])

    def test_create_question_error(self):
        res = self.client.post('/questions', json={
            'question': 'This Test error question?',
            'answer': 'yes',
            'category': '2'
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad_request')

    def test_serach_question(self):
        res = self.client.post('/search', json={
            'searchTerm': 'which'
            })  
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])        
    # ----------------------------------------------------------------------------------
    # Tests for Quizz
    # ----------------------------------------------------------------------------------

    def test_get_quiz_questions_by_category(self):
        json_play_quizz = {
            'previous_questions': [1, 2, 5],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }
        res = self.client.post('/quizzes', json=json_play_quizz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['question'])

    def test_get_quiz_questions_all(self):
        res = self.client.post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {
                'type': 'ALL',
                'id': 0
                }
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_question_to_delete_does_not_exit(self):
        res = self.client.delete('/questions/{}'.format(1236545))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad_request')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 