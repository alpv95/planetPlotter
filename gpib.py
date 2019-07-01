"""
 * Copyright (c) 2004 Frank Mori Hess (fmhess@users.sourceforge.net)
 * Copyright (c) 2018 Guilhem Vavelin (guileukow@users.sourceforge.net)
 *
 *    This source code is free software; you can redistribute it
 *    and/or modify it in source code form under the terms of the GNU
 *    General Public License as published by the Free Software
 *    Foundation; either version 2 of the License, or (at your option)
 *    any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program; if not, write to the Free Software
 *    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA
 """

import ctypes
import ctypes.util
import os
from ctypes import *


def enum(**enums):
    return type("Enum", (), enums)


ibsta_bit_numbers = enum(
    DCAS_NUM=0,
    DTAS_NUM=1,
    LACS_NUM=2,
    TACS_NUM=3,
    ATN_NUM=4,
    CIC_NUM=5,
    REM_NUM=6,
    LOK_NUM=7,
    CMPL_NUM=8,
    EVENT_NUM=9,
    SPOLL_NUM=10,
    RQS_NUM=11,
    SRQI_NUM=12,
    END_NUM=13,
    TIMO_NUM=14,
    ERR_NUM=15,
)

# IBSTA status bits (returned by all functions)
ibsta_bits = enum(
    DCAS=(1 << ibsta_bit_numbers.DCAS_NUM),  # device clear state
    DTAS=(1 << ibsta_bit_numbers.DTAS_NUM),  # device trigger state
    LACS=(1 << ibsta_bit_numbers.LACS_NUM),  # GPIB interface is addressed as Listener
    TACS=(1 << ibsta_bit_numbers.TACS_NUM),  # GPIB interface is addressed as Talker
    ATN=(1 << ibsta_bit_numbers.ATN_NUM),  # Attention is asserted
    CIC=(1 << ibsta_bit_numbers.CIC_NUM),  # GPIB interface is Controller-in-Charge
    REM=(1 << ibsta_bit_numbers.REM_NUM),  # remote state
    LOK=(1 << ibsta_bit_numbers.LOK_NUM),  # lockout state
    CMPL=(1 << ibsta_bit_numbers.CMPL_NUM),  # I/O is complete
    EVENT=(1 << ibsta_bit_numbers.EVENT_NUM),  # DCAS, DTAS, or IFC has occurred
    SPOLL=(1 << ibsta_bit_numbers.SPOLL_NUM),  # board serial polled by busmaster
    RQS=(1 << ibsta_bit_numbers.RQS_NUM),  # Device requesting service
    SRQI=(1 << ibsta_bit_numbers.SRQI_NUM),  # SRQ is asserted
    END=(1 << ibsta_bit_numbers.END_NUM),  # EOI or EOS encountered
    TIMO=(
        1 << ibsta_bit_numbers.TIMO_NUM
    ),  # Time limit on I/O or wait function exceeded
    ERR=(1 << ibsta_bit_numbers.ERR_NUM),  # Function call terminated on error
)

# IBERR error codes
iberr_code = enum(
    EDVR=0,  # system error
    ECIC=1,  # not CIC
    ENOL=2,  # no listeners
    EADR=3,  # CIC and not addressed before I/O
    EARG=4,  # bad argument to function call
    ESAC=5,  # not SAC
    EABO=6,  # I/O operation was aborted
    ENEB=7,  # non-existent board (GPIB interface offline)
    EDMA=8,  # DMA hardware error detected
    EOIP=10,  # new I/O attempted with old I/O in progress
    ECAP=11,  # no capability for intended opeation
    EFSO=12,  # file system operation error
    EBUS=14,  # bus error
    ESTB=15,  # lost serial poll bytes
    ESRQ=16,  # SRQ stuck on
    ETAB=20,  # Table Overflow
)

