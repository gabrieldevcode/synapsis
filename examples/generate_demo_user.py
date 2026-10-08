"""Creates a demo user so you can try Synapsis without signing up.

Synapsis stores each student's data in `users/`, a folder ignored by git, so
a freshly cloned repository has no content to review and the ranking shows up
empty. This script fills that gap: it builds a fictional user with four
subjects already registered, each one with a different date added, so the
priority ranking has something to sort on the very first login.

Usage, from the repository root:

    python examples/generate_demo_user.py

Then run `python synapsis.py`, choose "1. Login" and sign in with:

    username: demo
    password: demo123

The data is made up. No real student information ships with the project.
"""

import datetime
import os

NAME = 'demo'
PASSWORD = 'demo123'
COEFFICIENT = 6.700  # equivalent to answering the questionnaire with middling scores


# Each entry describes a subject: how many hours ago it was registered, the
# computed difficulty, the summary, the quiz and the attachments.
#
# The hours vary on purpose (2h to 15 days) to cover several of the time bands
# the ranking uses. The file paths are fictional: they show the format and do
# not point to anything that exists.
STUDIES = [
    {
        'name': 'Conditional Statements',
        'hours_ago': 2,
        'difficulty': 8.4,
        'summary': (
            'if/elif/else, comparison operators and chaining conditions. '
            'Watch out for using = instead of == inside an if.'
        ),
        'quiz': [
            ['Which operator compares equality in Python?', '=='],
            ['Is the else block required after an if?', 'no'],
        ],
        'files': ['materials/cs1/lecture03_conditionals.pdf'],
        'videos': ['https://example.invalid/lesson-conditionals'],
    },
    {
        'name': 'Loops',
        'hours_ago': 20,
        'difficulty': 6.1,
        'summary': (
            'while runs as long as the condition is true; for walks an '
            'iterable. enumerate returns the index and the value at once.'
        ),
        'quiz': [
            ['Which function returns index and value during a for loop?', 'enumerate'],
            ['Which statement stops a loop immediately?', 'break'],
        ],
        'files': ['materials/cs1/lecture05_loops.pdf'],
        'videos': [],
    },
    {
        'name': 'File Handling',
        'hours_ago': 75,
        'difficulty': 4.3,
        'summary': (
            'open() with the r, w and a modes. with closes the file on its own, '
            'even when an exception happens halfway through writing.'
        ),
        'quiz': [
            ['Which open mode erases the previous content of the file?', 'w'],
            ['Which method reads every line and returns a list?', 'readlines'],
        ],
        'files': [],
        'videos': ['https://example.invalid/lesson-files'],
    },
    {
        'name': 'Recursion',
        'hours_ago': 360,  # 15 days, falls in the last time band
        'difficulty': 2.8,
        'summary': (
            'Every recursive function needs a base case, otherwise the call '
            'stack overflows. Classic examples: factorial and Fibonacci.'
        ),
        'quiz': [
            ['What is the condition that ends the recursion called?', 'base case'],
            ['Which error does Python raise without a base case?', 'RecursionError'],
        ],
        'files': [],
        'videos': [],
    },
]


def write_study(studies_folder, study):
    """Writes one piece of content in the same format `register_content` produces.

    `open` is called without `encoding=` on purpose. Synapsis does not set an
    encoding when writing or reading either, so both use the platform default
    (cp1252 on Windows, UTF-8 on Linux). Forcing UTF-8 here would make accented
    characters show up garbled on the program's screen on Windows.
    """
    registered_at = datetime.datetime.now() - datetime.timedelta(hours=study['hours_ago'])
    timestamp = registered_at.strftime('%d/%m/%Y %H:%M')

    file_name = f"{study['name'].replace(' ', '_')}.txt"
    path = os.path.join(studies_folder, file_name)

    with open(path, 'w') as f:
        f.write(f"Content: {study['name']}\n")
        f.write(f"Difficulty: {study['difficulty']}\n")
        f.write(f"Date Added: {timestamp}\n")
        f.write(f"Summary: {study['summary']}\n")
        f.write('-' * 20 + '\n')
        f.write('QUIZ:\n')
        for item in study['quiz']:
            f.write(f'{item}\n')
        f.write('-' * 20 + '\n')
        f.write('FILES:\n')
        for file in study['files']:
            f.write(f'{file}\n')
        f.write('-' * 20 + '\n')
        f.write('VIDEO LESSONS:\n')
        for video in study['videos']:
            f.write(f'{video}\n')

    return path


def main():
    user_folder = os.path.join('users', NAME)
    studies_folder = os.path.join(user_folder, 'studies')
    os.makedirs(studies_folder, exist_ok=True)

    profile_path = os.path.join(user_folder, f'profile_{NAME}.txt')
    with open(profile_path, 'w') as f:
        f.write(f'{NAME}\n')
        f.write(f'{PASSWORD}\n')
        f.write(f'{COEFFICIENT:.3f}\n')
        f.write('0\n')

    print(f'Profile created: {profile_path}')
    for study in STUDIES:
        print(f'Study created:   {write_study(studies_folder, study)}')

    print()
    print(f'Done. Run `python synapsis.py`, choose "1. Login" and sign in with')
    print(f'username "{NAME}" and password "{PASSWORD}".')


if __name__ == '__main__':
    main()
