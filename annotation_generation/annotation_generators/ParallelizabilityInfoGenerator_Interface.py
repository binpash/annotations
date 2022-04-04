from __future__ import annotations
from typing import List

from abc import ABC, abstractmethod

from Generator_Interface import Generator_Interface
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo


class ParallelizabilityInfoGeneratorInterface(Generator_Interface, ABC):

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, cmd_invocation: CommandInvocation) -> ParallelizabilityInfoGeneratorInterface:
        Generator_Interface.__init__(cmd_invocation)
        self.parallelizability_info: ParallelizabilityInfo = ParallelizabilityInfo()

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> ParallelizabilityInfo:
        return self.parallelizability_info


    ## HELPERS/Library functions: modifying parallelizability info
