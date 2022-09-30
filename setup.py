# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

from pathlib import Path
long_description = (Path(__file__).parent / "README.md").read_text()

##
## TODO: Rename the package names (and the name of the whole library)
##
setup(name='pash-annotations',
      version='0.2',
      py_modules=['pash_annotations.util_flag_option',
                  'pash_annotations.util_new',
                  'pash_annotations.util_standard',
                  'pash_annotations.annotation_cli'],
      packages=['pash_annotations',
                'pash_annotations.annotation_generation',
                'pash_annotations.annotation_generation.annotation_generators',
                'pash_annotations.annotation_generation.datatypes',
                'pash_annotations.annotation_generation.datatypes.parallelizability',
                'pash_annotations.config',
                'pash_annotations.datatypes',
                'pash_annotations.parser'],
      package_data={'pash_annotations': ['parser/command_flag_option_info/data/*.json']},
      ## Necessary for the markdown to be properly rendered
      long_description=long_description,
      long_description_content_type="text/markdown",
      python_requires='>=3.8',
      include_package_data=True,
      )
