import setuptools
import subprocess
import os


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
def main():
    import onaws
    setuptools.setup(
        name="onaws",
        version=onaws.__version__,
        author="Amal Murali",
        author_email="amalmurali47@gmail.com",
        description="Library to fetch the details of assets hosted on AWS.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/amalmurali47/onaws",
        packages=setuptools.find_packages(),
        package_data={"onaws": ["VERSION"]},
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        entry_points={"console_scripts": ["onaws = onaws:__main__.main"]},
        install_requires=[
            "requests >= 2.25.1",
            "pytricia >= 1.0.2"
        ],
    )
    
if __name__ == '__main__':
    main()