from typing import Type

from m5.objects import (
    AddrRange,
    ARTCache,
    Cache,
    SectorTags,
    NoncoherentCache
)

class ARTICache(ARTCache):
    def __init__(
        self, flash_addr_range: AddrRange
    ):
        super().__init__(
            size="1KiB",
            # num_sets = size / (block_size × num_blocks_per_sector × assoc)
            assoc=8,
            tag_latency=1,
            data_latency=1,
            response_latency=0,
            mshrs=1,
            tgts_per_mshr=4,
            writeback_clean=False,  # ART I-Cache is not write-back
            is_read_only=True,  # I-Cache is read-only
            addr_ranges=[flash_addr_range],
            tags=SectorTags(
                num_blocks_per_sector=4 # 4 sectors per cache line
            ),
            bypass_cache=False,
            bypass_prefetch=False
        )

class ARTDCache(NoncoherentCache):
    def __init__(self, flash_addr_range: AddrRange):
        self._size = "256B"
        # Make it fully associative
        self._assoc = 8

        self._response_latency = 0
        self._tag_latency = 1
        self._data_latency = 1

        # The STM32G4 ART I-Cache doesn't allocate MSHRs but also STM32G4 has
        # no out-of-order execution and with a single issue core, 1 MSHR is 
        # sufficient to the model.
        self._mshrs = 1
        self._tgts_per_mshr = 4

        # This is a DCache, so read-write
        self._is_read_only = False
        # replacement policy is default LRU
        
        super().__init__(
            size=self._size,
            assoc=self._assoc,
            tag_latency=self._tag_latency,
            data_latency=self._data_latency,
            response_latency=self._response_latency,
            mshrs=self._mshrs,
            tgts_per_mshr=self._tgts_per_mshr,
            is_read_only=self._is_read_only,
            addr_ranges=[flash_addr_range]
        )
        
