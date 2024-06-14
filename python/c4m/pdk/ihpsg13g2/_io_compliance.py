# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
"""This is module with support code to make layout compliant with IHP specific requirements
For internal use only.

This module uses non-backwards compatible parts of the PDKMaster so need to be carefully
kept up-to-date with these libraries.
"""
from typing import Optional, Callable, cast

from pdkmaster.technology import geometry as _geo, primitive as _prm
from pdkmaster.design import layout as _lay
from pdkmaster.design.layout.layout_ import _InstanceSubLayout

from c4m.flexio import GuardRingT, DCDiodeT, PadInT, PadOutT, PadTriOutT, PadInOutT
from .pdkmaster import tech


_prims = tech.primitives


def guardring_create(gr: GuardRingT, *, create_cb: Optional[Callable[[GuardRingT], None]]) -> None:
    "For p-type guard ring put substrate label for IHP process"
    if gr.type_ == "p":
        p = _geo.Point(
            x=(-0.5*gr.width + 0.5*gr.ringwidth), y=(-0.5*gr.height + 0.5*gr.ringwidth)
        )
        lbl = _geo.Label(origin=p, text="sub!")
        gr.layout.add_shape(
            shape=lbl, layer=cast(_prm.Auxiliary, _prims["TEXT"]), net=None,
        )
    if create_cb:
        create_cb(gr)


# Add diode label and for p-type outer ring put substrate label for IHP process
def dcdiode_create(dio: DCDiodeT, *, create_cb: Optional[Callable[[DCDiodeT], None]]) -> None:
    TEXT = cast(_prm.Auxiliary, _prims["TEXT"])
    if dio.type_ == "n":
        p = _geo.Point(x=0.5*dio.active_width, y=0.5*dio.active_width)
        lbl = _geo.Label(origin=p, text="sub!")
        dio.layout.add_shape(
            shape=lbl, layer=TEXT, net=None,
        )
    if create_cb:
        create_cb(dio)


class PadIn(PadInT):
    "Add PAD label for Calibre ESD diode extraction"
    def _create_layout(self):
        super()._create_layout()

        layout = self.layout
        lbls = []
        for sl in layout._sublayouts:
            if (
                isinstance(sl, _InstanceSubLayout)
                and (sl.inst.cell.name in ("sg13g2_DCNDiode", "sg13g2_DCPDiode"))
            ):
                assert sl.rotation == _geo.Rotation.R90
                lbls.append(_geo.Label(
                    origin=(sl.origin + _geo.Point(x=-(1.5*1.26 + 0.99), y=0.0)),
                    text="PAD",
                ))
        text = cast(_prm.Auxiliary, _prims["TEXT"])
        for lbl in lbls:
            layout.add_shape(shape=lbl, layer=text, net=None)


class OutPadLabelsMixin:
    "Mixin class to support drawing PAD label for IHP Calibre LVS ESD diode detection"
    def pad_labels(self, *, layout: _lay.LayoutT):
        metal2 = cast(_prm.MetalWire, _prims["Metal2"])

        lbls = []
        x = None
        for sl in layout._sublayouts:
            if (
                isinstance(sl, _InstanceSubLayout)
                and sl.inst.cell.name.startswith("sg13g2_Clamp_N")
            ):
                assert sl.rotation == _geo.Rotation.No
                ckt = sl.inst.circuit
                pad = ckt.nets["pad"]
                for ms in sl.layout.filter_polygons(net=pad, mask=metal2.mask, split=True):
                    assert isinstance(ms.shape, _geo.RectangularT)
                    x = ms.shape.center.x
                    break
                break
        assert x is not None
        for sl in layout._sublayouts:
            if (
                isinstance(sl, _InstanceSubLayout)
                and (sl.inst.cell.name in ("sg13g2_DCNDiode", "sg13g2_DCPDiode"))
            ):
                assert sl.rotation == _geo.Rotation.No
                lbls.append(_geo.Label(origin=_geo.Point(x=x, y=sl.origin.y), text="PAD"))
        text = cast(_prm.Auxiliary, _prims["TEXT"])
        for lbl in lbls:
            layout.add_shape(shape=lbl, layer=text, net=None)


class PadOut(PadOutT, OutPadLabelsMixin):
    def _create_layout(self):
        super()._create_layout()
        self.pad_labels(layout=self.layout)


class PadTriOut(PadTriOutT, OutPadLabelsMixin):
    def _create_layout(self):
        super()._create_layout()
        self.pad_labels(layout=self.layout)


class PadInOut(PadInOutT, OutPadLabelsMixin):
    def _create_layout(self):
        super()._create_layout()
        self.pad_labels(layout=self.layout)


