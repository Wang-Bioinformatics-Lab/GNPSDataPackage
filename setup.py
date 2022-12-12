import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gnpsdata",
    version="0.0.2",
    author="Mingxun Wang",
    author_email="mwang87@gmail.com",
    description="GNPS Data API Access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage",
    project_urls={
        "Bug Tracker": "https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage/issues",
        "Documentation": "https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["gnpsdata"],
    install_requires=[
        "massql",
        "bs4",
        "requests",
        "networkx",
    ],
    python_requires=">=3.6",
    include_package_data=True
)