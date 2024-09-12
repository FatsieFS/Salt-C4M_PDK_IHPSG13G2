# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Callable, Optional, Any, cast
from functools import partial

from pdkmaster.technology import property_ as _prp, geometry as _geo, primitive as _prm
from pdkmaster.design import cell as _cell, circuit as _ckt, layout as _lay, library as _lbry

from c4m.flexcell import factory as _stdfab
from c4m.flexio import (
    DCDiodeT, IOSpecification, TrackSpecification, IOFrameSpecification,
    GuardRingT, PadOutT, PadTriOutT, PadInOutT, FactoryCellT, IOFactory,
)

from .pdkmaster import tech, cktfab, layoutfab
from .stdcell import _nmos, _pmos
from ._io_compliance import (
    guardring_create, dcdiode_create, PadIn, PadOut, PadTriOut, PadInOut,
)

__all__ = [
    "ihpsg13g2_iospec", "ihpsg13g2_ioframespec", "IHPSG13g2IOFactory",
    "ihpsg13g2_iofab", "iolib",
]


_prims = tech.primitives


class _IOStdCellFactory(_stdfab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary, name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=_iostdcellcanvas,
        )


_iostdcellcanvas = _stdfab.StdCellCanvas(
    tech=tech, **_stdfab.StdCellCanvas.compute_dimensions_lambda(lambda_=0.060),
    nmos=_nmos, pmos=_pmos,
)


# Make own libary for standard cells with prefixed names
_iostdlib = _lbry.RoutingGaugeLibrary(
    name="sg13g2_io_stdcells", tech=tech, routinggauge=_iostdcellcanvas.routinggauge
)
_iostdfab = _IOStdCellFactory(lib=_iostdlib, name_prefix="sg13g2_io_")
# TODO: change it so .add_default() is not needed
_iostdfab.add_default()

