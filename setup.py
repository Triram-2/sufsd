from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as file:
        return file.read()

setup(
  name='sufsd',
  version='0.2',
  author='Twir',
  author_email='bobyyy239@gmail.com',
  description='When parsing different sites, you almost always have to copy+paste some functions; this module was created to make such code easier. It includes the most commonly used functions when parsing. In the future it will be very actively replenished.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['selenium_driverless>=1.9.4'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  url='https://github.com/Triram-2/sufsd',
  keywords='utils selenium_driverless',
  python_requires='>=3.8'
)