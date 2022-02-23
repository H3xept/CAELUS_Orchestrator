from setuptools import setup, find_packages

setup(
   name='OrchestratorSDK',
   version='1.0',
   description='Communicate with the CAELUS orchestrator',
   author='Leonardo Cascianelli',
   author_email='me.leonardocascianelli@gmail.com',
   packages=find_packages(),
   install_requires=['wheel'],
)