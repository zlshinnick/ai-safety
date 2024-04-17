from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='ai-safety',
    version='0.0.1', 
    description='AI Safety: Toolkit for integrating safety measures into AI systems.',
    long_description="""
        AI Safety is an open-source toolkit designed to integrate safety measures into AI systems. 
        It offers functionalities for generating and evaluating responses, and checking for violations against user defined rules.
    """,
    author='Max Twelftree', 
    author_email='maxjtwelftree@gmail.com', 
    url='https://github.com/zlshinnick/ai-safety', 
    license='MIT', 
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'dev': [
            'pytest>=6.2.5',
        ],
    },
    classifiers=[
        # See https://pypi.org/classifiers/ for a full list
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
