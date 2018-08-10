import setuptools
from info import info

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-translations",
    version=info.RELEASE,
    description="A Django app which provides support for model translation.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url=info.SOURCE,
    author=info.AUTHOR,
    author_email=info.EMAIL,
    classifiers=[
        "Development Status :: " + info.DEV_STATUS,
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Internationalization",
    ],
    keywords="django internationalization",
    project_urls={
        "Documentation": info.DOCS,
        "Funding": info.FUND,
        "Source": info.SOURCE,
        "Tracker": info.TRACKER,
    },
    packages=setuptools.find_packages(exclude=["docs", "example"]),
    python_requires=">=3.5, <4",
)
