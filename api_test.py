import unittest
from app import start_app
from backend.models import db, Course, Week, Lecture, CodingQuestion, Submission

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

    def tearDown(self):
        """Clean up the database after each test."""
        # db.session.remove()
        # db.drop_all()
        # self.app_context.pop()

    def test_test(self):
        self.assertEqual('a','a')

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

    def test_post_course(self):
        """Test creating a new course."""
        response = self.client.post('/api/courses', json={
            'name': 'New Course',
            'description': 'This is a new course'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Course created successfully')

    def test_post_existing_course(self):
        """Test creating a course with an existing name."""
        response = self.client.post('/api/courses', json={
            'name': 'Python',
            'description': 'This is a new course'
        })
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['message'], 'Course with this name already exists')

    def test_put_course(self):
        """Test updating an existing course."""
        response = self.client.put(f'/api/courses/{self.sample_courses[self.test_sample_index].id}', json={
            'name': 'Updated Course',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Course updated successfully')

    def test_delete_course(self):
        """Test deleting an existing course."""
        response = self.client.delete(f'/api/courses/{self.sample_courses[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Course deleted successfully')

    def test_delete_nonexistent_course(self):
        """Test deleting a course that does not exist."""
        response = self.client.delete('/api/courses/9999')
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

    def test_post_week(self):
        """Test creating a new week."""
        response = self.client.post('/api/weeks', json={
            'number': 2,
            'course_id': self.sample_courses[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Week created successfully')

    def test_post_existing_week(self):
        """Test creating a week with an existing number for the same course."""
        response = self.client.post('/api/weeks', json={
            'number': 1,
            'course_id': self.sample_courses[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['message'], 'Week with this number already exists for this course')

    def test_put_week(self):
        """Test updating an existing week."""
        response = self.client.put(f'/api/weeks/{self.sample_weeks[self.test_sample_index].id}', json={
            'number': 2
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Week updated successfully')

    def test_delete_week(self):
        """Test deleting an existing week."""
        response = self.client.delete(f'/api/weeks/{self.sample_weeks[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Week deleted successfully')

    def test_delete_nonexistent_week(self):
        """Test deleting a week that does not exist."""
        response = self.client.delete('/api/weeks/9999')
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

    def test_post_lecture(self):
        """Test creating a new lecture."""
        response = self.client.post('/api/lectures', json={
            'title': 'New Lecture',
            'lecture_url': 'http://newexample.com',
            'week_id': self.sample_weeks[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Lecture created successfully')

    def test_post_existing_lecture(self):
        """Test creating a lecture with an existing title and URL for the same week."""
        response = self.client.post('/api/lectures', json={
            'title': 'Sample Lecture',
            'lecture_url': 'http://example.com',
            'week_id': self.sample_weeks[self.test_sample_index].id
        })
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['message'], 'Lecture with this title and URL already exists for this week')

    def test_put_lecture(self):
        """Test updating an existing lecture."""
        response = self.client.put(f'/api/lectures/{self.sample_lectures[self.test_sample_index].id}', json={
            'title': 'Updated Lecture',
            'lecture_url': 'http://updatedexample.com'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Lecture updated successfully')

    def test_delete_lecture(self):
        """Test deleting an existing lecture."""
        response = self.client.delete(f'/api/lectures/{self.sample_lectures[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Lecture deleted successfully')

    def test_delete_nonexistent_lecture(self):
        """Test deleting a lecture that does not exist."""
        response = self.client.delete('/api/lectures/9999')
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

    def test_delete_coding_question(self):
        """Test deleting an existing coding question."""
        response = self.client.delete(f'/api/coding-questions/{self.sample_coding_questions[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Coding question deleted successfully')

    def test_delete_nonexistent_coding_question(self):
        """Test deleting a coding question that does not exist."""
        response = self.client.delete('/api/coding-questions/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Coding question not found')

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

    def test_delete_submission(self):
        """Test deleting an existing submission."""
        response = self.client.delete(f'/api/submissions/{self.sample_submissions[self.test_sample_index].id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Submission deleted successfully')

    def test_delete_nonexistent_submission(self):
        """Test deleting a submission that does not exist."""
        response = self.client.delete('/api/submissions/9999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], 'Submission not found')