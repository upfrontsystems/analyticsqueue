from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='upfront.analyticsqueue',
      version=version,
      description="Upfront Analytics Queue",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Upfront Systems',
      author_email='rijk@upfrontsystems.co.za',
      url='git@github.com:upfrontsystems/analyticsqueue.git',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upfront'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pyga',
          'redis',
          'rq',
          'rq-dashboard',
          # -*- Extra requirements: -*-
      ],
      tests_require=[
          'mock_http',
      ],
      extras_require={
          'test': [
              'mock_http',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      processqueue=upfrontsystems.q.scripts.queueprocessor:processqueue
      rqinfo=upfrontsystems.q.scripts.rqinfo:main
      rqdashboard=rq_dashboard.scripts.rq_dashboard:main
      """,
      )
