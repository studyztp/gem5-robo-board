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

def Unsure() -> list[MinorFU]:
    FloatAdd = FPMaker(["FloatAdd"], 1, "FloatAdd", 2, 0)
    FloatCmp = FPMaker(["FloatCmp"], 1, "FloatCmp", 2, 0)
    FloatCvt = FPMaker(["FloatCvt"], 1, "FloatCvt", 2, 0)
    FloatMult = FPMaker(["FloatMult"], 1, "FloatMult", 2, 0)
    FloatMultAcc = FPMaker(["FloatMultAcc"], 3, "FloatMultAcc", 2, 0)
    FloatDiv = FPMaker(["FloatDiv"], 14, "FloatDiv", 2, 0)
    FloatMisc = FPMaker(["FloatMisc"], 1, "FloatMisc", 2, 0)
    FloatSqrt = FPMaker(["FloatSqrt"], 14, "FloatSqrt", 2, 0)
    SimdAdd = FPMaker(["SimdAdd"], 1, "SimdAdd", 2, 0)
    SimdAddAcc = FPMaker(["SimdAddAcc"], 1, "SimdAddAcc", 2, 0)
    SimdCmp = FPMaker(["SimdCmp"], 1, "SimdCmp", 2, 0)
    SimdCvt = FPMaker(["SimdCvt"], 1, "SimdCvt", 2, 0)
    SimdMisc = FPMaker(["SimdMisc"], 1, "SimdMisc", 2, 0)
    SimdMult = FPMaker(["SimdMult"], 1, "SimdMult", 2, 0)
    SimdMatMultAcc = FPMaker(["SimdMatMultAcc"], 1, "SimdMatMultAcc", 2, 0)
    SimdShift = FPMaker(["SimdShift"], 1, "SimdShift", 2, 0)            
    SimdShiftAcc = FPMaker(["SimdShiftAcc"], 1, "SimdShiftAcc", 2, 0)
    SimdDiv = FPMaker(["SimdDiv"], 14, "SimdDiv", 2, 0)
    SimdSqrt = FPMaker(["SimdSqrt"], 14, "SimdSqrt", 2, 0)
    SimdFloatAlu = FPMaker(["SimdFloatAlu"], 1, "SimdFloatAlu", 2, 0)
    SimdFloatMatMultAcc = FPMaker(["SimdFloatMatMultAcc"], 1, "SimdFloatMatMultAcc", 2, 0)
    SimdReduceAdd = FPMaker(["SimdReduceAdd"], 1, "SimdReduceAdd", 2, 0)
    SimdReduceAlu = FPMaker(["SimdReduceAlu"], 1, "SimdReduceAlu", 2, 0)
    SimdReduceCmp = FPMaker(["SimdReduceCmp"], 1, "SimdReduceCmp", 2, 0)
    SimdFloatReduceAdd = FPMaker(["SimdFloatReduceAdd"], 1, "SimdFloatReduceAdd", 2, 0)
    SimdFloatReduceCmp = FPMaker(["SimdFloatReduceCmp"], 1, "SimdFloatReduceCmp", 2, 0)
    SimdAes = FPMaker(["SimdAes"], 1, "SimdAes", 2, 0)
    SimdAesMix = FPMaker(["SimdAesMix"], 1, "SimdAesMix", 2, 0)
    SimdSha1Hash = FPMaker(["SimdSha1Hash"], 1, "SimdSha1Hash", 2, 0)
    SimdSha1Hash2 = FPMaker(["SimdSha1Hash2"], 1, "SimdSha1Hash2", 2, 0)
    SimdSha256Hash = FPMaker(["SimdSha256Hash"], 1, "SimdSha256Hash", 2, 0)
    SimdSha256Hash2 = FPMaker(["SimdSha256Hash2"], 1, "SimdSha256Hash2", 2, 0)
    SimdShaSigma2 = FPMaker(["SimdShaSigma2"], 1, "SimdShaSigma2", 2, 0) 
    SimdShaSigma3 = FPMaker(["SimdShaSigma3"], 1, "SimdShaSigma3", 2, 0)
    SimdPredAlu = FPMaker(["SimdPredAlu"], 1, "SimdPredAlu", 2, 0)
    Matrix = FPMaker(["Matrix"], 1, "Matrix", 2, 0)
    MatrixMov = FPMaker(["MatrixMov"], 1, "MatrixMov", 2, 0)
    MatrixOP = FPMaker(["MatrixOP"], 1, "MatrixOP", 2, 0)
    MemRead = FPMaker(["MemRead"], 1, "MemRead", 2, 0)
    MemWrite = FPMaker(["MemWrite"], 1, "MemWrite", 2, 0)
    IprAccess = FPMaker(["IprAccess"], 1, "IprAccess", 2, 0)
    InstPrefetch = FPMaker(["InstPrefetch"], 1, "InstPrefetch", 2, 0)
    SimdUnitStrideLoad = FPMaker(
        ["SimdUnitStrideLoad"], 1, "SimdUnitStrideLoad", 2, 0
    )
    SimdUnitStrideStore = FPMaker(
        ["SimdUnitStrideStore"], 1, "SimdUnitStrideStore", 2, 0
    )
    SimdUnitStrideMaskLoad = FPMaker(
        ["SimdUnitStrideMaskLoad"], 1, "SimdUnitStrideMaskLoad", 2, 0
    )
    SimdUnitStrideMaskStore = FPMaker(
        ["SimdUnitStrideMaskStore"], 1, "SimdUnitStrideMaskStore", 2, 0
    )
    SimdStridedLoad = FPMaker(
        ["SimdStridedLoad"], 1, "SimdStridedLoad", 2, 0
    )
    SimdStridedStore = FPMaker(
        ["SimdStridedStore"], 1, "SimdStridedStore", 2, 0
    )
    SimdIndexedLoad = FPMaker(
        ["SimdIndexedLoad"], 1, "SimdIndexedLoad", 2, 0
    )
    SimdIndexedStore = FPMaker(
        ["SimdIndexedStore"], 1, "SimdIndexedStore", 2, 0
    )
    SimdWholeRegisterLoad = FPMaker(
        ["SimdWholeRegisterLoad"], 1, "SimdWholeRegisterLoad", 2, 0
    )
    SimdWholeRegisterStore = FPMaker(
        ["SimdWholeRegisterStore"], 1, "SimdWholeRegisterStore", 2, 0
    )
    SimdUnitStrideFaultOnlyFirstLoad = FPMaker(
        ["SimdUnitStrideFaultOnlyFirstLoad"], 1, 
        "SimdUnitStrideFaultOnlyFirstLoad", 2, 0
    )
    SimdUnitStrideSegmentedLoad = FPMaker(
        ["SimdUnitStrideSegmentedLoad"], 1, "SimdUnitStrideSegmentedLoad", 2, 0
    )
    SimdUnitStrideSegmentedStore = FPMaker(
        ["SimdUnitStrideSegmentedStore"], 1, "SimdUnitStrideSegmentedStore", 2,
        0
    )
    SimdUnitStrideSegmentedFaultOnlyFirstLoad = FPMaker(
        ["SimdUnitStrideSegmentedFaultOnlyFirstLoad"], 1,
        "SimdUnitStrideSegmentedFaultOnlyFirstLoad", 2, 0
    )
    SimdStrideSegmentedLoad = FPMaker(
        ["SimdStrideSegmentedLoad"], 1, "SimdStrideSegmentedLoad", 2, 0
    )
    SimdStrideSegmentedStore = FPMaker(
        ["SimdStrideSegmentedStore"], 1, "SimdStrideSegmentedStore", 2, 0
    )
    SimdExt = FPMaker(["SimdExt"], 1, "SimdExt", 2, 0)
    SimdFloatExt = FPMaker(["SimdFloatExt"], 1, "SimdFloatExt", 2, 0)
    SimdConfig = FPMaker(["SimdConfig"], 1, "SimdConfig", 2, 0)
    #SimdBf16Cvt = FPMaker(["SimdBf16Cvt"], 1, "SimdBf16Cvt", 2, 0) 
    #SimdBf16DotProd = FPMaker(["SimdBf16DotProd"], 1, "SimdBf16DotProd", 2, 0)
    #SimdBf16MatMultAcc = FPMaker(
    #    ["SimdBf16MatMultAcc"], 1, "SimdBf16MatMultAcc", 2, 0)
    #SimdBf16MultAcc = FPMaker(
    #    ["SimdBf16MultAcc"], 1, "SimdBf16MultAcc", 2, 0)
    #Bf16Cvt = FPMaker(
    #    ["Bf16Cvt"], 1, "Bf16Cvt", 2, 0)
    return [
        FloatAdd,
        FloatCmp,
        FloatCvt,
        FloatMult,
        FloatMultAcc,
        FloatDiv,
        FloatMisc,
        FloatSqrt,
        SimdAdd,
        SimdAddAcc,
        SimdCmp,
        SimdCvt,
        SimdMisc,
        SimdMult,
        SimdMatMultAcc,
        SimdShift,
        SimdShiftAcc,
        SimdDiv,
        SimdSqrt,
        SimdFloatAlu,
        SimdFloatMatMultAcc,
        SimdReduceAdd,
        SimdReduceAlu,
        SimdReduceCmp,
        SimdFloatReduceAdd,
        SimdFloatReduceCmp,
        SimdAes,
        SimdAesMix,
        SimdSha1Hash,
        SimdSha1Hash2,
        SimdSha256Hash,
        SimdSha256Hash2,
        SimdShaSigma2,
        SimdShaSigma3,
        SimdPredAlu,
        Matrix,
        MatrixMov,
        MatrixOP,
        MemRead,
        MemWrite,
        IprAccess,
        InstPrefetch,
        SimdUnitStrideLoad,
        SimdUnitStrideStore,
        SimdUnitStrideMaskLoad,
        SimdUnitStrideMaskStore,
        SimdStridedLoad,
        SimdStridedStore,
        SimdIndexedLoad,
        SimdIndexedStore,
        SimdWholeRegisterLoad,
        SimdWholeRegisterStore,
        SimdUnitStrideFaultOnlyFirstLoad,
        SimdUnitStrideSegmentedLoad,
        SimdUnitStrideSegmentedStore,
        SimdUnitStrideSegmentedFaultOnlyFirstLoad,
        SimdStrideSegmentedLoad,
        SimdStrideSegmentedStore,
        SimdExt,
        SimdFloatExt,
        SimdConfig,
       # SimdBf16Cvt,
       # SimdBf16DotProd,
       # SimdBf16MatMultAcc,
       # SimdBf16MultAcc,
       # Bf16Cvt
    ]

