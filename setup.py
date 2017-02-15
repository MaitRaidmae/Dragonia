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
      [console_scripts]
      initialize_dragonia_db = dragonia.initialize_db:main
      [paste.app_factory]
      main = dragonia:main
      """,
)