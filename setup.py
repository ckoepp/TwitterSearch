from setuptools import setup
import io

#from TwitterSearch import __version__

def readme():
    with io.open('README.rst', 'r', encoding="utf8") as f:
        return f.read()

def requirements():
    req = []
    for line in open('requirements.txt','r'):
        req.append(line.split()[0])
    return req

setup(name='TwitterSearch',
      version='1.0.1',
      description='A library to easily iterate tweets found by the Twitter API',
      long_description=readme(),
      url='http://github.com/ckoepp/TwitterSearch',
      author='Christian Koepp',
      author_email='christian.koepp@tum.de',
      license='MIT',
      packages=['TwitterSearch'],
      keywords='twitter api search',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
      ],
      install_requires=requirements(),
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose>=1.0.0', 'httpretty>=0.8.4,!=0.8.7,!=0.8.8,!=0.8.6']
      )
