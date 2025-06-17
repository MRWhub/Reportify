from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='reportify',
    version='0.0.1',
    license='Apache',
    author='Kevin',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='exemplo@gmail.com',
    keywords='reportify',
    description=u'Trabalho Projeto de Sistemas',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy',
        'networkx',
        'plotly',
        'pydantic',
        'python-dotenv',
        'tqdm', 
    ],
)
