# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from pathlib import Path

from pdkmaster.io.spice import PySpiceFactory

from .spice import prims_spiceparams as _spiceparams


__all__ = ["pyspicefab"]


_file = Path(__file__)
_libfile = _file.parent.joinpath("models", "all.spice")
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
    prims_params=_spiceparams,
)
