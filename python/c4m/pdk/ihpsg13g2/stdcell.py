# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Optional, Any, cast

from pdkmaster.technology import property_ as _prp, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexcell import factory as _fab

from .pdkmaster import tech, cktfab, layoutfab

__all__ = [
    "stdcellcanvas", "StdCellFactory", "stdcelllib",
    "stdcell3v3canvas", "StdCell3V3Factory", "stdcell3v3lib",
]

prims = tech.primitives

_activ = cast(_prm.WaferWire, prims["Activ"])
assert len(_activ.oxide) == 1
_nmos = cast(_prm.MOSFET, prims["sg13g2_lv_nmos"])
_pmos = cast(_prm.MOSFET, prims["sg13g2_lv_pmos"])
_ionmos = cast(_prm.MOSFET, prims["sg13g2_hv_nmos"])
_iopmos = cast(_prm.MOSFET, prims["sg13g2_hv_pmos"])


# standard cell libraries with minimum dimensions
class StdCellFactory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcellcanvas,
        )


stdcellcanvas = _fab.StdCellCanvas(
    tech=tech,
    nmos=_nmos, nmos_min_w=0.78,
    pmos=_pmos, pmos_min_w=0.78,
    cell_height=5.71, cell_horplacement_grid=0.80,
    m1_vssrail_width=1.12, m1_vddrail_width=1.12,
    well_edge_height=2.86,
)
# stdcelllib is handled by __getattr__()


class StdCell3V3Factory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell3v3canvas,
        )


stdcell3v3canvas = _fab.StdCellCanvas(
    tech=tech,
    nmos=_ionmos, nmos_min_w=0.76,
    pmos=_iopmos, pmos_min_w=0.76,
    cell_height=6.8, cell_horplacement_grid=1.00,
    m1_vssrail_width=1.22, m1_vddrail_width=1.22,
    well_edge_height=3.4,
    inside=_activ.oxide[0], inside_enclosure=_activ.min_oxide_enclosure[0],
)
# stdcell3v3lib is handled by __getattr__()


_stdcelllib: Optional[_lbry.RoutingGaugeLibrary] = None
stdcelllib: _lbry.RoutingGaugeLibrary
_stdcell3v3lib: Optional[_lbry.RoutingGaugeLibrary] = None
stdcell3v3lib: _lbry.RoutingGaugeLibrary
def __getattr__(name: str) -> Any:
    if name == "stdcelllib":
        global _stdcelllib
        if _stdcelllib is None:
            _stdcelllib = _lbry.RoutingGaugeLibrary(
                name="StdCellLib", tech=tech, routinggauge=stdcellcanvas.routinggauge,
            )
            StdCellFactory(lib=_stdcelllib).add_default()
        return _stdcelllib
    elif name == "stdcell3v3lib":
        global _stdcell3v3lib
        if _stdcell3v3lib is None:
            _stdcell3v3lib = _lbry.RoutingGaugeLibrary(
                name="StdCell3V3Lib", tech=tech, routinggauge=stdcell3v3canvas.routinggauge,
            )
            StdCell3V3Factory(lib=_stdcell3v3lib).add_default()
        return _stdcell3v3lib
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