GPIB_Errors = {
    (
        iberr_code.EDVR
    ): "A system call has failed. ibcnt/ibcntl will be set to the value of errno.",
    (
        iberr_code.ECIC
    ): "Your interface board needs to be controller-in-charge, but is not.",
    (
        iberr_code.ENOL
    ): "You have attempted to write data or command bytes, but there are no listeners currently addressed.",
    (
        iberr_code.EADR
    ): "The interface board has failed to address itself properly before starting an io operation.",
    (iberr_code.EARG): "One or more arguments to the function call were invalid.",
    (iberr_code.ESAC): "The interface board needs to be system controller, but is not.",
    (
        iberr_code.EABO
    ): "A read or write of data bytes has been aborted, possibly due to a timeout or reception of a device clear command.",
    (
        iberr_code.ENEB
    ): "The GPIB interface board does not exist, its driver is not loaded, or it is in use by another process.",
    (iberr_code.EDMA): "Not used (DMA error), included for compatibility purposes.",
    (
        iberr_code.EOIP
    ): "Function call can not proceed due to an asynchronous IO operation (ibrda(), ibwrta(), or ibcmda()) in progress.",
    (
        iberr_code.ECAP
    ): "Incapable of executing function call, due the GPIB board lacking the capability, or the capability being disabled in software.",
    (
        iberr_code.EFSO
    ): "File system error. ibcnt/ibcntl will be set to the value of errno.",
    (iberr_code.EBUS): "An attempt to write command bytes to the bus has timed out.",
    (
        iberr_code.ESTB
    ): "One or more serial poll status bytes have been lost. This can occur due to too many status bytes accumulating (through automatic serial polling) without being read.",
    (iberr_code.ESRQ): "The serial poll request service line is stuck on.",
    (
        iberr_code.ETAB
    ): "This error can be returned by ibevent(), FindLstn(), or FindRQS(). See their descriptions for more information.",
}

# Timeout values and meanings
gpib_timeout = enum(
    TNONE=0,  # Infinite timeout (disabled)
    T10us=1,  # Timeout of 10 usec (ideal)
    T30us=2,  # Timeout of 30 usec (ideal)
    T100us=3,  # Timeout of 100 usec (ideal)
    T300us=4,  # Timeout of 300 usec (ideal)
    T1ms=5,  # Timeout of 1 msec (ideal)
    T3ms=6,  # Timeout of 3 msec (ideal)
    T10ms=7,  # Timeout of 10 msec (ideal)
    T30ms=8,  # Timeout of 30 msec (ideal)
    T100ms=9,  # Timeout of 100 msec (ideal)
    T300ms=10,  # Timeout of 300 msec (ideal)
    T1s=11,  # Timeout of 1 sec (ideal)
    T3s=12,  # Timeout of 3 sec (ideal)
    T10s=13,  # Timeout of 10 sec (ideal)
    T30s=14,  # Timeout of 30 sec (ideal)
    T100s=15,  # Timeout of 100 sec (ideal)
    T300s=16,  # Timeout of 300 sec (ideal)
    T1000s=17,  # Timeout of 1000 sec (maximum)
)

# End-of-string (EOS) modes for use with ibeos
eos_flags = enum(
    EOS_MASK=0x1c00,
    REOS=0x0400,  # Terminate reads on EOS
    XEOS=0x800,  # assert EOI when EOS char is sent
    BIN=0x1000,  # Do 8-bit compare on EOS
)

# GPIB Bus Control Lines bit vector
bus_control_line = enum(
    ValidDAV=0x01,
    ValidNDAC=0x02,
    ValidNRFD=0x04,
    ValidIFC=0x08,
    ValidREN=0x10,
    ValidSRQ=0x20,
    ValidATN=0x40,
    ValidEOI=0x80,
    ValidALL=0xff,
    BusDAV=0x0100,  # DAV  line status bit
    BusNDAC=0x0200,  # NDAC line status bit
    BusNRFD=0x0400,  # NRFD line status bit
    BusIFC=0x0800,  # IFC  line status bit
    BusREN=0x1000,  # REN  line status bit
    BusSRQ=0x2000,  # SRQ  line status bit
    BusATN=0x4000,  # ATN  line status bit
    BusEOI=0x8000,  # EOI  line status bit
)

old_bus_control_line = enum(
    BUS_DAV=0x0100,  # DAV  line status bit
    BUS_NDAC=0x0200,  # NDAC line status bit
    BUS_NRFD=0x0400,  # NRFD line status bit
    BUS_IFC=0x0800,  # IFC  line status bit
    BUS_REN=0x1000,  # REN  line status bit
    BUS_SRQ=0x2000,  # SRQ  line status bit
    BUS_ATN=0x4000,  # ATN  line status bit
    BUS_EOI=0x8000,  # EOI  line status bit
)

