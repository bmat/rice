from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='rice',
    packages=['rice'],
    version='0.4',
    description='Non intrusive serialization library',
    author='BMAT developers',
    author_email='tv-av@bmat.com',
    url='https://github.com/bmat/rice',
    download_url='https://github.com/bmat/rice/archive/master.zip',
    keywords=['rice', 'serialization', 'deserialization', 'doc'],
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System',
                 'Topic :: Utilities'],
    install_requires=install_requires
)
