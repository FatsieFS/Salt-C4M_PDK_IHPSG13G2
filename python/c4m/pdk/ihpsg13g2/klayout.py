# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
"""Provide KLayout support"""
from typing import Optional

from pdkmaster.io.klayout import PCellLibrary

from .pdkmaster import tech, layoutfab, gds_layers


__all__ = ["register_primlib"]


def register_primlib(*, name: Optional[str]=None):
    if name is None:
        name = f"C4M.{tech.name}Prims"

    # The library will register itself when
    PCellLibrary(name=name, layoutfab=layoutfab, gds_layers=gds_layers)