# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from importlib import import_module
from typing import Iterable, Any

from pdkmaster.design import library as _lbry

from c4m.flexcell import factory as _stdfab

from .pdkmaster import *
from .spice import *
from .pyspice import *
from .klayout import register_primlib as pya_register_primlib


# This module uses lazy submodule importing using __getattr__() to avoid that all
# libraries are generated when this module is imported.


from .pdkmaster import __all__ as _pdkmaster_all
from .pyspice import __all__ as _pyspice_all
from .stdcell import __all__ as _stdcell_all
from .io import __all__ as _io_all

stdcellcanvas: _stdfab.StdCellCanvas
StdCellFactory: type
stdcelllib: _lbry.RoutingGaugeLibrary
stdcell3v3canvas: _stdfab.StdCellCanvas
StdCell3V3Factory: type
stdcell3v3lib: _lbry.RoutingGaugeLibrary
libs: Iterable[_lbry.Library]
def __getattr__(name: str) -> Any:
    if name in _stdcell_all:
        stdcell = import_module(".stdcell", __name__)
        return getattr(stdcell, name)
    elif name in _io_all:
        io = import_module(".io", __name__)
        return getattr(io, name)
    elif name == "libs":
        from .stdcell import stdcelllib, stdcell3v3lib
        from .io import iolib
        return [stdcelllib, stdcell3v3lib, iolib]
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    self = import_module(__name__)
    return sorted((
        *(name for name in self.__dict__.keys() if name.startswith("__")),
        *_pdkmaster_all, *_pyspice_all,
        "pya_register_primlib",
        *_stdcell_all, *_io_all,
        "libs",
    ))
