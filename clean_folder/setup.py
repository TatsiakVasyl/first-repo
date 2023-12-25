from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.0.0.1',
    url='https://github.com/TatsiakVasyl/first-repo',
    author='Tatsiak Vasyl',
    author_email='tatsyakvasil@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'clean-folder=clean_folder.clean:main',
        ],
    },
    packages=find_packages(),
)