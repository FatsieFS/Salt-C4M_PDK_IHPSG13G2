# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import List
from pdkmaster.design import library as _lbry

from .pdkmaster import *
from .pyspice import *
from .stdcell import *
from .io import *
from .klayout import register_primlib as pya_register_primlib


__libs__: List[_lbry.Library] = [
    stdcell1v2lib, stdcell1v2lambdalib,
    stdcell3v3lib, stdcell3v3lambdalib,
    iolib,
]
