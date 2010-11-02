from setuptools import setup
setup(name='Ska.report_ranges',
      author = 'Jean Connelly',
      description='Time Range manipulation for report generation',
      author_email = 'jconnelly@cfa.harvard.edu',
      py_modules = ['Ska.report_ranges'],
      url = 'http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.report_ranges.html',
      test_suite = 'nose.collector',
      version='0.01',
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
