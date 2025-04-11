from setuptools import setup, find_packages

setup(
    name="gmail-sender",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyYAML>=5.4.1",
        "google-api-python-client>=2.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=0.4.6",
    ],
    python_requires=">=3.6",
    author="xuanlingzi",
    author_email="xuanlingzi@gmail.com",
    description="A tool for sending personalized emails to multiple recipients",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xuanlingzi/gmail-sender",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