class CortexM4Core(ArmMinorCPU):
    def __init__(self, if_fpu: bool) -> None:
        super().__init__()
        self._if_fpu = if_fpu

        # M4 does not support SMT
        self.threadPolicy = "SingleThreaded"

        # The instruction line in STM32G4 is 8 bytes (64 bits)
        self.fetch1LineSnapWidth = 8
        self.fetch1LineWidth = 8

        # Trying to merge the fetch1 and fetch2 stage into one stage
        self.fetch1ToFetch2ForwardDelay = 1
        # Backward cycle delay from Fetch2 to Fetch1 for branch prediction
        # signalling (0 means in the same cycle, 1 mean the next cycle)
        self.fetch1ToFetch2BackwardDelay = 1
        # Size of input buffer to Fetch2 in cycles-worth of insts
        self.fetch2InputBufferSize = 1
        # Size of input buffer to Decode in cycles-worth of insts
        self.decodeInputBufferSize = 1
        # Width (in instructions) of input to Decode (and implicitly Decode's
        # own width)
        self.decodeInputWidth = 1
        # No super-scalar execution
        self.executeInputWidth = 1
        self.executeIssueLimit = 1
        self.executeCommitLimit = 1
        self.executeInputBufferSize = 1

        # TODO: Need to loop back to branch predictor later

        self.executeFuncUnits = self._create_fu_pool()

    def _create_fu_pool(self) -> list[MinorFU]:
        _all_fus = []
        if self._if_fpu:
            _all_fus += CortexM4FPUPool()
        _all_fus += CortexM4IntFU()
        _all_fus += Unsure()
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
