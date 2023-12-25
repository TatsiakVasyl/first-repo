from setuptools import setup, find_packages

setup(
    name='clean_folder',
      version='0.0.0.1',
      entry_points={'console_scripts' :['clean-folder=clean_folder.clen:main']
        },
    packages= find_packages(),
    )