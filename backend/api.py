 
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy import func
from datetime import timedelta
from backend.models import db, Course, Week, Lecture, CodingQuestion, Submission
api_bp = Blueprint("api", __name__)
api = Api(api_bp)  # Create an Api instance using the Blueprint

class CourseResource(Resource):
    def get(self, course_id=None):
        if course_id:
            course = Course.query.get(course_id)
            if not course:
                return {'message': 'Course not found'}, 404
            return {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'weeks': [{'id': week.id, 'number': week.number} for week in course.weeks]
            }
        else:
            courses = Course.query.all()
            return [{
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'weeks': [{'id': week.id, 'number': week.number} for week in course.weeks]
            } for course in courses]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        existing_course = Course.query.filter_by(name=args['name']).first()
        if existing_course:
            return {'message': 'Course with this name already exists'}, 409  # Conflict status code

        new_course = Course(name=args['name'], description=args.get('description'))
        db.session.add(new_course)
        db.session.commit()

        return {'message': 'Course created successfully', 'id': new_course.id}, 201

    def put(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        if args['name']:
            course.name = args['name']
        if args['description']:
            course.description = args['description']

        db.session.commit()
        return {'message': 'Course updated successfully'}, 200

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted successfully'}, 200

api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')


class WeekResource(Resource):
    def get(self, week_id=None):
        if week_id:
            week = Week.query.get(week_id)
            if not week:
                return {'message': 'Week not found'}, 404
            return {
                'id': week.id,
                'number': week.number,
                'course_id': week.course_id,
                'lectures': [{'id': lecture.id, 'title': lecture.title, 'lecture_url': lecture.lecture_url} for lecture in week.lectures],
                'coding_questions': [{'id': cq.id, 'content': cq.content} for cq in week.coding_questions]
            }
        else:
            weeks = Week.query.all()
            return [{
                'id': week.id,
                'number': week.number,
                'course_id': week.course_id,
                'lectures': [{'id': lecture.id, 'title': lecture.title, 'lecture_url': lecture.lecture_url} for lecture in week.lectures],
                'coding_questions': [{'id': cq.id, 'content': cq.content} for cq in week.coding_questions]
            } for week in weeks]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', type=int, required=True, help='Number cannot be blank')
        parser.add_argument('course_id', type=int, required=True, help='Course ID cannot be blank')
        args = parser.parse_args()

        existing_week = Week.query.filter_by(number=args['number'], course_id=args['course_id']).first()
        if existing_week:
            return {'message': 'Week with this number already exists for this course'}, 409  # Conflict status code

        new_week = Week(number=args['number'], course_id=args['course_id'])
        db.session.add(new_week)
        db.session.commit()

        return {'message': 'Week created successfully', 'id': new_week.id}, 201


    def put(self, week_id):
        week = Week.query.get(week_id)
        if not week:
            return {'message': 'Week not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('number', type=int)
        parser.add_argument('course_id', type=int)
        args = parser.parse_args()

        if args['number']:
            week.number = args['number']
        if args['course_id']:
            week.course_id = args['course_id']

        db.session.commit()
        return {'message': 'Week updated successfully'}, 200

    def delete(self, week_id):
        week = Week.query.get(week_id)
        if not week:
            return {'message': 'Week not found'}, 404

        db.session.delete(week)
        db.session.commit()
        return {'message': 'Week deleted successfully'}, 200

api.add_resource(WeekResource, '/weeks', '/weeks/<int:week_id>')


class LectureResource(Resource):
    def get(self, lecture_id=None):
        if lecture_id:
            lecture = Lecture.query.get(lecture_id)
            if not lecture:
                return {'message': 'Lecture not found'}, 404
            return {
                'id': lecture.id,
                'title': lecture.title,
                'lecture_url': lecture.lecture_url,
                'week_id': lecture.week_id
            }
        else:
            lectures = Lecture.query.all()
            return [{
                'id': lecture.id,
                'title': lecture.title,
                'lecture_url': lecture.lecture_url,
                'week_id': lecture.week_id
            } for lecture in lectures]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
        parser.add_argument('lecture_url', type=str, required=True, help='Lecture URL cannot be blank')
        parser.add_argument('week_id', type=int, required=True, help='Week ID cannot be blank')
        args = parser.parse_args()

        existing_lecture = Lecture.query.filter_by(title=args['title'], lecture_url=args['lecture_url'], week_id=args['week_id']).first()
        if existing_lecture:
            return {'message': 'Lecture with this title and URL already exists for this week'}, 409  # Conflict status code

        new_lecture = Lecture(title=args['title'], lecture_url=args['lecture_url'], week_id=args['week_id'])
        db.session.add(new_lecture)
        db.session.commit()

        return {'message': 'Lecture created successfully', 'id': new_lecture.id}, 201


    def put(self, lecture_id):
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('lecture_url', type=str)
        parser.add_argument('week_id', type=int)
        args = parser.parse_args()

        if args['title']:
            lecture.title = args['title']
        if args['lecture_url']:
            lecture.lecture_url = args['lecture_url']
        if args['week_id']:
            lecture.week_id = args['week_id']

        db.session.commit()
        return {'message': 'Lecture updated successfully'}, 200

    def delete(self, lecture_id):
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 404

        db.session.delete(lecture)
        db.session.commit()
        return {'message': 'Lecture deleted successfully'}, 200

api.add_resource(LectureResource, '/lectures', '/lectures/<int:lecture_id>')


class CodingQuestionResource(Resource):
    def get(self, coding_question_id=None):
        if coding_question_id:
            coding_question = CodingQuestion.query.get(coding_question_id)
            if not coding_question:
                return {'message': 'Coding question not found'}, 404
            return {
                'id': coding_question.id,
                'content': coding_question.content, 
                'test_cases': coding_question.test_cases,
                'solution': coding_question.solution,
                'week_id': coding_question.week_id
            }
        else:
            coding_questions = CodingQuestion.query.all()
            return [{
                'id': coding_question.id,
                'content': coding_question.content,
                'test_cases': coding_question.test_cases,
                'solution': coding_question.solution,
                'week_id': coding_question.week_id
            } for coding_question in coding_questions]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True, help='Content cannot be blank')
        parser.add_argument('test_cases', type=str, required=True, help='Test cases cannot be blank')
        parser.add_argument('solution', type=str)
        parser.add_argument('week_id', type=int, required=True, help='Week ID cannot be blank')
        args = parser.parse_args()

        new_coding_question = CodingQuestion(content=args['content'], test_cases=args['test_cases'], solution=args.get('solution'), week_id=args['week_id'])
        db.session.add(new_coding_question)
        db.session.commit()

        return {'message': 'Coding question created successfully', 'id': new_coding_question.id}, 201

    def put(self, coding_question_id):
        coding_question = CodingQuestion.query.get(coding_question_id)
        if not coding_question:
            return {'message': 'Coding question not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        parser.add_argument('test_cases', type=str)
        parser.add_argument('solution', type=str)
        parser.add_argument('week_id', type=int)
        args = parser.parse_args()

        if args['content']:
            coding_question.content = args['content']
        if args['test_cases']:
            coding_question.test_cases = args['test_cases']
        if args['solution']:
            coding_question.solution = args['solution']
        if args['week_id']:
            coding_question.week_id = args['week_id']

        db.session.commit()
        return {'message': 'Coding question updated successfully'}, 200

    def delete(self, coding_question_id):
        coding_question = CodingQuestion.query.get(coding_question_id)
        if not coding_question:
            return {'message': 'Coding question not found'}, 404

        db.session.delete(coding_question)
        db.session.commit()
        return {'message': 'Coding question deleted successfully'}, 200

api.add_resource(CodingQuestionResource, '/coding-questions', '/coding-questions/<int:coding_question_id>')


class SubmissionResource(Resource):
    def get(self, submission_id=None):
        if submission_id:
            submission = Submission.query.get(submission_id)
            if not submission:
                return {'message': 'Submission not found'}, 404
            return {
                'id': submission.id,
                'code': submission.code,
                'coding_question_id': submission.coding_question_id,
                'created_at': submission.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': submission.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'status': submission.status
            }
        else:
            submissions = Submission.query.all()
            return [{
                'id': submission.id,
                'code': submission.code,
                'coding_question_id': submission.coding_question_id,
                'created_at': submission.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': submission.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'status': submission.status
            } for submission in submissions]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str, required=True, help='Code cannot be blank')
        parser.add_argument('coding_question_id', type=int, required=True, help='Coding question ID cannot be blank')
        args = parser.parse_args()

        new_submission = Submission(code=args['code'], coding_question_id=args['coding_question_id'])
        db.session.add(new_submission)
        db.session.commit()

        return {'message': 'Submission created successfully', 'id': new_submission.id}, 201

    def put(self, submission_id):
        submission = Submission.query.get(submission_id)
        if not submission:
            return {'message': 'Submission not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        parser.add_argument('coding_question_id', type=int)
        args = parser.parse_args()

        if args['code']:
            submission.code = args['code']
        if args['coding_question_id']:
            submission.coding_question_id = args['coding_question_id']

        db.session.commit()
        return {'message': 'Submission updated successfully'}, 200

    def delete(self, submission_id):
        submission = Submission.query.get(submission_id)
        if not submission:
            return {'message': 'Submission not found'}, 404

        db.session.delete(submission)
        db.session.commit()
        return {'message': 'Submission deleted successfully'}, 200

api.add_resource(SubmissionResource, '/submissions', '/submissions/<int:submission_id>')

