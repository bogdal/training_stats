try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'training_stats',
    'packages': ['training_stats'],
    'version': '0.2.0',
    'description': 'Training Stats',
    'author': 'Jakub Draganek',
    'author_email': 'jakub.draganek@gmail.com',
    'url': 'https://github.com/salwator/training_stats',
    'python_requires': '>=3.4',
    'install_requires': ['numpy'],
    'scripts': [],
}

setup(**config)
