from setuptools import setup, find_packages


setup(
    author="Pavel KÅ™upala",
    author_email='pavel.krupala@gmail.com',
    license="MIT license",
    #long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nodeeditor',
    name='nodeeditor',
    # packages=find_packages(include=['_template']),
    packages=find_packages(
        include=['nodeeditor*'], exclude=['examples*', 'tests*']),
    package_data={'': ['qss/*']},
    version='0.0.1',
    zip_safe=False,
)
