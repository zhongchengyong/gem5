# Makefile for RISC-V gem5 SE mode tests
#
# Usage:
#   make              - Build all tests
#   make clean        - Clean build artifacts
#   make run-cbo      - Run cbo_clean_test with gem5
#   make help         - Show this help
#
# Note: start.S is NOT needed for gem5 SE (System Call Emulation) mode.
# gem5 SE mode emulates the Linux ABI and handles program startup/exit
# automatically, so we can use standard GCC linking with the C runtime.

# Cross compiler prefix
CROSS_COMPILE ?= riscv64-unknown-elf-

CC = $(CROSS_COMPILE)gcc
OBJCOPY = $(CROSS_COMPILE)objcopy
READELF = $(CROSS_COMPILE)readelf

# Compiler flags for gem5 SE mode:
#   -static          : produce a statically linked binary
#   No -nostdlib     : use standard C runtime (crt0) so main() is called normally
#   No custom linker : use default linker script
CFLAGS  = -march=rv64gc_zicbom -mabi=lp64d -O2 -static
CFLAGS += -Wall -Wextra

# gem5 configuration
GEM5_PATH   ?= ../build/RISCV/gem5.debug
CONFIG_PATH ?= ./riscv-o3-se.py

# Targets
TARGETS = cbo_clean_test.elf

# Default: build all
all: $(TARGETS)

# Generic rule: compile .c -> .elf directly (no custom start.S or linker script)
%.elf: %.c
	$(CC) $(CFLAGS) $< -o $@

# Clean build artifacts
clean:
	rm -f $(TARGETS)

# Run with gem5
run-cbo: cbo_clean_test.elf
	@if [ ! -f "$(GEM5_PATH)" ]; then \
		echo "Error: gem5 not found at $(GEM5_PATH)"; \
		echo "Set GEM5_PATH environment variable or build gem5 first"; \
		exit 1; \
	fi
	$(GEM5_PATH) $(CONFIG_PATH) $<


# Show ELF information
info-cbo: cbo_clean_test.elf
	$(READELF) -h $<
	$(READELF) -S $<

# Help
help:
	@echo "Available targets:"
	@echo "  all        - Build all tests (default)"
	@echo "  clean      - Clean build artifacts"
	@echo "  run-cbo    - Run cbo_clean_test with gem5"
	@echo "  info-cbo   - Show ELF info for cbo_clean_test"
	@echo "  help       - Show this help"
	@echo ""
	@echo "Variables:"
	@echo "  CROSS_COMPILE - Cross compiler prefix (default: riscv64-unknown-elf-)"
	@echo "  GEM5_PATH     - Path to gem5 binary (default: ../build/RISCV/gem5.debug)"
	@echo "  CONFIG_PATH   - Path to config script (default: ./riscv-o3-se.py)"

.PHONY: all clean run-cbo info-cbo help
