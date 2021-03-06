from setuptools import setup, find_packages

setup(
    name="flicktor",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['tw = flicktor.__main__:main']
    },
    author='minamorl',
    author_email='minamorl@users.noreply.github.com',
    install_requires=[
        'staccato',
        'clint',
        'python-dateutil',
        'requests',
        'requests-oauthlib',
        'pytz'
    ],
)
