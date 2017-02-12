from setuptools import setup

requires = [
    'pyramid',
    'pyramid_chameleon',
    'bcrypt',
    'sqlalchemy',
    'pyramid_tm',
    'zope.sqlalchemy',
    'requests',
    'pyramid_debugtoolbar'
]

setup(name='dragonia',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = dragonia:main
      """,
)