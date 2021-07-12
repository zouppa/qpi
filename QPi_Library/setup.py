from setuptools import find_packages, setup
setup(
    name='QPi_lib',
    packages=find_packages(include=['qpi_lib']),
    version='0.2.7',
    description='QPi project',
    author='QPi Team',
    license='MIT',
    install_requires=['qiskit','numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)