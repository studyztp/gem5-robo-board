from typing import Optional

from m5.objects import (
    BaseCPU,
    BaseMMU,
    Port,
    Process,
)
from m5.objects.ArmCPU import ArmMinorCPU
from m5.objects.BaseMinorCPU import *

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.utils.requires import requires


class CortexM4Core(ArmMinorCPU):
    def __init__(self, if_fpu: bool) -> None:
        super().__init__()
        self._if_fpu = if_fpu

        # M4 does not support SMT
        self.threadPolicy = "SingleThreaded"

        # Backward cycle delay from Fetch2 to Fetch1 for branch prediction
        # signalling (0 means in the same cycle, 1 mean the next cycle)
        self.fetch1ToFetch2BackwardDelay = 0
        # Size of input buffer to Fetch2 in cycles-worth of insts
        self.fetch2InputBufferSize = 1
        # Size of input buffer to Decode in cycles-worth of insts
        self.decodeInputBufferSize = 1
        # Width (in instructions) of input to Decode (and implicitly Decode's
        # own width)
        self.decodeInputWidth = 1


class CortexM4CPU(BaseCPUCore):
    def __init__(self, if_fpu: bool):
        cpu = CortexM4Core(if_fpu=if_fpu)
        super().__init__(core=cpu, isa=ISA.ARM)


class CortexM4Processor(BaseCPUProcessor):
    def __init__(self, num_cores: int, if_fpu: bool):
        cores = [CortexM4CPU(if_fpu=if_fpu) for _ in range(num_cores)]
        super().__init__(cores=cores)
