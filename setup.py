import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-translations",
    version="1.0.0a1",
    description="A Django app which provides support for model translation.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/perplexionist/django-translations",
    author="Behzad B. Mokhtari",
    author_email="35877268+perplexionist@users.noreply.github.com",
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Internationalization",
    ),
    keywords="django internationalization",
    project_urls={
        "Documentation": "https://perplexionist.github.io/django-translations",
        "Funding": "https://blockchain.info/address/1FcPBamd6mVrHBNvjB5PqjbnGCBhdY7Rtm",
        "Source": "https://github.com/perplexionist/django-translations",
        "Tracker": "https://github.com/perplexionist/django-translations/issues",
    },
    packages=setuptools.find_packages(exclude=["docs", "example"]),
    python_requires=">=3.5, <4",
)
