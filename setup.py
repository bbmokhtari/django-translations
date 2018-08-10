import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-translations",
    version='0.0.0',
    author="Behzad B. Mokhtari",
    description="A Django app which provides support for model translation.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/perplexionist/django-translations",
    packages=['translations'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
