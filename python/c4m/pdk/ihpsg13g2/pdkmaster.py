# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Tuple, Dict, cast

from pdkmaster.typing import GDSLayerSpecDict
from pdkmaster.technology import (
    property_ as _prp, primitive as _prm, technology_ as _tch
)
from pdkmaster.design import layout as lay, circuit as ckt

__all__ = [
    "tech", "technology", "layoutfab", "layout_factory",
    "cktfab", "circuit_factory", "gds_layers", "textgds_layers", #"plotter",
]


class _IHPSG13G2(_tch.Technology):
    @property
    def name(self):
        return "IHPSG13G2"
    @property
    def grid(self):
        return 0.005

    def __init__(self):
        prims = _prm.Primitives(_prm.Base(type_=_prm.pBase))

        # TODO: angle design rules

        pin_prims = {
            name: _prm.Marker(name=f"{name}.pin")
            for name in (
                "Activ", "GatPoly",
                *(f"Metal{n}" for n in range(1, 5 + 1)),
                *(f"TopMetal{n}" for n in range(1, 2 + 1)),
                # "Passiv",
            )
        }
        prims += pin_prims.values()

        obs_prims: Dict[str, _prm.Marker] = {
            name: _prm.Marker(name=f"{name}.obs")
            for name in (
                "Activ", "GatPoly", "Cont",
                *(f"Metal{n}" for n in range(1, 5 + 1)),
                *(f"Via{n}" for n in range(1, 4 + 1)),
                *(f"TopMetal{n}" for n in range(1, 2 + 1)),
                *(f"TopVia{n}" for n in range(1, 2 + 1)),
            )
        }
        prims += obs_prims.values()

        # single mask based primitives
        NWell = _prm.Well(
            name="NWell", type_=_prm.nImpl,
            min_width=0.62, # NW.a
            min_space=0.62, # NW.b
        )
        pSD = _prm.Implant(
            name="pSD", type_=_prm.pImpl,
            min_width=0.31, # pSD.a
            min_space=0.31, # pSD.b
            min_area=0.25, # pSD.k
            # min_hole_area=0.25, # pSD.l
        )
        ThickGateOx = _prm.Insulator(
            name="ThickGateOx",
            min_width=0.86, # TGO.f
            min_space=0.86, # TGO.e
        )
        # We define EXTBlock as adjust implant as it needs to be extended over GatPoly
        EXTBlock = _prm.Implant(
            name="EXTBlock", # 3.12
            type_=_prm.adjImpl,
            min_width=0.31, # EXT.a
            min_space=0.31, # EXT.b
        )
        # Recognition layers
        RES = _prm.Marker(name="RES")
        SalBlock = _prm.ExtraProcess(
            name="SalBlock", # 3.13
            min_width=0.42, # Sal.a
            min_space=0.42, # Sal.b
        )
        # Substrate net separation layer
        Substrate = _prm.SubstrateMarker(name="Substrate")
        prims += (
            NWell, pSD, ThickGateOx, EXTBlock, RES, SalBlock, Substrate,
        )

        # layers diff and tap will be generated out of Activ
        Activ = _prm.WaferWire(
            name="Activ", pin=pin_prims["Activ"], blockage=obs_prims["Activ"],
            min_width=0.15, # Act.a
            min_space=0.21, # Act.b
            min_area=0.122, # Act.d
            # min_hole_area=0.15, # Act.e
            allow_in_substrate=True, well=NWell, implant=pSD,
            min_implant_enclosure=_prp.Enclosure(0.18), # pSD.c
            implant_abut="none",
            allow_contactless_implant=False,
            # TODO: switch back minimum well enclosure for core cells
            min_well_enclosure=_prp.Enclosure(0.31), # NW.c
            min_well_enclosure4oxide={
                ThickGateOx: _prp.Enclosure(0.62), # NW.c1
            },
            min_substrate_enclosure=_prp.Enclosure(0.31), # NW.d
            min_substrate_enclosure4oxide={
                ThickGateOx: _prp.Enclosure(0.62), # NW.d1
            },
            min_well_enclosure_same_type=_prp.Enclosure(0.03), # pSD.d1
            min_substrate_enclosure_same_type=_prp.Enclosure(0.03), # pSD.sc1
            allow_well_crossing=False,
            oxide=ThickGateOx,
            min_oxide_enclosure=_prp.Enclosure(0.27), # TGO.a
        )
        GatPoly = _prm.GateWire(
            name="GatPoly", pin=pin_prims["GatPoly"], blockage=obs_prims["GatPoly"],
            min_width=0.13, # Gat.a
            min_space=0.18, # Gat.b
            min_area=0.09, # Gat.e
            # IHP will do dummy insertion
            # min_density=0.15, # GFil.g
        )
        # wires
        metals: Dict[str, _prm.MetalWire] = {
            name: _prm.MetalWire(name=name, **wire_args) for name, wire_args in (
                ("Metal1", {
                    "pin": pin_prims["Metal1"],
                    "blockage": obs_prims["Metal1"],
                    "min_width": 0.16, # M1.a
                    "min_space": 0.18, # M1.b
                    "space_table": (
                        ((0.3, 1.0), 0.22), # M1.e
                        ((10.0, 10.0), 0.60), # M1.f
                    ),
                    "min_area": 0.09 # M1.d
                    # IHP will do dummy insertion
                    # "min_density": 0.35, # M1.j
                    # "max_density": 0.60, # M1.k
                    # TODO: M1.g/i 45deg line
                }),
                *(
                    (metal, {
                        "pin": pin_prims[metal],
                        "blockage": obs_prims[metal],
                        "min_width": 0.20, # Mn.a
                        "min_space": 0.21, # Mn.b
                        "space_table": (
                            ((0.39, 1.0), 0.24), # Mn.e
                            ((10.0, 10.0), 0.60), # Mn.f
                        ), # m1.3a+b, m2.3a+b
                        "min_area": 0.144 # Mn.d
                        # IHP will do dummy insertion
                        # "min_density": 0.35, # Mn.j
                        # "max_density": 0.60, # Mn.k
                        # TODO: Mn.g/i 45deg line
                    }) for metal in (f"Metal{n}" for n in range(2, 5 + 1))
                ),
                ("TopMetal1", {
                    "pin": pin_prims["TopMetal1"],
                    "blockage": obs_prims["TopMetal1"],
                    "min_width": 1.64, # TM1.a
                    "min_space": 1.64, # TM1.b
                    # IHP will do dummy insertion
                    # "min_density": 0.25, # TM1.c
                    # "max_density": 0.70, # TM1.d
                }),
                ("TopMetal2", {
                    "pin": pin_prims["TopMetal2"],
                    "blockage": obs_prims["TopMetal2"],
                    "min_width": 2.00, # TM2.a
                    "min_space": 2.00, # TM2.b
                    "space_table": (
                        ((5.0, 50.0), 5.0), # TM2.b1R
                    ),
                    # IHP will do dummy insertion
                    # "min_density": 0.25, # TM1.c
                    # "max_density": 0.70, # TM1.d
                }),
            )
        }
        # TODO: RDL option
        prims += (Activ, GatPoly, *metals.values())

        # vias
        vias: Dict[str, _prm.Via] = {
            via_args["name"]: _prm.Via(**via_args) for via_args in (
                {
                    "name": "Cont",
                    "blockage": obs_prims["Cont"],
                    "width": 0.16, # Cnt.a
                    "min_space": 0.18, # Cnt.b
                    "bottom": (Activ, GatPoly),
                    "top": metals["Metal1"],
                    "min_bottom_enclosure": (
                        _prp.Enclosure(0.07), # Cnt.c
                        _prp.Enclosure(0.07), # Cnt.d
                    ),
                    "min_top_enclosure": _prp.Enclosure((0.000, 0.080)), # li.5.-
                },
                {
                    "name": "Via1",
                    "blockage": obs_prims["Via1"],
                    "width": 0.19, # V1.a
                    "min_space": 0.22, # V1.b
                    "bottom": metals["Metal1"],
                    "top": metals["Metal2"],
                    # TODO: allow single side bigger enclosure
                    "min_bottom_enclosure": _prp.Enclosure((0.01, 0.05)), # V1.c/c1
                    "min_top_enclosure": _prp.Enclosure((0.005, 0.05)), # Mn.c/c1
                },
                *(
                    {
                        "name": f"Via{n}",
                        "blockage": obs_prims[f"Via{n}"],
                        "width": 0.19, # Vn.a
                        "min_space": 0.22, # Vn.b
                        "bottom": metals[f"Metal{n}"],
                        "top": metals[f"Metal{n + 1}"],
                        # TODO: allow single side bigger enclosure
                        "min_bottom_enclosure": _prp.Enclosure((0.005, 0.05)), # Mn.c/c1
                        "min_top_enclosure": _prp.Enclosure((0.005, 0.05)), # Vn.c/c1
                    } for n in range(2, 4 + 1)
                ),
                {
                    "name": "TopVia1",
                    "blockage": obs_prims["TopVia1"],
                    "width": 0.42, # TV1.a
                    "min_space": 0.42, # TV1.b
                    "bottom": metals["Metal5"],
                    "top": metals["TopMetal1"],
                    "min_bottom_enclosure": _prp.Enclosure(0.01), # TV1.c
                    "min_top_enclosure": _prp.Enclosure(0.42), # TV1.d
                },
                {
                    "name": "TopVia2",
                    "blockage": obs_prims["TopVia2"],
                    "width": 0.9, # TV2.a
                    "min_space": 1.06, # TV2.b
                    "bottom": metals["TopMetal1"],
                    "top": metals["TopMetal2"],
                    "min_bottom_enclosure": _prp.Enclosure(0.5), # TV2.c
                    "min_top_enclosure": _prp.Enclosure(0.5), # TV2.d
                },
            )
        }
        Passiv = _prm.PadOpening(
            name="Passiv", #pin=pin_prims["Passiv"],
            # TODO: Can min_width be reduced ?
            min_width=40.000, # Own rule
            # min_width=2.1, # Pas.a
            min_space=3.5, # Pas.b
            bottom=metals["TopMetal2"],
            min_bottom_enclosure=_prp.Enclosure(2.1), # Pas.c
        )
        prims += (*vias.values(), Passiv)

        # misc using wires
        prims += (
            # extra space rules
            _prm.Spacing( # pSD.d
                primitives1=Activ, primitives2=pSD, min_space=0.18,
            ),
            _prm.Spacing( # NW.f
                primitives1=NWell, primitives2=Activ, min_space=0.24,
            ),
            _prm.Spacing( # TGO.b
                primitives1=Activ, primitives2=ThickGateOx, min_space=0.27,
            ),
            _prm.Spacing( # Gat.d
                primitives1=Activ, primitives2=GatPoly, min_space=0.07,
            ),
            _prm.Spacing( # Cnt.e
                primitives1=vias["Cont"], primitives2=Activ, min_space=0.14,
            ),
            _prm.Spacing( # Sal.d
                primitives1=SalBlock, primitives2=(Activ, GatPoly, vias["Cont"]),
                min_space=0.2,
            ),
            _prm.Spacing( # EXT.c
                primitives1=EXTBlock, primitives2=pSD, min_space=0.31,
            ),
            _prm.Spacing( # Rsil.e
                primitives1=GatPoly, primitives2=EXTBlock, min_space=0.18,
            )
        )

        # resistors
        prims += (
            _prm.Resistor(name="Rsil", # 4.4
                min_width=0.5, # Rsil.a
                min_length=0.5,  # Rsil.f
                wire=GatPoly,
                indicator=RES,
                min_indicator_extension=0.0, # Rsil.c
                contact=vias["Cont"],
                min_contact_space=0.12, # Rsil.b
                # Rsil.d covered by pSD.d above
                # TODO: Rsil.e after EXTBlock has been added
            ),
            _prm.Resistor(name="Rppd", # 4.5
                min_width=0.5, # Rppd.a
                min_length=0.5,  # Rppd.e
                wire=GatPoly,
                indicator=SalBlock,
                min_indicator_extension=0.2, # Sal.c
                implant=(pSD, EXTBlock),
                min_implant_enclosure=(
                    _prp.Enclosure(0.18), # Rppd.b
                    _prp.Enclosure(0.18), # Rppd.d
                ),
                contact=vias["Cont"],
                min_contact_space=0.2, # Rppd.c
            ),
        )

        # diodes
        recog_dio = _prm.Marker(name="Recog.dio")
        prims += (
            recog_dio,
            _prm.Diode(
                name="ndiode", wire=Activ,
                min_width=0.48, # rule not yet in DRM
                indicator=recog_dio,
                min_indicator_enclosure=_prp.Enclosure(0.02), # From GDSII
                implant=(), min_implant_enclosure=(),
            ),
            _prm.Diode(
                name="pdiode", wire=Activ,
                min_width=0.48, # rule not yet in DRM
                indicator=recog_dio,
                min_indicator_enclosure=_prp.Enclosure(0.02), # From GDSII
                implant=pSD, min_implant_enclosure=(),
                well=NWell,
            ),
        )

        # transistors
        lvmosgate = _prm.MOSFETGate(name="lvmosgate",
            active=Activ, poly=GatPoly,
            # No need for overruling min_l or min_w
            min_sd_width=0.23, # Act.c
            min_polyactive_extension=0.18, # Gat.c
            contact=vias["Cont"],
            min_contactgate_space=0.11, # Cnt.f
        )
        hvmosgate = _prm.MOSFETGate(name="hvmosgate",
            active=Activ, poly=GatPoly, oxide=ThickGateOx,
            # TODO: support min_l = 0.4 for PMOS and 0.45 for NMOS
            min_l=0.45, # Gat.a3/a4
            min_w=0.30, # from transistor model
            max_w=10.0, # from transistor model
            min_gate_space=0.25, # Gat.b1
            min_gateoxide_enclosure=_prp.Enclosure((0.34, 0.26)),
            min_sd_width=0.23, # Act.c
            min_polyactive_extension=0.18, # Gat.c
            contact=vias["Cont"],
            min_contactgate_space=0.11, # Cnt.f
        )
        trans = {
            name: _prm.MOSFET(name=name,
                gate=gate, implant=impl, well=well,
                min_gateimplant_enclosure=impl_enc, # Implant.1
            )
            for name, gate, well, impl, impl_enc in (
                ("sg13g2_lv_nmos", lvmosgate, None, (), ()),
                ("sg13g2_lv_pmos", lvmosgate, NWell, pSD, _prp.Enclosure(0.30)), # pSD.i
                ("sg13g2_hv_nmos", hvmosgate, None, (), ()),
                ("sg13g2_hv_pmos", hvmosgate, NWell, pSD, _prp.Enclosure(0.40)), # pSD.i1
            )
        }
        prims += (lvmosgate, hvmosgate, *trans.values())

        # Gate spacing rules
        sg13g2_lv_nmos = cast(_prm.MOSFET, prims.sg13g2_lv_nmos)
        sg13g2_hv_nmos = cast(_prm.MOSFET, prims.sg13g2_hv_nmos)
        prims += (
            _prm.Spacing( # pSD.j
                primitives1=sg13g2_lv_nmos.gate4mosfet, primitives2=pSD, min_space=0.3,
            ),
            _prm.Spacing( # pSD.j1
                primitives1=sg13g2_hv_nmos.gate4mosfet, primitives2=pSD, min_space=0.4,
            ),
        )
        prims += (_prm.Auxiliary(name=name) for name in ("TEXT", "prBoundary"))

        # ESD
        # Use Auxiliary for ESD recognition layer as it is currently
        # not used in another primitive
        prims += _prm.Auxiliary(name="Recog.esd")

        super().__init__(primitives=prims)

