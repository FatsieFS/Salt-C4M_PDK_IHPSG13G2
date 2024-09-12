# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from pdkmaster.io.spice import SpicePrimsParamSpec, SpiceNetlistFactory

from .pdkmaster import tech as _tech


__all__ = ["prims_spiceparams", "netlistfab"]


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
        prim=_prims[dev_name], **params, # type: ignore
    )
netlistfab = SpiceNetlistFactory(params=prims_spiceparams)
