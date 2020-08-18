from setuptools import setup, find_packages

setup(
  name='benchgen',
  version='1.0.0',
  author='Refactr',
  packages=find_packages(),
  scripts=[

  ],
  install_requires=[
    'lxml',
    'jinja2'
  ],
  zip_safe=True,
  entry_points={
    'console_scripts': [
      'benchgen = benchgen.__main__:main'
    ]
  }
)