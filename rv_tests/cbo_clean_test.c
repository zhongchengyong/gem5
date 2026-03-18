/*
 * Test case for CBO.CLEAN instruction
 * This test performs a series of stores to addresses with 64-byte intervals,
 * then uses cbo.clean to write back those cache lines.
 */

#include <stdint.h>

#define CACHE_LINE_SIZE 64
#define NUM_LINES 16
#define BUFFER_SIZE (CACHE_LINE_SIZE * NUM_LINES)

/* Buffer for testing - aligned to cache line boundary */
static volatile uint8_t buffer[BUFFER_SIZE] __attribute__((aligned(64)));

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

    /* Initialize buffer with pattern */
    for (i = 0; i < BUFFER_SIZE; i++) {
        buffer[i] = (uint8_t)(i & 0xFF);
    }

    /* Perform stores at 64-byte intervals */
    for (i = 0; i < NUM_LINES; i++) {
        ptr = (volatile uint8_t *)(buffer + i * CACHE_LINE_SIZE);
        *ptr = (uint8_t)i;
    }

    /* Use cbo.clean to write back each cache line */
    for (i = 0; i < NUM_LINES; i++) {
        cbo_clean((void *)(buffer + i * CACHE_LINE_SIZE));
    }

    /* Verify the values */
    for (i = 0; i < NUM_LINES; i++) {
        ptr = (volatile uint8_t *)(buffer + i * CACHE_LINE_SIZE);
        if (*ptr != (uint8_t)i) {
            return -1; /* Test failed */
        }
    }

    return 0; /* Test passed */
}