# Possible GPIB command messages
cmd_byte = enum(
    GTL=0x1,  # go to local
    SDC=0x4,  # selected device clear
    PPConfig=0x5,
    PPC=0x5,  # parallel poll configure
    GET=0x8,  # group execute trigger
    TCT=0x9,  # take control
    LLO=0x11,  # local lockout
    DCL=0x14,  # device clear
    PPU=0x15,  # parallel poll unconfigure
    SPE=0x18,  # serial poll enable
    SPD=0x19,  # serial poll disable
    LAD=0x20,  # value to be 'ored' in to obtain listen address
    UNL=0x3F,  # unlisten
    TAD=0x40,  # value to be 'ored' in to obtain talk address
    UNT=0x5F,  # untalk
    SAD=0x60,  # my secondary address (base)
    PPE=0x60,  # parallel poll enable (base)
    PPD=0x70,  # parallel poll disable
)

ppe_bits = enum(
    PPC_DISABLE=0x10, PPC_SENSE=0x8, PPC_DIO_MASK=0x7  # parallel poll sense bit
)

ibask_option = enum(
    IbaPAD=0x1,
    IbaSAD=0x2,
    IbaTMO=0x3,
    IbaEOT=0x4,
    IbaPPC=0x5,  # board only
    IbaREADDR=0x6,  # device only
    IbaAUTOPOLL=0x7,  # board only
    IbaCICPROT=0x8,  # board only
    IbaIRQ=0x9,  # board only
    IbaSC=0xa,  # board only
    IbaSRE=0xb,  # board only
    IbaEOSrd=0xc,
    IbaEOSwrt=0xd,
    IbaEOScmp=0xe,
    IbaEOSchar=0xf,
    IbaPP2=0x10,  # board only
    IbaTIMING=0x11,  # board only
    IbaDMA=0x12,  # board only
    IbaReadAdjust=0x13,
    IbaWriteAdjust=0x14,
    IbaEventQueue=0x15,  # board only
    IbaSPollBit=0x16,  # board only
    IbaSpollBit=0x16,  # board only
    IbaSendLLO=0x17,  # board only
    IbaSPollTime=0x18,  # device only
    IbaPPollTime=0x19,  # board only
    IbaEndBitIsNormal=0x1a,
    IbaUnAddr=0x1b,  # device only
    IbaHSCableLength=0x1f,  # board only
    IbaIst=0x20,  # board only
    IbaRsv=0x21,  # board only
    IbaBNA=0x200,  # device only
    # linux-gpib extensions
    Iba7BitEOS=0x1000,  # board only. Returns 1 if board supports 7 bit eos compares
)

ibconfig_option = enum(
    IbcPAD=0x1,
    IbcSAD=0x2,
    IbcTMO=0x3,
    IbcEOT=0x4,
    IbcPPC=0x5,  # board only
    IbcREADDR=0x6,  # device only
    IbcAUTOPOLL=0x7,  # board only
    IbcCICPROT=0x8,  # board only
    IbcIRQ=0x9,  # board only
    IbcSC=0xa,  # board only
    IbcSRE=0xb,  # board only
    IbcEOSrd=0xc,
    IbcEOSwrt=0xd,
    IbcEOScmp=0xe,
    IbcEOSchar=0xf,
    IbcPP2=0x10,  # board only
    IbcTIMING=0x11,  # board only
    IbcDMA=0x12,  # board only
    IbcReadAdjust=0x13,
    IbcWriteAdjust=0x14,
    IbcEventQueue=0x15,  # board only
    IbcSPollBit=0x16,  # board only
    IbcSpollBit=0x16,  # board only
    IbcSendLLO=0x17,  # board only
    IbcSPollTime=0x18,  # device only
    IbcPPollTime=0x19,  # board only
    IbcEndBitIsNormal=0x1a,
    IbcUnAddr=0x1b,  # device only
    IbcHSCableLength=0x1f,  # board only
    IbcIst=0x20,  # board only
    IbcRsv=0x21,  # board only
    IbcBNA=0x200,  # device only
)

