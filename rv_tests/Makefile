# Makefile for RISC-V cbo.clean test
#
# Usage:
#   make              - Build the test
#   make clean        - Clean build artifacts
#   make run          - Run with gem5 (requires GEM5_PATH)
#   make info         - Show ELF information
#   make help         - Show this help

# Cross compiler prefix - adjust if needed
# Default to Xuantie compiler if available
CROSS_COMPILE ?= riscv64-unknown-elf-

CC = $(CROSS_COMPILE)gcc
OBJCOPY = $(CROSS_COMPILE)objcopy
READELF = $(CROSS_COMPILE)readelf

# Compiler flags
CFLAGS = -march=rv64gc_zicbom -mabi=lp64d -O2 -static
CFLAGS += -Wall -Wextra

# Linker flags
LDFLAGS = -static -nostdlib

# gem5 configuration
GEM5_PATH ?= ../build/RISCV/gem5.debug
CONFIG_PATH ?= ./riscv-o3-se.py

# Source files
TARGET = cbo_clean_test
SRC = cbo_clean_test.c
OBJ = $(SRC:.c=.o)
START_SRC = start.S
ELF = $(TARGET).elf

# Default target
all: $(ELF)

# Compile source to object
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Compile assembly to object
start.o: $(START_SRC)
	$(CC) $(CFLAGS) -c $< -o $@

# Link object to ELF
$(ELF): $(OBJ) start.o
	$(CC) $(CFLAGS) $(LDFLAGS) -T linker.ld $^ -o $@

# Clean build artifacts
clean:
	rm -f $(OBJ) $(ELF) start.o

# Run with gem5
run: $(ELF)
	@if [ ! -f "$(GEM5_PATH)" ]; then \
		echo "Error: gem5 not found at $(GEM5_PATH)"; \
		echo "Set GEM5_PATH environment variable or build gem5 first"; \
		exit 1; \
	fi
	$(GEM5_PATH) $(CONFIG_PATH) $(ELF)

# Show ELF information
info: $(ELF)
	$(READELF) -h $(ELF)
	$(READELF) -S $(ELF)

# Help
help:
	@echo "Available targets:"
	@echo "  all   - Build the test (default)"
	@echo "  clean - Clean build artifacts"
	@echo "  run   - Run with gem5"
	@echo "  info  - Show ELF information"
	@echo "  help  - Show this help"
	@echo ""
	@echo "Variables:"
	@echo "  CROSS_COMPILE - Cross compiler prefix (default: riscv64-linux-gnu-)"
	@echo "  GEM5_PATH     - Path to gem5.opt (default: ../build/RISCV/gem5.opt)"
	@echo "  CONFIG_PATH   - Path to config script (default: ./riscv-o3-se.py)"

.PHONY: all clean run info help
