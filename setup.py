
# To setup this package, run "pip install -e ."

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='dictiorm',
      version='0.1',
      description='A tiny MongoDB ORM that takes zero time to setup because docs become simple dicts.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
      ],
      keywords='ORM, MongoDB, dictionary, dictiorm',
      url='https://github.com/bmpenuelas/dictiORM',
      author='Borja Penuelas',
      author_email='borja.penuelas@gmail.com',
      license='MIT',
      packages=['dictiorm'],
      include_package_data=True,
      install_requires=[
      ],
      zip_safe=False)