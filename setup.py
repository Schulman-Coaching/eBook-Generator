"""
Setup configuration for the eBook Generator package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI-powered eBook generation using Google's Gemini AI"

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['google-generativeai>=0.3.0']

setup(
    name="ebook-generator",
    version="1.0.0",
    author="Elie Schulman",
    author_email="elie@schulmancoaching.com",
    description="AI-powered eBook generation using Google's Gemini AI",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Schulman-Coaching/eBook-Generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
    },
    entry_points={
        'console_scripts': [
            'ebook-gen=ebook_generator.generator:main',
            'ebook-generator=ebook_generator.generator:main',
        ],
    },
    include_package_data=True,
    package_data={
        'ebook_generator': ['*.md', '*.json'],
    },
    keywords=[
        'ebook', 'generator', 'ai', 'gemini', 'google', 'artificial intelligence',
        'content generation', 'book', 'writing', 'automation', 'markdown', 'epub'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/Schulman-Coaching/eBook-Generator/issues',
        'Source': 'https://github.com/Schulman-Coaching/eBook-Generator',
        'Documentation': 'https://github.com/Schulman-Coaching/eBook-Generator#readme',
    },
)