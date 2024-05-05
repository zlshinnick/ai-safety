from setuptools import setup, find_packages

setup(
    name='ai-safety',
    version='0.1',
    packages=find_packages(),
    description='Open source screening software enhancing safety in large language models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zach Shinnick',
    author_email='Zachshinnick03@outlook.com',
    url='https://github.com/zlshinnick/ai-safety.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)