t1_delays = enum(T1_DELAY_2000ns=1, T1_DELAY_500ns=2, T1_DELAY_350ns=3)


class Gpib:
    def __init__(self):
        # Need to do this to load the NSSpeechSynthesizer class, which is in AppKit.framework
        self.libgpib = ctypes.cdll.LoadLibrary(
            ctypes.util.find_library("libmacosx_gpib_lib")
        )

        self.libgpib.objc_getClass.restype = ctypes.c_void_p
        self.libgpib.sel_registerName.restype = ctypes.c_void_p
        self.libgpib.objc_msgSend.restype = ctypes.c_void_p
        self.libgpib.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

        # Without this, it will still work, but it'll leak memory
        NSAutoreleasePool = self.libgpib.objc_getClass("NSAutoreleasePool")
        self.autorelease = self.libgpib.objc_msgSend(
            NSAutoreleasePool, self.libgpib.sel_registerName("alloc")
        )
        self.autorelease = self.libgpib.objc_msgSend(
            self.autorelease, self.libgpib.sel_registerName("init")
        )

        gpib_visa = self.libgpib.objc_getClass("gpib_visa")
        self.visa = self.libgpib.objc_msgSend(
            gpib_visa, self.libgpib.sel_registerName("alloc")
        )
        self.visa = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("init")
        )

    def _ThreadIbcnt(self):
        return self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ThreadIbcnt")
        )

    def _SetGpibError(self, funcname):
        pass
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        code = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ThreadIberr")
        )

        if code == iberr_code.EDVR or code == iberr_code.EFSO:
            sverrno = self.libgpib.objc_msgSend(
                self.visa, self.libgpib.sel_registerName("ThreadIbcnt")
            )
            print(
                "%s() error: %s (errno: %d)" % (funcname, os.strerror(sverrno), sverrno)
            )
        elif code in GPIB_Errors.keys():
            print("%s() failed: %s" % (funcname, GPIB_Errors[code]))
        else:
            print("%s() failed: unknown reason (iberr: %d)." % (funcname, code))

    def find(self, name):
        """
        find -- get a board handle according to its name
        find(name) -> handle
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        ud = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibfind:"), name
        )
        if ud < 0:
            self._SetGpibError("find")
        return ud

    def count(self):
        """
        count -- get the count of board found
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        return self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibcount")
        )

    def name(self, board):
        """
        name -- get the name of board board
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_char_p
        return str(
            buffer(
                self.libgpib.objc_msgSend(
                    self.visa, self.libgpib.sel_registerName("ibname:"), board
                )
            )
        )

    def dev(self, board, pad, sad=-1, tmo=gpib_timeout.T1s, eot=1, eos_mode=0):
        """
        dev -- get a device handle"
        dev(boardid, pad, [sad, timeout, eot, eos_mode]) -> handle
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        ud = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibdev::::::"),
            board,
            pad,
            sad,
            tmo,
            eot,
            eos_mode,
        )
        if ud < 0:
            self._SetGpibError("dev")
            return None
        return ud

    def ask(self, handle, option):
        """
        ask -- query configuration (board or device)
        ask(handle, option) -> result
        option should be one one of the symbolic constants gpib.ibask_option.IbaXXXX
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        result = ctypes.c_int(0)
        retval = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibask:::"),
            handle,
            option,
            byref(result),
        )
        if retval & ibsta_bits.ERR:
            self._SetGpibError("ask")
            return None
        return result.value

    def config(self, handle, option, setting):
        """
        config -- change configuration (board or device)
        config(handle, option, setting)
        option should be one one of the symbolic constants gpib.ibconfig_option.IbcXXXX
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        sta = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibconfig:::"),
            handle,
            option,
            setting,
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("config")
            return None
        return sta

    def listener(self, handle, pad, sad=-1):
        """
        listener -- check if listener is present (board or device)
        listener(handle, pad, [sad]) -> boolean
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        found_listener = ctypes.c_bool(False)
        retval = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibln::::"),
            handle,
            pad,
            sad,
            byref(found_listener),
        )
        if retval & ibsta_bits.ERR:
            self._SetGpibError("listener")
            return None
        return found_listener.value

    def read(self, handle, num_bytes=512):
        """
        read -- read data bytes (board or device)
        read(handle, num_bytes) -> string
        """
        retval = (c_ubyte * num_bytes)()
        sta = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibrd:::"),
            handle,
            byref(retval),
            num_bytes,
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("read")
            return None
        return str(buffer(retval)[0 : self._ThreadIbcnt() - 1])

    def read_async(self, handle, num_bytes=512):
        """
        read_async -- read data bytes asynchronously (board or device)
        read_async(handle, num_bytes) -> string
        """
        retval = (c_ubyte * num_bytes)()
        sta = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibrda:::"),
            handle,
            byref(retval),
            num_bytes,
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("read_async")
            return None
        return str(buffer(retval)[0 : self._ThreadIbcnt() - 1])

    def write(self, handle, data):
        """
        write -- write data bytes (board or device)
        write(handle, data)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        data_len = len(data)
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibwrt:::"), handle, data, data_len
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("write")
            return None
        return sta

    def write_async(self, handle, data):
        """
        write_async -- write data bytes asynchronously (board or device)
        write_async(handle, data)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        data_len = len(data)
        sta = self.libgpib.objc_msgSend(
            self.visa,
            self.libgpib.sel_registerName("ibwrta:::"),
            handle,
            data,
            data_len,
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("write_async")
            return None
        return sta

    def command(self, handle, data):
        """
        command -- write command bytes (board)\n"
        command(handle, data)
        """
        # self.libgpib.objc_msgSend.argtypes = (
        #     ctypes.c_void_p,
        #     ctypes.c_void_p,
        #     ctypes.c_void_p,
        #     ctypes.c_void_p,
        #     ctypes.c_int,
        # )
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        data_len = 1
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibcmd:::"), handle, data, data_len
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("command")
            return None
        return sta

    def remote_enable(self, handle, enable):
        """
        remote_enable -- set remote enable (board)
        remote_enable(handle, enable)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibsre::"), handle, enable
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("remote_enable")
            return None
        return sta

    def clear(self, handle):
        """
        clear -- clear device (device)
        clear(handle)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibclr:"), handle
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("clear")
            return None
        return sta

    def local(self, handle):
        """
        ibloc -- push device to local mode (device)
        ibloc(handle)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibloc:"), handle
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("local")
            return None
        return sta

    def interface_clear(self, handle):
        """
        interface_clear -- perform interface clear (board)
        interface_clear(handle)
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_int
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibsic:"), handle
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("interface_clear")
            return None
        return sta

    def close(self):
        """
        close --- close all opened board and device and cleanup everything
        It is mandatory to call this function before leaving the program
        close()
        """
        self.libgpib.objc_msgSend(self.visa, self.libgpib.sel_registerName("close"))
        self.libgpib.objc_msgSend(
            self.autorelease, self.libgpib.sel_registerName("release")
        )

    def wait(self, handle, mask):
        """
        wait -- wait for event (board or device)
        wait(handle, mask)
        """
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibwait::"), handle, mask
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("wait")
            return None
        return sta

    def serial_poll(self, handle):
        """
        serial_poll -- conduct serial poll (device)
        serial_poll(handle) -> status_byte
        """
        spr = (c_ubyte)(0)
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibrsp::"), handle, byref(spr)
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("serial_poll")
            return None
        return spr.value

    def trigger(self, handle):
        """
        trigger -- trigger device (device)
        trigger(handle)
        """
        sta = self.libgpib.objc_msgSend(
            self.visa, self.libgpib.sel_registerName("ibtrg:"), handle
        )
        if sta & ibsta_bits.ERR:
            self._SetGpibError("trigger")
            return None
        return sta

    def version(self):
        """
        version -- obtain the current macosx_gpib_lib version
        version()
        """
        self.libgpib.objc_msgSend.restype = ctypes.c_char_p
        return str(
            buffer(
                self.libgpib.objc_msgSend(
                    self.visa, self.libgpib.sel_registerName("ibvers")
                )
            )
        )
