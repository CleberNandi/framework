from setuptools import setup, find_packages


setup(
    name='framework',
    version='0.1.0',
    description='framework is directory of lib full to use in projects',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pyad"],
    zip_safe=False
)