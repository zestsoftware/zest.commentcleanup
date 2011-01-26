from setuptools import setup, find_packages

version = '1.5dev'

setup(name='zest.commentcleanup',
      version=version,
      description="Quickly remove lots of spam comments from your Plone Site",
      long_description=open("README.txt").read() + "\n" +
                       open('CHANGES.txt').read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='spam comments replies',
      author='Maurits van Rees',
      author_email='m.van.rees@zestsoftware.nl',
      url='http://plone.org/products/zest.commentcleanup',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zest'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
