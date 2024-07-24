import subprocess
from flask import Blueprint, jsonify, request, render_template
from .models import db, CodingQuestion, Submission
import json
from backend.src.models import GenerativeFeatures

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return 'Hello, World!'

@views.route('/demo')
def demo():
    return render_template('demo.html')

@views.route('/api/lecture-summary', methods=['POST'])
def generate_lecture_summary():
    lecture_video = request.json.get('videoUrl')
    generate = GenerativeFeatures()
    lecture_summary = generate.generate_lecture_summary(lecture_video)
    print(lecture_summary)
    return jsonify({'summary': lecture_summary})

@views.route('/coding_question/<int:question_id>', methods=['GET'])
def get_coding_question(question_id):
    question = CodingQuestion.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'content': question.content,
        'test_cases': question.test_cases
    })

@views.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    test_cases = json.loads(data['test_cases'])
    
    results = []
    for test in test_cases:
        input_data = test['input']
        expected_output = test['output']
        
        # Create a temporary Python script with the user code and the test case
        script = f"""
{code}

print(reverse_string({json.dumps(input_data)}))
"""
        try:
            # Run the script using subprocess
            result = subprocess.run(
                ['python3', '-c', script],
                capture_output=True,
                text=True,
                timeout=5  # Add a timeout to prevent infinite loops
            )
            output = result.stdout.strip()
            if output == expected_output:
                results.append('Correct')
            else:
                results.append(f'Incorrect (Got: {output})')
        except subprocess.TimeoutExpired:
            results.append('Error: Timeout')
        except Exception as e:
            results.append(f'Error: {str(e)}')

    return jsonify(results)

@views.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.get_json()
    coding_question_id = data['coding_question_id']
    code = data['code']

    # Find the existing submission if it exists
    submission = Submission.query.filter_by(coding_question_id=coding_question_id).first()
    if submission:
        submission.code = code
        submission.status = 'updated'
        message = 'Submission updated'
    else:
        submission = Submission(
            code=code,
            coding_question_id=coding_question_id,
            status='submitted'
        )
        db.session.add(submission)
        message = 'Submission received'

    db.session.commit()
    return jsonify({'message': message}), 201
