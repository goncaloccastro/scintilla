from distutils.core import setup

setup(
    name='scintilla',
    version='0.0.3',
    packages=['scintilla'],
    url='https://github.com/goncaloccastro/scintilla',
    license='MIT',
    author='Gonçalo Castro',
    author_email='goncaloccastro@gmail.com',
    description='Scintilla - Generate DataFrames for property based testing',
    python_requires='>=3.7',
    install_requires=[
        'Faker==8.14.0',
        'pyspark==3.0.1',
        'prettytable==3.1.1',
    ]
)
