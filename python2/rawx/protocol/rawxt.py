import os
import sys
import time
import serial
import struct
from rawx.base import RawXC
from rawx.const import *
from rawx.tools import log

class RAWXT(RawXC):
    '''
    RAWX protocol implementation, expects an object to read from and an
    object to write to.

    >>> rawstream = RAWX()

    '''

    def send_raw_file(self, filename, fserial):
        '''
        Send a file via serial port.

            >>> send_raw_file
            True

        Returns ``True`` upon succesful transmission or ``False`` in case of
        failure.
        '''
        
        # File transfer
        frawfile = open(filename, 'rb')
        
        filesz = os.path.getsize(filename)
        
        if not filesz:
            return False
        
        data = frawfile.read(filesz)
        
        if not data:
            return False
            
        # Send file size
        #s1 = struct.pack('<I',filesz)
        #b1 = struct.unpack('BBBB',s1)
        #fserial.write(b1)
                
        fserial.write(data)
        
        frawfile.close()

        return True
