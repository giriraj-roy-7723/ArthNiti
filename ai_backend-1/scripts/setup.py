from setuptools import setup, find_packages

setup(
    name='ai_backend',
    version='0.1.0',
    description='A backend service for AI applications',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(include=['app', 'app.*']),
    install_requires=[
        # List your project dependencies here
        # e.g., 'numpy', 'pandas', 'fastapi', etc.
    ],
    entry_points={
        'console_scripts': [
            'ai_backend=app.main:main',  # Adjust this if your main function is located elsewhere
        ],
    },
)