# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup

from ska_helpers.setup_helper import duplicate_package_info

name = "ska_report_ranges"
namespace = "Ska.report_ranges"

packages = ["ska_report_ranges"]
package_dir = {name: name}

duplicate_package_info(packages, name, namespace)
duplicate_package_info(package_dir, name, namespace)

setup(name=name,
      author='Jean Connelly',
      description='Time Range manipulation for report generation',
      author_email='jconnelly@cfa.harvard.edu',
      url='http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.report_ranges.html',
      use_scm_version=True,
      zip_safe=False,
      packages=packages,
      package_dir=package_dir,
      )
