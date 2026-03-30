/*
 * Test case for CBO.CLEAN instruction
 * This test performs a series of stores to addresses with 64-byte intervals,
 * then uses cbo.clean to write back those cache lines.
 *
 * Compiled for gem5 SE (System Call Emulation) mode:
 *   riscv64-unknown-elf-gcc -march=rv64gc_zicbom -mabi=lp64d -O2 -static \
 *     cbo_clean_test.c -o cbo_clean_test.elf
 */

#include <stdint.h>
#include <stdlib.h>

#define CACHE_LINE_SIZE 64
#define NUM_LINES 1
#define BUFFER_SIZE (CACHE_LINE_SIZE * NUM_LINES)

/* Buffer for testing - aligned to cache line boundary */
static volatile uint8_t buffer[BUFFER_SIZE] __attribute__((aligned(64)));
static uint8_t INPUT_VAL = 0x55;

static inline void
cbo_clean(void *addr)
{
    asm volatile("cbo.clean (%0)" : : "r"(addr) : "memory");
}

int
main(void)
{
    volatile uint8_t *ptr;
    int i;

    /* Perform stores at 64-byte intervals */
    for (i = 0; i < NUM_LINES; i++) {
        ptr = (volatile uint8_t *)(buffer + i * CACHE_LINE_SIZE);
        *ptr = (uint8_t)INPUT_VAL;
    }

    /* Use cbo.clean to write back each cache line */
    for (i = 0; i < NUM_LINES; i++) {
        cbo_clean((void *)(buffer + i * CACHE_LINE_SIZE));
    }

    /* Verify the values */
    for (i = 0; i < NUM_LINES; i++) {
        ptr = (volatile uint8_t *)(buffer + i * CACHE_LINE_SIZE);
        if (*ptr != INPUT_VAL) {
            exit(1); /* Test failed */
        }
    }

    exit(0); /* Test passed */
}
