from setuptools import setup, find_packages

setup(
    name="sentientone",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "typing-extensions",
        "dataclasses",
        "numpy",
        "pydantic",
    ],
    extras_require={
        "dev": [
            "pytest",
            "mypy",
            "flake8",
            "black",
        ],
    },
    python_requires=">=3.9",
    author="SentientOne Research",
    author_email="research@sentientone.research",
    description="An Adaptive Intelligent Systems Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YourUsername/SentientOne",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
