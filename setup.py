from setuptools import find_packages, setup

from pip.req import parse_requirements


def get_requirements(filename):
    try:
        from pip.download import PipSession

        session = PipSession()
    except ImportError:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


def get_install_requires():
    return get_requirements('requirements.txt')


def get_test_requires():
    return get_requirements('requirements_dev.txt')


setup_args = dict(
    name='voting_wars',
    version='0.1.0',
    packages=find_packages(),
    namespace_packages=['vote'],
    install_requires=get_install_requires(),
    tests_require=get_test_requires(),
    entry_points={
        'console_scripts': [
            'voting-web=vote.scripts.web:main',
        ]
    },
)


if __name__ == '__main__':
    setup(**setup_args)
