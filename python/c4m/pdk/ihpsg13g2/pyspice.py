# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from pathlib import Path
from typing import cast

from pdkmaster.technology import primitive as _prm
from pdkmaster.io.spice import SpicePrimsParamSpec, PySpiceFactory

from .pdkmaster import tech as _tech


__all__ = ["prims_spiceparams", "pyspicefab"]


_file = Path(__file__)
_libfile = _file.parent.joinpath("models", "all.spice")
_prims = _tech.primitives
prims_spiceparams = SpicePrimsParamSpec()
for dev_name, params in (
    ("Rsil", dict(sheetres=7.0, model="rsil", is_subcircuit=True)),
    ("Rppd", dict(sheetres=260.0, model="rppd", is_subcircuit=True)),
    ("ndiode", dict(
        model="dantenna", is_subcircuit=True, subcircuit_paramalias={
            "width": "w", "height": "l",
        },
    )),
    ("pdiode", dict(
        # model="dpantenna", is_subcircuit=True, subcircuit_paramalias={
        model="dpantenna", is_subcircuit=True, subcircuit_paramalias={
            "width": "w", "height": "l",
        },
    )),
    ("sg13g2_lv_nmos", dict(model="sg13_lv_nmos", is_subcircuit=True)),
    ("sg13g2_lv_pmos", dict(model="sg13_lv_pmos", is_subcircuit=True)),
    ("sg13g2_hv_nmos", dict(model="sg13_hv_nmos", is_subcircuit=True)),
    ("sg13g2_hv_pmos", dict(model="sg13_hv_pmos", is_subcircuit=True)),
):
    prims_spiceparams.add_device_params(
        prim=cast(_prm.MOSFET, _prims[dev_name]), **params,
    )
pyspicefab = PySpiceFactory(
    libfile=str(_libfile),
    corners=(
        "lvmos_tt", "lvmos_ff", "lvmos_ss", "lvmos_fs", "lvmos_sf",
        "hvmos_tt", "hvmos_ff", "hvmos_ss", "hvmos_fs", "hvmos_sf",
        "res_typ", "res_bcs", "res_wcs",
        "dio",
    ),
    conflicts={
        "lvmos_tt": ("lvmos_ff", "lvmos_ss", "lvmos_fs", "lvmos_sf"),
        "lvmos_ff": ("lvmos_tt", "lvmos_ss", "lvmos_fs", "lvmos_sf"),
        "lvmos_ss": ("lvmos_tt", "lvmos_ff", "lvmos_fs", "lvmos_sf"),
        "lvmos_fs": ("lvmos_tt", "lvmos_ff", "lvmos_ss", "lvmos_sf"),
        "lvmos_sf": ("lvmos_tt", "lvmos_ff", "lvmos_ss", "lvmos_fs"),
        "hvmos_tt": ("hvmos_ff", "hvmos_ss", "hvmos_fs", "hvmos_sf"),
        "hvmos_ff": ("hvmos_tt", "hvmos_ss", "hvmos_fs", "hvmos_sf"),
        "hvmos_ss": ("hvmos_tt", "hvmos_ff", "hvmos_fs", "hvmos_sf"),
        "hvmos_fs": ("hvmos_tt", "hvmos_ff", "hvmos_ss", "hvmos_sf"),
        "hvmos_sf": ("hvmos_tt", "hvmos_ff", "hvmos_ss", "hvmos_fs"),
        "res_typ": ("res_bcs", "res_wcs"),
        "res_bcs": ("res_typ", "res_wcs"),
        "res_wcs": ("res_typ", "res_bcs"),
        "dio": (),
    },
    prims_params=prims_spiceparams,
)
