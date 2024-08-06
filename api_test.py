import pytest
from app import start_app
from backend.models import db, Course, Week, Lecture, CodingQuestion, Submission
from unittest.mock import patch, MagicMock
from backend.src.models import GenerativeFeatures
from flask import Flask, json
from backend import views

@pytest.fixture(scope='module')
def test_client():
    app, jwt = start_app()
    client = app.test_client()
    app_context = app.app_context()
    app_context.push()

    # Drop all tables and create them again
    db.drop_all()
    db.create_all()

    # Add courses
    sample_courses = [
        Course(name='Python', description='Learn the basics of Python programming.')
    ]
    db.session.add_all(sample_courses)
    db.session.commit()

    # Add weeks to each course
    sample_weeks = [
        Week(number=1, course_id=sample_courses[0].id)
    ]
    db.session.add_all(sample_weeks)
    db.session.commit()

    # Add lectures to each week
    sample_lectures = [
        Lecture(title='Introduction', lecture_url='https://youtu.be/8ndsDXohLMQ', week_id=sample_weeks[0].id)
    ]
    db.session.add_all(sample_lectures)
    db.session.commit()

    # Add coding questions to each week
    sample_coding_questions = [
        CodingQuestion(
            content='Write a Python function to reverse a string.',
            test_cases='[{"input": "hello", "output": "olleh"}, {"input": "world", "output": "dlrow"}]',
            solution='def reverse_string(s): return s[::-1]',
            week_id=sample_weeks[0].id
        )
    ]
    db.session.add_all(sample_coding_questions)
    db.session.commit()

    # Add a sample submission
    sample_submissions = [
        Submission(
            code='print("Hello, World!")',
            coding_question_id=sample_coding_questions[0].id
        )
    ]
    db.session.add_all(sample_submissions)
    db.session.commit()

    yield client

    db.session.remove()
    db.drop_all()
    app_context.pop()

@pytest.fixture
def gen_features():
    return GenerativeFeatures()

def test_get_course(test_client):
    """Test retrieving a course by ID."""
    response = test_client.get('/api/courses/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Python'
    assert data['description'] == 'Learn the basics of Python programming.'

def test_get_nonexistent_course(test_client):
    """Test retrieving a course that does not exist."""
    response = test_client.get('/api/courses/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data['message'] == 'Course not found'

def test_get_week(test_client):
    """Test retrieving a week by ID."""
    response = test_client.get('/api/weeks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['number'] == 1
    assert data['course_id'] == 1

def test_get_nonexistent_week(test_client):
    """Test retrieving a week that does not exist."""
    response = test_client.get('/api/weeks/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data['message'] == 'Week not found'

def test_get_lecture(test_client):
    """Test retrieving a lecture by ID."""
    response = test_client.get('/api/lectures/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Introduction'
    assert data['lecture_url'] == 'https://youtu.be/8ndsDXohLMQ'
    assert data['week_id'] == 1

def test_get_nonexistent_lecture(test_client):
    """Test retrieving a lecture that does not exist."""
    response = test_client.get('/api/lectures/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data['message'] == 'Lecture not found'

def test_get_coding_question(test_client):
    """Test retrieving a coding question by ID."""
    response = test_client.get('/api/coding-questions/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'Write a Python function to reverse a string.'
    assert data['test_cases'] == '[{"input": "hello", "output": "olleh"}, {"input": "world", "output": "dlrow"}]'
    assert data['week_id'] == 1

def test_get_nonexistent_coding_question(test_client):
    """Test retrieving a coding question that does not exist."""
    response = test_client.get('/api/coding-questions/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data['message'] == 'Coding question not found'

def test_post_coding_question(test_client):
    """Test creating a new coding question."""
    response = test_client.post('/api/coding-questions', json={
        'content': 'New Coding Question',
        'test_cases': 'Test Case 1',
        'solution': 'Sample Solution',
        'week_id': 1
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Coding question created successfully'

def test_put_coding_question(test_client):
    """Test updating an existing coding question."""
    response = test_client.put('/api/coding-questions/1', json={
        'content': 'Updated Coding Question',
        'test_cases': 'Updated Test Cases',
        'solution': 'Updated Solution'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Coding question updated successfully'

def test_get_submission(test_client):
    """Test retrieving a submission by ID."""
    response = test_client.get('/api/submissions/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 'print("Hello, World!")'
    assert data['coding_question_id'] == 1
    assert 'created_at' in data
    assert 'updated_at' in data
    assert 'status' in data

def test_get_nonexistent_submission(test_client):
    """Test retrieving a submission that does not exist."""
    response = test_client.get('/api/submissions/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data['message'] == 'Submission not found'

def test_post_submission(test_client):
    """Test creating a new submission."""
    response = test_client.post('/api/submissions', json={
        'code': 'print("Hello, World!")',
        'coding_question_id': 1
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Submission created successfully'

def test_put_submission(test_client):
    """Test updating an existing submission."""
    response = test_client.put('/api/submissions/1', json={
        'code': 'print("Updated Code")'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Submission updated successfully'

@patch('backend.src.models.GenerativeFeatures.generate_lecture_summary')
def test_generate_lecture_summary(mock_generate_lecture_summary, test_client):
    """Test generating lecture summary."""
    mock_generate_lecture_summary.return_value = 'summary text'
    response = test_client.post('/api/lecture-summary', json={'videoUrl': 'https://youtu.be/jQ_vO3xjFt0?si=OBucznx9N6eHr5jp'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['summary'] == 'summary text'
    mock_generate_lecture_summary.assert_called_once_with('https://youtu.be/jQ_vO3xjFt0?si=OBucznx9N6eHr5jp')

@patch('backend.src.models.GenerativeFeatures.generate_code_feedback')
def test_compare_ai(mock_generate_code_feedback, test_client):
    """Test comparing AI feedback for a submission."""
    mock_generate_code_feedback.return_value = 'Good job!'
    response = test_client.post('/compare-ai', json={'submission_id': 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data['code_feedback'] == 'Good job!'
    mock_generate_code_feedback.assert_called_once()