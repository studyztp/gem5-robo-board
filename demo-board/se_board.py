import argparse
import os
from pathlib import Path

from cores.m4_core import CortexM4Processor

import m5
from m5.objects import (
    AddrRange,
    BadAddr,
    CfiMemory,
    Process,
    Root,
    SEWorkload,
    SimpleMemory,
    SrcClockDomain,
    System,
    SystemXBar,
    VoltageDomain
)

parser = argparse.ArgumentParser(
    description="Run a gem5 simulation with the demo stm32g4 MCU board in SE"
        " mode."
)
parser.add_argument(
    "--binary", type=str, required=True, help="Path to the binary to run"
)
args = parser.parse_args()

binary_path = Path(args.binary)
if not binary_path.is_file():
    raise FileNotFoundError(f"Binary file '{binary_path.as_posix()}' does not "
                            "exist.")

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "100MHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"

# ==== setup the CPU ====
# single core Cortex-M4 with FPU
processor = CortexM4Processor(num_cores=1, if_fpu=True)
system.processor = processor
# ==== end of CPU setup ====

# ==== setup memory ranges ====
# flash memory 512 KBytes
flash_memory = AddrRange("512KiB")
# sram 1 has 80 KBytes
sram1 = AddrRange(start=0x20000000, size="80KiB")
# sram 2 has 16 KBytes
sram2 = AddrRange(start=0x20014000, size="16KiB")
# record memory ranges in system
system.mem_ranges = [flash_memory, sram1, sram2]
# ==== end of memory ranges setup ====

# ==== setup the memory bus ====
# create a memory bus for the system
system.membus = SystemXBar()
# bad address responder so when the CPU accesses an unmapped address, the
# simulation will panic
system.membus.badaddr_responder = BadAddr()
system.membus.default = system.membus.badaddr_responder.pio
# the max. routing table size needs to be set to a higher value for HBM2 stack
system.membus.max_routing_table_size = 2048

# create Flash memory and connect it to the membus
# TODO: the current CfiMemory model does not support timing
system.flash_memory = CfiMemory()
system.flash_memory.range = flash_memory
system.flash_memory.port = system.membus.mem_side_ports

# create SRAM 1 memory and connect it to the membus
system.sram1 = SimpleMemory()
system.sram1.range = sram1
system.sram1.port = system.membus.mem_side_ports

# create SRAM 2 memory and connect it to the membus
system.sram2 = SimpleMemory()
system.sram2.range = sram2
system.sram2.port = system.membus.mem_side_ports

# this part bypasses the cache hierarchy and connects the cores directly to the
# membus
for core in system.processor.get_cores():
    core.connect_icache(system.membus.cpu_side_ports)
    core.connect_dcache(system.membus.cpu_side_ports)
    # because Cortex M-class does not have an MMU, the walker ports are not
    # used. However, we still need to connect them to something, so we connect
    # them to the membus due to the tightly coupled nature of the MinorCPU with
    # the MMU
    core.connect_walker_ports(
        system.membus.cpu_side_ports, system.membus.cpu_side_ports
    )
    core.connect_interrupt()

# set the system port for functional access from the simulator
system.system_port = system.membus.cpu_side_ports

# ==== end of memory bus setup ====

# ==== setup the process ====
# create the process
process = Process()
process.executable = binary_path.as_posix()
process.cmd = [binary_path.as_posix()]

system.workload = SEWorkload.init_compatible(binary_path.as_posix())

# set the process for the core
for core in system.processor.get_cores():
    core.set_workload(process)

# ==== end of process setup ====

# ==== setup the simulation ====
# create the root of the system
root = Root(full_system=False, system=system)
# instantiate the system
m5.instantiate()
# ==== end of simulation setup ====

# ==== start the simulation ====
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
# ==== end of simulation ====
