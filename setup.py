from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in express_tally/__init__.py
from express_tally import __version__ as version

setup(
	name='express_tally',
	version=version,
	description='This application sync data between tally and erpnext using frappe rest api',
	author='Laxman Tandon',
	author_email='laxmantandon@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
