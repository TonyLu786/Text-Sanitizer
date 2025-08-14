from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text-sanitizer",
    version="1.0.0",
    author="Senior Algorithm Engineer",
    author_email="your-email@example.com",
    description="A multilingual text sanitization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langdetect>=1.0.9",
        "click>=8.1.0",
        "tqdm>=4.64.0",
    ],
    entry_points={
        'console_scripts': [
            'text-sanitizer=src.cli.cli:main',
        ],
    },
)