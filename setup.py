from distutils.core import setup

setup(
    name='scintilla',
    version='0.0.1',
    packages=['scintilla'],
    url='https://github.com/goncaloccastro/scintilla',
    license='MIT',
    author='Gonçalo Castro',
    author_email='goncaloccastro@gmail.com',
    description='Scintilla - Generate DataFrame for property based testing',
    python_requires='>=3.7',
    install_requires=[
        'Faker==8.14.0'
        'pyspark==3.0.1'
        'prettytable==3.1.1'
    ]
)
