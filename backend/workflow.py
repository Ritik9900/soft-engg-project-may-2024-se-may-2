import configparser
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

#For reading configuration files for OpenAI Key Credentials
config = configparser.ConfigParser()
config.read('./credentials.ini')

OPENAI_API_KEY = config.get('OpenAI', 'api_key')

#setting API key as environment variable
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from src.models import GenerativeFeatures

# Lecture Video Url
# lecture_video = 'https://youtu.be/jQ_vO3xjFt0?si=OBucznx9N6eHr5jp'
@app.route('/api/lecture-summary', methods=['POST'])
def generate_lecture_summary():
    lecture_video = request.json.get('videoUrl')
    generate = GenerativeFeatures()
    lecture_summary = generate.generate_lecture_summary(lecture_video)
    print(lecture_summary)
    return jsonify({'summary': lecture_summary})




# Sample student code and solution code for testing
# student_code = '''
# def count_frequencies(lst):
#     frequency = []
#     for item in lst:
#         frequency[item] = lst.count(item)
#     return frequency
#     '''

# solution_code = '''
# def count_frequencies(lst):
#     frequency = {}
#     for item in lst:
#         if item in frequency:
#             frequency[item] += 1
#         else:
#             frequency[item] = 1
#     return frequency
#     '''

# generate = GenerativeFeatures()

# lecture_summary = generate.generate_lecture_summary(lecture_video)
# code_feedback = generate.generate_code_feedback(student_code, solution_code)

# print(lecture_summary)

# print(code_feedback)