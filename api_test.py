import unittest
from app import start_app
from backend.models import db, Course, Week, Lecture, CodingQuestion, Submission
from unittest.mock import patch, MagicMock
from backend.src.models import GenerativeFeatures

from flask import Flask, json
from backend import views

class APITestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the database with sample data."""
        self.app, self.jwt = start_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Drop all tables and create them again
        db.drop_all()
        db.create_all()

        # Add courses
        self.sample_courses = [
            Course(name='Python', description='Learn the basics of Python programming.')
        ]
        db.session.add_all(self.sample_courses)
        db.session.commit()

        # Index to use in tests
        self.test_sample_index = 0

        # Add weeks to each course
        self.sample_weeks = [
            Week(number=1, course_id=self.sample_courses[0].id)
        ]
        db.session.add_all(self.sample_weeks)
        db.session.commit()

        # Add lectures to each week
        self.sample_lectures = [
            Lecture(title='Introduction', lecture_url='https://youtu.be/8ndsDXohLMQ', week_id=self.sample_weeks[0].id)
        ]
        db.session.add_all(self.sample_lectures)
        db.session.commit()

        # Add coding questions to each week
        self.sample_coding_questions = [
            CodingQuestion(
                content='Write a Python function to reverse a string.',
                test_cases='[{"input": "hello", "output": "olleh"}, {"input": "world", "output": "dlrow"}]',
                solution='def reverse_string(s): return s[::-1]',
                week_id=self.sample_weeks[0].id
            )
        ]
        db.session.add_all(self.sample_coding_questions)
        db.session.commit()

        # Add a sample submission
        self.sample_submissions = [
            Submission(
                code='print("Hello, World!")',
                coding_question_id=self.sample_coding_questions[0].id
            )
        ]
        db.session.add_all(self.sample_submissions)
        db.session.commit()

        print('Dummy data added successfully!')

        #Set up the GenerativeFeatures instance and mock dependencies.
        self.gen_features = GenerativeFeatures()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    ############################################## Test cases for CourseResource ##############################################
    def test_get_course(self):
        """Test retrieving a course by ID."""
        response = self.client.get(f'/api/courses/{self.sample_courses[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], self.sample_courses[self.test_sample_index].name)
        self.assertEqual(data['description'], self.sample_courses[self.test_sample_index].description)

    def test_get_nonexistent_course(self):
        """Test retrieving a course that does not exist."""
        response = self.client.get('/api/courses/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Course not found')

    ############################################## Test cases for WeekResource ##############################################
    def test_get_week(self):
        """Test retrieving a week by ID."""
        response = self.client.get(f'/api/weeks/{self.sample_weeks[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['number'], self.sample_weeks[self.test_sample_index].number)
        self.assertEqual(data['course_id'], self.sample_weeks[self.test_sample_index].course_id)

    def test_get_nonexistent_week(self):
        """Test retrieving a week that does not exist."""
        response = self.client.get('/api/weeks/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Week not found')
        
    ############################################## Test cases for LectureResource ##############################################
    def test_get_lecture(self):
        """Test retrieving a lecture by ID."""
        response = self.client.get(f'/api/lectures/{self.sample_lectures[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], self.sample_lectures[self.test_sample_index].title)
        self.assertEqual(data['lecture_url'], self.sample_lectures[self.test_sample_index].lecture_url)
        self.assertEqual(data['week_id'], self.sample_lectures[self.test_sample_index].week_id)

    def test_get_nonexistent_lecture(self):
        """Test retrieving a lecture that does not exist."""
        response = self.client.get('/api/lectures/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Lecture not found')
        
    ############################################## Test cases for CodingQuestionResource ##############################################
    def test_get_coding_question(self):
        """Test retrieving a coding question by ID."""
        response = self.client.get(f'/api/coding-questions/{self.sample_coding_questions[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['content'], self.sample_coding_questions[self.test_sample_index].content)
        self.assertEqual(data['test_cases'], self.sample_coding_questions[self.test_sample_index].test_cases)
        self.assertEqual(data['week_id'], self.sample_coding_questions[self.test_sample_index].week_id)

    def test_get_nonexistent_coding_question(self):
        """Test retrieving a coding question that does not exist."""
        response = self.client.get('/api/coding-questions/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Coding question not found')

    def test_post_coding_question(self):
        """Test creating a new coding question."""
        response = self.client.post('/api/coding-questions', json={
            'content': 'New Coding Question',
            'test_cases': 'Test Case 1',
            'solution': 'Sample Solution',
            'week_id': self.sample_weeks[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Coding question created successfully')

    def test_put_coding_question(self):
        """Test updating an existing coding question."""
        response = self.client.put(f'/api/coding-questions/{self.sample_coding_questions[self.test_sample_index].id}', json={
            'content': 'Updated Coding Question',
            'test_cases': 'Updated Test Cases',
            'solution': 'Updated Solution'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Coding question updated successfully')
        
    ############################################## Test cases for SubmissionResource ##############################################
    def test_get_submission(self):
        """Test retrieving a submission by ID."""
        response = self.client.get(f'/api/submissions/{self.sample_submissions[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['code'], self.sample_submissions[self.test_sample_index].code)
        self.assertEqual(data['coding_question_id'], self.sample_submissions[self.test_sample_index].coding_question_id)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertIn('status', data)

    def test_get_nonexistent_submission(self):
        """Test retrieving a submission that does not exist."""
        response = self.client.get('/api/submissions/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Submission not found')

    def test_post_submission(self):
        """Test creating a new submission."""
        response = self.client.post('/api/submissions', json={
            'code': 'print("Hello, World!")',
            'coding_question_id': self.sample_coding_questions[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Submission created successfully')

    def test_put_submission(self):
        """Test updating an existing submission."""
        response = self.client.put(f'/api/submissions/{self.sample_submissions[self.test_sample_index].id}', json={
            'code': 'print("Updated Code")'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Submission updated successfully')
        
    ############################################## Test cases for Lecture Summary ##############################################
    @patch('backend.src.models.GenerativeFeatures.generate_lecture_summary')
    def test_generate_lecture_summary(self, mock_generate_lecture_summary):
        """Test generating lecture summary."""
        mock_generate_lecture_summary.return_value = 'summary text'
        response = self.client.post('/api/lecture-summary', json={'videoUrl': 'https://youtu.be/jQ_vO3xjFt0?si=OBucznx9N6eHr5jp'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['summary'], 'summary text')
        mock_generate_lecture_summary.assert_called_once_with('https://youtu.be/jQ_vO3xjFt0?si=OBucznx9N6eHr5jp')