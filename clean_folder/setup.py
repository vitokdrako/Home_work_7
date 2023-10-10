from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder=clean_folder.clean:main'
        ],
    },
    install_requires=[],
    author="Vitokdrako",
    author_email="vitokdrako@gmail.com",
    description="Organaizer.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vitokdrako/Home_work_7.git", 
)
