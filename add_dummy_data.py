from datetime import datetime
from backend.models import db, Course, Week, Lecture, CodingQuestion, Submission
from app import app

with app.app_context():
    # Drop all tables and create them again
    db.drop_all()
    db.create_all()

    # Add courses
    courses = [
        Course(name='Python Basics', description='Learn the basics of Python programming.'),
        Course(name='Advanced Python', description='Deep dive into advanced Python concepts.'),
        Course(name='Python for Data Science', description='Apply Python in the field of Data Science.')
    ]

    db.session.add_all(courses)
    db.session.commit()

    # Add weeks to each course
    weeks = [
        Week(number=1, course_id=1),
        Week(number=2, course_id=1),
        Week(number=3, course_id=1),
        Week(number=1, course_id=2),
        Week(number=2, course_id=2),
        Week(number=3, course_id=2),
        Week(number=1, course_id=3),
        Week(number=2, course_id=3),
        Week(number=3, course_id=3)
    ]

    db.session.add_all(weeks)
    db.session.commit()

    # Add lectures to each week
    lectures = [
        # Week 1, Course 1
        Lecture(title='Introduction to Python', lecture_url='https://www.youtube.com/watch?v=rfscVS0vtbw', week_id=1),
        Lecture(title='Python Variables', lecture_url='https://www.youtube.com/watch?v=nhpQIwa9VNg', week_id=1),
        Lecture(title='Python Data Types', lecture_url='https://www.youtube.com/watch?v=8O5kXJke7Vg', week_id=1),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=1),
        # Week 2, Course 1
        Lecture(title='Python Control Flow', lecture_url='https://www.youtube.com/watch?v=sxTmJE4k0ho', week_id=2),
        Lecture(title='Python Functions', lecture_url='https://www.youtube.com/watch?v=9Os0o3wzS_I', week_id=2),
        Lecture(title='Python Modules', lecture_url='https://www.youtube.com/watch?v=6r7G5a6r34s', week_id=2),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=2),
        # Week 3, Course 1
        Lecture(title='Python Classes', lecture_url='https://www.youtube.com/watch?v=ZDa-Z5JzLYM', week_id=3),
        Lecture(title='Python Inheritance', lecture_url='https://www.youtube.com/watch?v=RSl87lqOXDE', week_id=3),
        Lecture(title='Python Standard Library', lecture_url='https://www.youtube.com/watch?v=DPD_PpVsR2Q', week_id=3),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=3),
        # Week 1, Course 2
        Lecture(title='Advanced List Comprehensions', lecture_url='https://www.youtube.com/watch?v=3dt4OGnU5sM', week_id=4),
        Lecture(title='Decorators in Python', lecture_url='https://www.youtube.com/watch?v=FsAPt_9Bf3U', week_id=4),
        Lecture(title='Generators in Python', lecture_url='https://www.youtube.com/watch?v=bD05uGo_sVI', week_id=4),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=4),
        # Week 2, Course 2
        Lecture(title='Context Managers', lecture_url='https://www.youtube.com/watch?v=-aKFBoZpiqA', week_id=5),
        Lecture(title='Python Metaclasses', lecture_url='https://www.youtube.com/watch?v=2p6l5QWoivk', week_id=5),
        Lecture(title='Concurrency in Python', lecture_url='https://www.youtube.com/watch?v=IEEhzQoKtQU', week_id=5),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=5),
        # Week 3, Course 2
        Lecture(title='Asyncio in Python', lecture_url='https://www.youtube.com/watch?v=tSLDcRkgTsY', week_id=6),
        Lecture(title='Python Coroutines', lecture_url='https://www.youtube.com/watch?v=ZzfHjytDceU', week_id=6),
        Lecture(title='Advanced Decorators', lecture_url='https://www.youtube.com/watch?v=MjHpMCIvwsY', week_id=6),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=6),
        # Week 1, Course 3
        Lecture(title='Introduction to Numpy', lecture_url='https://www.youtube.com/watch?v=8yZMXCaFshs', week_id=7),
        Lecture(title='Pandas Basics', lecture_url='https://www.youtube.com/watch?v=dcqPhpY7tWk', week_id=7),
        Lecture(title='Data Visualization with Matplotlib', lecture_url='https://www.youtube.com/watch?v=3Xc3CA655Y4', week_id=7),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=7),
        # Week 2, Course 3
        Lecture(title='Advanced Pandas', lecture_url='https://www.youtube.com/watch?v=5JnMutdy6Fw', week_id=8),
        Lecture(title='Scikit-learn for Machine Learning', lecture_url='https://www.youtube.com/watch?v=0Lt9w-BxKFQ', week_id=8),
        Lecture(title='Deep Learning with TensorFlow', lecture_url='https://www.youtube.com/watch?v=tPYj3fFJGjk', week_id=8),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=8),
        # Week 3, Course 3
        Lecture(title='Natural Language Processing', lecture_url='https://www.youtube.com/watch?v=8vwoGXzHwDk', week_id=9),
        Lecture(title='Time Series Analysis', lecture_url='https://www.youtube.com/watch?v=wp0vBnN0k3s', week_id=9),
        Lecture(title='Model Deployment', lecture_url='https://www.youtube.com/watch?v=cchIa2SU69U', week_id=9),
        Lecture(title='Graded Programming Assignment', lecture_url='', week_id=9)
    ]

    db.session.add_all(lectures)
    db.session.commit()

    # Add coding questions to each week
    coding_questions = [
        # Week 1, Course 1
        CodingQuestion(content='Write a Python function to reverse a string.', test_cases='[{"input": "hello", "output": "olleh"}, {"input": "world", "output": "dlrow"}]', solution='def reverse_string(s): return s[::-1]', week_id=1),
        CodingQuestion(content='Write a Python function to check if a number is prime.', test_cases='[{"input": "5", "output": "True"}, {"input": "4", "output": "False"}]', solution='def is_prime(n): return all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))', week_id=1),
        # Week 2, Course 1
        CodingQuestion(content='Write a Python function to find the factorial of a number.', test_cases='[{"input": "5", "output": "120"}, {"input": "3", "output": "6"}]', solution='def factorial(n): return 1 if n == 0 else n * factorial(n-1)', week_id=2),
        CodingQuestion(content='Write a Python function to find the nth Fibonacci number.', test_cases='[{"input": "5", "output": "5"}, {"input": "7", "output": "13"}]', solution='def fibonacci(n): a, b = 0, 1\n for _ in range(n): a, b = b, a + b\n return a', week_id=2),
        # Week 3, Course 1
        CodingQuestion(content='Write a Python function to find the GCD of two numbers.', test_cases='[{"input": "8, 12", "output": "4"}, {"input": "14, 21", "output": "7"}]', solution='def gcd(a, b): while b: a, b = b, a % b\n return a', week_id=3),
        CodingQuestion(content='Write a Python function to find the LCM of two numbers.', test_cases='[{"input": "4, 6", "output": "12"}, {"input": "5, 3", "output": "15"}]', solution='def lcm(a, b): return abs(a*b) // gcd(a, b)', week_id=3),
        # Week 1, Course 2
        CodingQuestion(content='Write a Python function to flatten a nested list.', test_cases='[{"input": "[[1, 2, [3]], 4]", "output": "[1, 2, 3, 4]"}, {"input": "[[1], 2, [[3], [4, [5]]]]", "output": "[1, 2, 3, 4, 5]"}]', solution='def flatten(lst):\n for item in lst:\n if isinstance(item, list):\n yield from flatten(item)\n else:\n yield item', week_id=4),
        CodingQuestion(content='Write a Python function to compute the power set of a set.', test_cases='[{"input": "{1, 2, 3}", "output": "[[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]"}]', solution='from itertools import chain, combinations\n def power_set(s):\n return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))', week_id=4),
        # Week 2, Course 2
        CodingQuestion(content='Write a Python function to compute the transpose of a matrix.', test_cases='[{"input": "[[1, 2, 3], [4, 5, 6]]", "output": "[[1, 4], [2, 5], [3, 6]]"}]', solution='def transpose(matrix):\n return [list(row) for row in zip(*matrix)]', week_id=5),
        CodingQuestion(content='Write a Python function to compute the determinant of a matrix.', test_cases='[{"input": "[[1, 2], [3, 4]]", "output": "-2"}]', solution='def determinant(matrix):\n if len(matrix) == 2:\n return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]\n # Recursive case for larger matrices', week_id=5),
        # Week 3, Course 2
        CodingQuestion(content='Write a Python function to compute the inverse of a matrix.', test_cases='[{"input": "[[1, 2], [3, 4]]", "output": "[[-2.0, 1.0], [1.5, -0.5]]"}]', solution='import numpy as np\n def inverse(matrix):\n return np.linalg.inv(matrix).tolist()', week_id=6),
        CodingQuestion(content='Write a Python function to compute the eigenvalues of a matrix.', test_cases='[{"input": "[[1, 2], [2, 1]]", "output": "[3.0, -1.0]"}]', solution='import numpy as np\n def eigenvalues(matrix):\n return np.linalg.eigvals(matrix).tolist()', week_id=6),
        # Week 1, Course 3
        CodingQuestion(content='Write a Python function to normalize a vector.', test_cases='[{"input": "[1, 2, 3]", "output": "[0.267, 0.534, 0.802]"}]', solution='import numpy as np\n def normalize(vector):\n norm = np.linalg.norm(vector)\n return (vector / norm).tolist()', week_id=7),
        CodingQuestion(content='Write a Python function to compute the dot product of two vectors.', test_cases='[{"input": "[1, 2, 3], [4, 5, 6]", "output": "32"}]', solution='import numpy as np\n def dot_product(a, b):\n return np.dot(a, b)', week_id=7),
        # Week 2, Course 3
        CodingQuestion(content='Write a Python function to compute the mean squared error between two vectors.', test_cases='[{"input": "[1, 2, 3], [4, 5, 6]", "output": "27.0"}]', solution='import numpy as np\n def mse(a, b):\n return np.mean((np.array(a) - np.array(b)) ** 2)', week_id=8),
        CodingQuestion(content='Write a Python function to compute the gradient of a quadratic function.', test_cases='[{"input": "3x^2 + 4x + 5", "output": "[6x + 4]"}]', solution='import sympy as sp\n def gradient(func):\n x = sp.symbols("x")\n return sp.diff(func, x)', week_id=8),
        # Week 3, Course 3
        CodingQuestion(content='Write a Python function to compute the Fourier transform of a signal.', test_cases='[{"input": "[1, 2, 3, 4]", "output": "[10.0, -2.0+2.0j, -2.0, -2.0-2.0j]"}]', solution='import numpy as np\n def fourier_transform(signal):\n return np.fft.fft(signal).tolist()', week_id=9),
        CodingQuestion(content='Write a Python function to compute the convolution of two signals.', test_cases='[{"input": "[1, 2, 3], [0, 1, 0.5]", "output": "[0.0, 1.0, 2.5, 4.0, 1.5]"}]', solution='import numpy as np\n def convolution(a, b):\n return np.convolve(a, b).tolist()', week_id=9)
    ]

    db.session.add_all(coding_questions)
    db.session.commit()

    print('Dummy data added successfully!')
