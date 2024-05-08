# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import cast

from pdkmaster.technology import property_ as _prp, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexcell import factory as _fab

from .pdkmaster import tech, cktfab, layoutfab

__all__ = [
    "stdcell1v2canvas", "StdCell1V2Factory", "stdcell1v2lib",
    "stdcell3v3canvas", "StdCell3V3Factory", "stdcell3v3lib",
    "stdcell1v2lambdacanvas", "StdCell1V2LambdaFactory", "stdcell1v2lambdalib",
    "stdcell3v3lambdacanvas", "StdCell3V3LambdaFactory", "stdcell3v3lambdalib",
]

prims = tech.primitives

_activ = cast(_prm.WaferWire, prims["Activ"])
assert len(_activ.oxide) == 1
_nmos = cast(_prm.MOSFET, prims["sg13g2_lv_nmos"])
_pmos = cast(_prm.MOSFET, prims["sg13g2_lv_pmos"])
_ionmos = cast(_prm.MOSFET, prims["sg13g2_hv_nmos"])
_iopmos = cast(_prm.MOSFET, prims["sg13g2_hv_pmos"])


# standard cell libraries with minimum dimensions
class StdCell1V2Factory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell1v2canvas,
        )


stdcell1v2canvas = _fab.StdCellCanvas(
    tech=tech,
    nmos=_nmos, nmos_min_w=0.76,
    pmos=_pmos, pmos_min_w=0.76,
    cell_height=5.5, cell_horplacement_grid=0.80,
    m1_vssrail_width=1.12, m1_vddrail_width=1.12,
    well_edge_height=2.71,
)
stdcell1v2lib = _lbry.RoutingGaugeLibrary(
    name="StdCell1V2Lib", tech=tech, routinggauge=stdcell1v2canvas.routinggauge,
)
StdCell1V2Factory(lib=stdcell1v2lib).add_default()


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
stdcell3v3lib = _lbry.RoutingGaugeLibrary(
    name="StdCell3V3Lib", tech=tech, routinggauge=stdcell3v3canvas.routinggauge,
)
StdCell3V3Factory(lib=stdcell3v3lib).add_default()


# Legacy dimensions based on lambda rules
class StdCell1V2LambdaFactory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell1v2lambdacanvas,
        )


stdcell1v2lambdacanvas = _fab.StdCellCanvas(
    tech=tech, **_fab.StdCellCanvas.compute_dimensions_lambda(lambda_=0.060),
    nmos=_nmos, pmos=_pmos,
)
stdcell1v2lambdalib = _lbry.RoutingGaugeLibrary(
    name="StdCell1V2LambdaLib", tech=tech, routinggauge=stdcell1v2lambdacanvas.routinggauge,
)
StdCell1V2LambdaFactory(lib=stdcell1v2lambdalib).add_default()


class StdCell3V3LambdaFactory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcell3v3lambdacanvas,
        )


stdcell3v3lambdacanvas = _fab.StdCellCanvas(
    tech=tech, **_fab.StdCellCanvas.compute_dimensions_lambda(lambda_=0.06),
    nmos=_ionmos, pmos=_iopmos,
    inside=_activ.oxide[0], inside_enclosure=_activ.min_oxide_enclosure[0],
)
stdcell3v3lambdalib = _lbry.RoutingGaugeLibrary(
    name="StdCell3V3LambdaLib", tech=tech, routinggauge=stdcell3v3lambdacanvas.routinggauge,
)
StdCell3V3LambdaFactory(lib=stdcell3v3lambdalib).add_default()
