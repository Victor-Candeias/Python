from setuptools import setup, find_packages

setup(
    name='SerialPortService',
    version='1.0.0',
    description='A Windows service that manages virtual serial ports and handles communication with a real serial port.',
    author='Victor Candeias',
    author_email='victor.s.candeias@ctt.pt',
    url='https://github.com/Victor-Candeias/Python/serial-port-service',  # Replace with your project URL
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'pywin32',
        'pyserial',
    ],
    entry_points={
        'console_scripts': [
            'serial-port-service = src.serial_port_service:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: System :: Networking',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    python_requires='>=3.8',
)
