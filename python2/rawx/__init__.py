__author__ = 'DAB-Embedded'
__version__ = '1.0.0'

import gettext
from rawx.protocol.rawxt import RAWXT

gettext.install('rawxt')

# To satisfy import *
__all__ = [
    'RAWXT',
]
