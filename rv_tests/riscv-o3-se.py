# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
RISC-V O3CPU SE mode configuration script.

This script runs a RISC-V binary in syscall emulation mode using the
out-of-order CPU model (O3CPU).

Usage:
------
scons build/RISCV/gem5.opt
./build/RISCV/gem5.opt rv_tests/riscv-o3-se.py <binary_path>

Example:
--------
./build/RISCV/gem5.opt rv_tests/riscv-o3-se.py rv_tests/cbo_clean_test.elf
"""

import argparse
import os
import sys

import m5
from m5.objects import *

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Run a RISC-V binary with O3CPU in SE mode"
)
parser.add_argument(
    "binary",
    type=str,
    help="Path to the RISC-V ELF binary to run",
)
parser.add_argument(
    "--cpu-type",
    type=str,
    default="O3CPU",
    choices=["O3CPU", "TimingSimpleCPU", "AtomicSimpleCPU"],
    help="CPU type to use (default: O3CPU)",
)
parser.add_argument(
    "--mem-size",
    type=str,
    default="1GiB",
    help="Memory size (default: 1GiB)",
)
parser.add_argument(
    "--clock",
    type=str,
    default="1GHz",
    help="CPU clock frequency (default: 1GHz)",
)
parser.add_argument(
    "--max-ticks",
    type=int,
    default=0,
    help="Maximum ticks to simulate (0 for unlimited, default: 0)",
)
args = parser.parse_args()

# Check if binary exists
if not os.path.isfile(args.binary):
    print(f"Error: Binary file '{args.binary}' not found")
    sys.exit(1)

# Create system
system = System()

# Setup clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = args.clock
system.clk_domain.voltage_domain = VoltageDomain()

# Memory configuration
system.mem_mode = "timing" if args.cpu_type != "AtomicSimpleCPU" else "atomic"
system.mem_ranges = [AddrRange(args.mem_size)]

# Create CPU based on type
if args.cpu_type == "O3CPU":
    system.cpu = RiscvO3CPU()
elif args.cpu_type == "TimingSimpleCPU":
    system.cpu = RiscvTimingSimpleCPU()
else:
    system.cpu = RiscvAtomicSimpleCPU()

# Create memory bus
system.membus = SystemXBar()

# Create L1 caches (32KB, 4-way set associative)
system.cpu.icache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20,
)
system.cpu.dcache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20,
)

# Connect CPU to caches
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# Connect caches to memory bus
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

# Create interrupt controller
system.cpu.createInterruptController()

# Setup memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR4_2400_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect system port
system.system_port = system.membus.cpu_side_ports

# Setup workload
system.workload = SEWorkload.init_compatible(args.binary)

# Create process
process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

# Create root
root = Root(full_system=False, system=system)

# Instantiate simulation
m5.instantiate()

print(f"Beginning simulation!")
print(f"Binary: {args.binary}")
print(f"CPU Type: {args.cpu_type}")
print(f"Clock: {args.clock}")
print(f"Memory: {args.mem_size}")

# Run simulation
if args.max_ticks > 0:
    exit_event = m5.simulate(args.max_ticks)
else:
    exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
print(f"Exit code: {exit_event.getCode()}")
