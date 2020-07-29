import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldaphelper-pkg-christian-hawk", # Replace with your own username
    version="0.0.3",
    author="Christian Eland",
    author_email="eland.christian@gmail.com",
    description="Let's make LDAP communication easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christian-hawk/ldaphelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)