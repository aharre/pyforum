from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Feature-Oriented Ranking Utility Metric (FORUM) for evaluating ranking algorithms'
LONG_DESCRIPTION = 'A package that calculates the Feature-Oriented Ranking Utility Metric (FORUM) for evaluating ranking algorithms.'

# Setting up
setup(
        name="pyforum", 
        version=VERSION,
        author="Patrick Gildersleve",
        author_email="<p.gildersleve@lse.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy'],
        keywords=['python', 'ranking algorithms', 'algorithms', 'forum', 'comments', 'news comments'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)