_cell_width = 80.0
_cell_height = 180.0
ihpsg13g2_iospec = IOSpecification(
    stdcellfab=_iostdfab,
    nmos=cast(_prm.MOSFET, _prims.sg13g2_lv_nmos), pmos=cast(_prm.MOSFET, _prims.sg13g2_lv_pmos),
    ionmos=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    iopmos=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    monocell_width=_cell_width, 
    metal_bigspace=0.6, topmetal_bigspace=4.0,
    clampnmos=None, clampnmos_w=4.4, clampnmos_l=0.6, clampnmos_rows=1,
    clamppmos=None, clamppmos_w=6.66, clamppmos_l=0.6, clamppmos_rows=2,
    clampfingers=0, clampfingers_analog=20, clampdrive={
        "4mA": 2, "16mA": 8, "30mA": 15,
    },
    rcclampdrive=43, rcclamp_rows=4,
    clampgate_gatecont_space=0.14, clampgate_sourcecont_space=0.24,
    clampgate_draincont_space=0.51,
    add_clampsourcetap=False,
    clampsource_cont_tap_enclosure=_prp.Enclosure((0.265, 0.06)), clampsource_cont_tap_space=0.075,
    clampdrain_layer=None, clampgate_clampdrain_overlap=None, clampdrain_active_ext=None,
    clampdrain_gatecont_space=None, clampdrain_contcolumns=1, clampdrain_via1columns=2,
    nres=cast(_prm.Resistor, _prims.Rppd),
    pres=cast(_prm.Resistor, _prims.Rppd),
    ndiode=cast(_prm.Diode, _prims.ndiode),
    pdiode=cast(_prm.Diode, _prims.pdiode),
    secondres_width=1.0, secondres_length=2.0,
    secondres_active_space=0.6,
    corerow_height=10, corerow_nwell_height=6,
    iorow_height=8.5, iorow_nwell_height=5.25,
    nwell_minspace=2.0, levelup_core_space=1.0,
    resvdd_prim=cast(_prm.Resistor, _prims.Rppd),
    resvdd_w=1.0, resvdd_lfinger=20.0, resvdd_fingers=26, resvdd_space=0.65,
    invvdd_n_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    invvdd_n_l=0.5, invvdd_n_w=9.0, invvdd_n_fingers=6, invvdd_n_rows=2,
    invvdd_p_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    invvdd_p_l=0.5, invvdd_p_w=7.0, invvdd_p_fingers=50,
    capvdd_l=9.5, capvdd_w=9.0, capvdd_fingers=7, capvdd_rows=2,
    rcmosfet_row_minspace=0.25,
    add_corem3pins=True, add_dcdiodes=True,
    dcdiode_actwidth=1.26, dcdiode_actspace=0.99, dcdiode_actspace_end=1.38,
    dcdiode_inneractheight=27.78, dcdiode_diodeguard_space=1.32, dcdiode_fingers=2,
    dcdiode_impant_enclosure=0.42,
    dcdiode_indicator=cast(_prm.Auxiliary, _prims["Recog.esd"]),
    iovss_ptap_extra=cast(_prm.SubstrateMarker, _prims["Substrate"]),
)
ihpsg13g2_ioframespec = IOFrameSpecification(
    cell_height=_cell_height,
    tracksegment_viapitch=2.0, trackconn_viaspace=0.3, trackconn_chspace=0.2,
    pad_height=None,
    padpin_height=3.0,
    pad_width=70.0,
    pad_viapitch=None,
    pad_viacorner_distance=23.0, pad_viametal_enclosure=3.0,
    pad_y=55.32,
    tracksegment_maxpitch=30.0, tracksegment_space={
        None: 2.0,
        cast(_prm.MetalWire, _prims.TopMetal2): 5.0,
    },
    acttracksegment_maxpitch=30, acttracksegment_space=1.0,
    track_specs=(
        TrackSpecification(name="iovss", bottom=6.0, width=55.0),
        TrackSpecification(name="iovdd", bottom=65.0, width=55.0),
        TrackSpecification(name="secondiovss", bottom=125.0, width=10.0),
        TrackSpecification(name="vddvss", bottom=(_cell_height - 41.0), width=40.0),
    ),
)
class IHPSG13g2IOFactory(IOFactory):
    iospec = ihpsg13g2_iospec
    ioframespec = ihpsg13g2_ioframespec

    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
        name_prefix: str="", name_suffix: str="",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            spec=self.iospec, framespec=self.ioframespec,
            name_prefix=name_prefix, name_suffix=name_suffix,
        )

    def guardring(self, *,
        type_: str, width: float, height: float, fill_well: bool = False, fill_implant: bool = False,
        create_cb: Optional[Callable[[GuardRingT], None]]=None,
    ):
        return super().guardring(
            type_=type_, width=width, height=height, fill_well=fill_well,
            fill_implant=fill_implant,
            create_cb=partial(guardring_create, create_cb=create_cb),
        )

    def dcdiode(self, *,
        type_: str, create_cb: Optional[Callable[[DCDiodeT], None]]=None,
    ) -> DCDiodeT:
        return super().dcdiode(
            type_=type_, create_cb=partial(dcdiode_create, create_cb=create_cb))

    def out(self, *,
        drivestrength: Optional[str]=None, create_cb: Optional[Callable[[PadOutT], None]]=None,
    ) -> PadOutT:
        return super().out(
            drivestrength=drivestrength, create_cb=create_cb, cell_class=PadOut,
        )

    def triout(self, *,
        drivestrength: Optional[str]=None,
        create_cb: Optional[Callable[[PadTriOutT], None]]=None,
    ) -> PadTriOutT:
        return super().triout(
            drivestrength=drivestrength, create_cb=create_cb, cell_class=PadTriOut,
        )

    def inout(self, *,
        drivestrength: Optional[str]=None,
        create_cb: Optional[Callable[[PadInOutT], None]]=None,
    ) -> PadInOutT:
        return super().inout(
            drivestrength=drivestrength, create_cb=create_cb, cell_class=PadInOut,
        )

    def get_cell(self, name: str, *,
        create_cb: Optional[Callable[[FactoryCellT], None]]=None,
    ) -> FactoryCellT:
        if name == "IOPadIn":
            return self.getcreate_cell(
                name=name, cell_class=PadIn, create_cb=create_cb,
            )
        else:
            return super().get_cell(name, create_cb=create_cb)
# iolib is handled by __getattr__()


_ihpsg13g2_iofab: Optional[IHPSG13g2IOFactory] = None
ihpsg13g2_iofab: IHPSG13g2IOFactory
_iolib: Optional[_lbry.Library] = None
iolib: _lbry.Library
def __getattr__(name: str) -> Any:
    if name in ("ihpsg13g2_iofab", "iolib"):
        global _ihpsg13g2_iofab, _iolib
        if _iolib is None:
            _iolib = _lbry.Library(name="sg13g2_io", tech=tech)
            _ihpsg13g2_iofab = IHPSG13g2IOFactory(
                lib=_iolib, cktfab=cktfab, layoutfab=layoutfab, name_prefix="sg13g2_",
            )
            _ihpsg13g2_iofab.get_cell("Gallery")
        if name == "ihpsg13g2_iofab":
            assert _ihpsg13g2_iofab is not None
            return _ihpsg13g2_iofab
        else:
            assert name == "iolib"
            return _iolib
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