tech = technology = _IHPSG13G2()
cktfab = circuit_factory = ckt.CircuitFactory(tech=tech)

def _primlayout_cb(*, layout: lay.LayoutT, prim: _prm.PrimitiveT, **prim_args):
    from pdkmaster.technology import geometry as _geo
    if isinstance(prim, _prm.Resistor):
        w = prim_args["width"]
        l = prim_args["length"]
        if prim.name == "Rppd":
            sheet = 396.917
        elif prim.name == "Rsil":
            sheet = 24.863
        else:
            raise NotImplementedError(
                f"resistance computation for Resistor '{prim.name}'",
            )

        r = sheet*l/w
        if r > 1000.0:
            r /= 1000.0
            s = f"{r:.3f}k"
        else:
            s = f"{r:.3f}"
        ms = _geo.MaskShape(
            mask=cast(_prm.DesignMaskPrimitiveT, tech.primitives["TEXT"]).mask,
            shape=_geo.Label(origin=_geo.origin, text=f"{prim.name.lower()} r={s}"),
        )
        layout.add_shape(shape=ms, net=None)
    elif isinstance(prim, _prm.Diode):
        if prim.name == "ndiode":
            lbl = "dant"
        elif prim.name == "pdiode":
            lbl = "dpant"
        else:
            raise NotImplementedError(f"label for Dioce '{prim.name}'")
        ms = _geo.MaskShape(
            mask=cast(_prm.DesignMaskPrimitiveT, tech.primitives["TEXT"]).mask,
            shape=_geo.Label(origin=_geo.origin, text=lbl),
        )
        layout.add_shape(shape=ms, net=None)
