from typing import Optional
from m5.objects import (
    OpClass
)
from m5.objects.ArmCPU import ArmMinorCPU
from m5.objects.BaseMinorCPU import *

from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.utils.requires import requires

def FPMaker(
    _opClasses: list[str], 
    _opLat: int, 
    _timingDescription:str, 
    _srcRegsRelativeLats: int, 
    _extraAssumedLat: int
)-> MinorFU:
    class CustomFU(MinorFU):
        opClasses = minorMakeOpClassSet(_opClasses)
        opLat = _opLat
        timings = [MinorFUTiming(
            description=_timingDescription, 
            srcRegsRelativeLats=_srcRegsRelativeLats,
            extraAssumedLat=_extraAssumedLat
            )
        ]
    return CustomFU()

def CortexM4FPUPool() -> list[MinorFU]:
    # Floating point unit
    # TODO: understand the exact opClasses supported by M4 FPU. Currently, we 
    # allow the following opClasses which cover most of the floating point
    # operations.

    # Number of cycle is found in Cortex-M4 Technical Reference Manual
    # Table 7-1  FPU instruction set.
    # Combine with the Arm ISA in gem5/src/arch/arm/isa/insts/fp.isa, Cortex M4
    # supports the following floating point operations:
    # vabs.f32, vmov, vmrs, vneg
    floatAbs = FPMaker(["SimdFloatMisc"], 1, "SimdFloatMisc", 2, 0)
    # vadd.f32, vsub
    floatAdd = FPMaker(["SimdFloatAdd"], 1, "SimdFloatAdd", 2, 0)
    # vcmp.f32 and vcmpe.f32
    floatCmp = FPMaker(["SimdFloatCmp"], 1, "SimdFloatCmp", 2, 0)
    # vcvt.f32
    floatCvt = FPMaker(["SimdFloatCvt"], 1, "SimdFloatCvt", 2, 0)
    # vdiv.f32
    floatDiv = FPMaker(["SimdFloatDiv"], 14, "SimdFloatDiv", 2, 0)
    # vmul
    floatMul = FPMaker(["SimdFloatMult"], 1, "SimdFloatMult", 2, 0)
    # vmla, vmls, vnmla, vnmls, vfma, vfms, vfnma, vfnms
    floatMla = FPMaker(["SimdFloatMultAcc"], 3, "SimdFloatMultAcc", 2, 0)
    # vsqrt
    floatSqrt = FPMaker(["SimdFloatSqrt"], 14, "SimdFloatSqrt", 2, 0)
    # vldr.32
    floatMemRead = FPMaker(
        ["FloatMemRead"], 2, "FloatMemRead", 2, 0
    )
    # vstr.32
    floatMemWrite = FPMaker(
        ["FloatMemWrite"], 2, "FloatMemWrite", 2, 0 
    )

    # TODO: need to dig more precisely with vldm, vpop, vpush, vstm

    return [
        floatAbs,
        floatAdd,
        floatCmp,
        floatCvt,
        floatDiv,
        floatMul,
        floatMla,
        floatSqrt,
        floatMemRead,
        floatMemWrite,
    ]

def CortexM4IntFU() -> list[MinorFU]:
    # Integer instruction units
    # Number of cycle is found in Cortex-M4 Technical Reference Manual
    # Table 3-1  Cortex-M4 instruction set. 
    intSimple = FPMaker(["IntAlu"], 1, "IntAlu", 1, 0)
    intMul = FPMaker(["IntMult"], 2, "IntMult", 1, 0)
    # TODO: confused on divide instruction so use the original MinorFU setting 
    # first
    intDiv = FPMaker(["IntDiv"], 9, "IntDiv", 0, 0)
    # orn
    simdAlu = FPMaker(["SimdAlu"], 1, "SimdAlu", 2, 0)
    simdMultAcc = FPMaker(["SimdMultAcc"], 1, "SimdMultAcc", 2, 0)

    return [
        intSimple,
        intMul,
        intDiv,
        simdAlu,
        simdMultAcc
    ]


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

        self.executeFuncUnits = self._create_fu_pool()

    def _create_fu_pool(self) -> list[MinorFU]:
        _all_fus = []
        if self._if_fpu:
            _all_fus += CortexM4FPUPool()
        _all_fus += CortexM4IntFU()
        class CortexM4FUPool(MinorFUPool):
            funcUnits = _all_fus
        return CortexM4FUPool()


class CortexM4CPU(BaseCPUCore):
    def __init__(self, if_fpu: bool):
        cpu = CortexM4Core(if_fpu=if_fpu)
        super().__init__(core=cpu, isa=ISA.ARM)


class CortexM4Processor(BaseCPUProcessor):
    def __init__(self, num_cores: int, if_fpu: bool):
        cores = [CortexM4CPU(if_fpu=if_fpu) for _ in range(num_cores)]
        super().__init__(cores=cores)
