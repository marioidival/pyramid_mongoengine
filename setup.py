# Copyright (c) 2015 Idival, Mario <marioidival@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from setuptools import find_packages, setup


REQUIRES = [
    "pymongo==2.8",
    "mongoengine==0.9.0",
    "pyramid"
]

TEST_REQUIRES = [
    "nose",
    "coverage",
    "webtest"
]

def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="pyramid-mongoengine",
    version="0.0.3",
    description="Mongoengine Pyramid extension based in flask-mongoengine",
    long_description=readme(),
    url="https://github.com/marioidival/pyramid_mongoengine",
    packages=find_packages(),
    include_package_data=True,

    author="Mario Idival",
    author_email="marioidival@gmail.com",
    license="MIT",
    keywords="pyramid mongoengine python os opensource",
    zip_safe=False,

    install_requires=REQUIRES,
    tests_require=TEST_REQUIRES,
    setup_requires=TEST_REQUIRES
)