layoutfab = layout_factory = lay.LayoutFactory(tech=tech, create_cb=_primlayout_cb)

gds_layers: GDSLayerSpecDict = {
    "Recog.esd": (99, 30),
    "Recog.dio": (99, 31),
}
textgds_layers: GDSLayerSpecDict = {}

# Use datatype 100 for obstruction layer;
# datatype 23 'nofill' would cause no dummy generation if accidently not removed before tape-out
for name, layer, has_pin, has_obs, has_pintext in (
    ("Activ", 1, True, True, False),
    ("GatPoly", 5, True, True, False),
    ("Cont", 6, False, True, False),
    ("Metal1", 8, True, True, True),
    ("Passiv", 9, True, False, False),
    ("Metal2", 10, True, True, True),
    ("pSD", 14, False, False, False),
    ("Via1", 19, False, True, False),
    ("RES", 24, False, False, False),
    ("SalBlock", 28, False, False, False),
    ("Via2", 29, False, True, False),
    ("Metal3", 30, True, True, True),
    ("NWell", 31, False, False, False),
    ("Substrate", 40, False, False, False),
    ("ThickGateOx", 44, False, False, False),
    ("Via3", 49, False, True, False),
    ("Metal4", 50, True, True, True),
    ("TEXT", 63, False, False, False),
    ("Via4", 66, False, True, False),
    ("Metal5", 67, True, True, True),
    ("EXTBlock", 111, False, False, False),
    ("TopVia1", 125, False, True, False),
    ("TopMetal1", 126, True, True, True),
    ("TopVia2", 133, False, True, False),
    ("TopMetal2", 134, True, True, True),
    ("prBoundary", 189, False, False, False),
):
    gds_layers[name] = (layer, 0)
    if has_pin:
        gds_layers[f"{name}.pin"] = (layer, 2)
    if has_pintext:
        textgds_layers[f"{name}.pin"] = (layer, 25)
    if has_obs:
        gds_layers[f"{name}.obs"] = (layer, 100)
