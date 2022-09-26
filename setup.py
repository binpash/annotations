# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

from pathlib import Path
long_description = (Path(__file__).parent / "README.md").read_text()

##
## TODO: Rename the package names (and the name of the whole library)
##
setup(name='pash-annotations',
      version='0.1.1',
      py_modules=['util_flag_option',
                  'util_new',
                  'util_standard'],
      packages=['annotation_generation_new',
                'annotation_generation_new.annotation_generators',
                'annotation_generation_new.datatypes',
                'annotation_generation_new.datatypes.parallelizability',
                'command_flag_option_info',
                'config_new',
                'datatypes_new',
                'parser_new'],
      ## Necessary for the markdown to be properly rendered
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires='>=3.8',
    ## TODO: Maybe we can use this?
    #   packages=find_packages(),
    #   package_data={'': ['command_flag_option_info/data/*.json']},
    #   data_files=[('', ['command_flag_option_info/data/*.json'])],
      include_package_data=True,
      ## Actually this is not helpful
      # install_requires=[
      #   "future-annotations ; python_version<'3.7'",
      # ]
      )
