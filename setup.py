from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "Adult-income-prediction-MLFlow"
AUTHOR_USER_NAME = "siddmodi"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author='Siddharth',
    description="Adult income classification prediction",

    long_description='''
                        Fill the mentioned details and get the sales of your described items
                        on your described outlet in Rs :,	
                    ''',

    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="siddharthmodi39101@gmail.com",
    packages=[SRC_REPO],
    license="",
    python_requires=">=3.6",
    install_requires=LIST_OF_REQUIREMENTS
    )