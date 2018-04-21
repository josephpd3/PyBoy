# -*- encoding: utf-8 -*-
#
# Authors: Mads Ynddal
# License: See LICENSE file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from RAM import allocateRAM
import Global
import numpy as np # np.fromfile is not included in Cython version
import struct
import cython

class BootROM():
    def __init__(self, bootROMFile):
        if bootROMFile is not None:
            if Global.isPyPy:
                with open(bootROMFile, "rb") as bootROMFileHandle:
                    rom = bootROMFileHandle.read()
                # print _bootROM.shape, romData.shape
                # print [hex(x) for x in _bootROM]
                # print [hex(x) for x in romData]
                # print _bootROM.shape
                # print [hex(x) for x in _bootROM]
                _bootROM = struct.unpack('%iB' % len(rom), rom)
            else:
                _bootROM = np.fromfile(bootROMFile, np.uint8, 256).astype(np.uint32)
        else:
            _bootROM = allocateRAM(256)
            # _bootROM = [0 for x in range(256)]
            # Set stack pointer
            _bootROM[0x00] = 0x31
            _bootROM[0x01] = 0xFE
            _bootROM[0x02] = 0xFF

            # Inject jump to 0xFC
            _bootROM[0x03] = 0xC3
            _bootROM[0x04] = 0xFC
            _bootROM[0x05] = 0x00

            # Inject code to disable boot-ROM
            _bootROM[0xFC] = 0x3E
            _bootROM[0xFD] = 0x01
            _bootROM[0xFE] = 0xE0
            _bootROM[0xFF] = 0x50

        if Global.isPyPy:
            self.bootROM = _bootROM
        else:
            self.bootROM = _bootROM.copy()


    @cython.locals(address=cython.ushort)
    def __getitem__(self, address):
        return self.bootROM[address]