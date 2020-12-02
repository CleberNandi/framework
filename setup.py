from setuptools import setup, find_packages


setup(
    name='my_lib',
    version='0.1.0',
    description='my_lib is directory of lib full to use in projects',
    # url='https://github.com/hudsonbrendon/calculator',
    author='Cleber Goulart Nandi',
    author_email='cleber.nandi@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    # install_requires=[],
    zip_safe=False
)