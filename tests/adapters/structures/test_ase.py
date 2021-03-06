# pylint: disable=import-error
import json
from pathlib import Path
import re
from typing import List

import pytest

from .utils import get_min_ver

min_ver = get_min_ver("ase")
ase = pytest.importorskip(
    "ase",
    minversion=min_ver,
    reason=f"ase must be installed with minimum version {min_ver} for these tests to"
    " be able to run",
)

from ase import Atoms

from optimade.models.structures import Periodicity

from optimade.adapters import Structure
from optimade.adapters.exceptions import ConversionError
from optimade.adapters.structures.ase import get_ase_atoms


def test_successful_conversion(RAW_STRUCTURES):
    """Make sure its possible to convert"""
    for structure in RAW_STRUCTURES:
        assert isinstance(get_ase_atoms(Structure(structure)), Atoms)


def test_null_positions(null_position_structure):
    """Make sure null positions are handled"""
    assert isinstance(get_ase_atoms(null_position_structure), Atoms)


def test_null_lattice_vectors(null_lattice_vector_structure):
    """Make sure null lattice vectors are handled"""
    assert isinstance(get_ase_atoms(null_lattice_vector_structure), Atoms)


def test_special_species(SPECIAL_SPECIES_STRUCTURES):
    """Make sure vacancies and non-chemical symbols ("X") are handled"""
    for special_structure in SPECIAL_SPECIES_STRUCTURES:
        structure = Structure(special_structure)

        with pytest.raises(
            ConversionError,
            match="ASE cannot handle structures with partial occupancies",
        ):
            get_ase_atoms(structure)
