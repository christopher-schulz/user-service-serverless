from setuptools import setup, find_packages

setup(name="bookings-api",
      packages=find_packages(exclude=["test"]),
      setup_requires=["pytest-runner"],
      tests_require=["pytest"])
