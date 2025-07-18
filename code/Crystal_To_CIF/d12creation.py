#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared Module for D12 File Creation
-----------------------------------
This module contains shared constants, utilities, and functions for creating
D12 input files for CRYSTAL23. It is used by both CRYSTALOptToD12.py and
NewCifToD12.py to avoid code duplication.

AUTHOR:
    Marcus Djokic
"""

import os
import numpy as np


# Element class and atomic data
class Element:
    """Element atomic numbers for easy reference"""

    H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P = list(range(1, 16))
    S, Cl, Ar, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn = list(range(16, 31))
    Ga, Ge, As, Se, Br, Kr, Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru = list(range(31, 45))
    Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe, Cs, Ba, La, Ce = list(range(45, 59))
    Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf = list(range(59, 73))
    Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn = list(range(73, 87))
    Fr, Ra, Ac, Th, Pa, U, Np, Pu, Am, Cm, Bk, Cf, Es, Fm = list(range(87, 101))
    Md, No, Lr, Rf, Db, Sg, Bh, Hs, Mt, Ds, Rg, Cn, Uut = list(range(101, 114))
    Fl, Uup, Lv, Uus, Uuo = list(range(114, 119))


# Dictionary mapping element symbols to atomic numbers
ELEMENT_SYMBOLS = {
    "H": 1,
    "He": 2,
    "Li": 3,
    "Be": 4,
    "B": 5,
    "C": 6,
    "N": 7,
    "O": 8,
    "F": 9,
    "Ne": 10,
    "Na": 11,
    "Mg": 12,
    "Al": 13,
    "Si": 14,
    "P": 15,
    "S": 16,
    "Cl": 17,
    "Ar": 18,
    "K": 19,
    "Ca": 20,
    "Sc": 21,
    "Ti": 22,
    "V": 23,
    "Cr": 24,
    "Mn": 25,
    "Fe": 26,
    "Co": 27,
    "Ni": 28,
    "Cu": 29,
    "Zn": 30,
    "Ga": 31,
    "Ge": 32,
    "As": 33,
    "Se": 34,
    "Br": 35,
    "Kr": 36,
    "Rb": 37,
    "Sr": 38,
    "Y": 39,
    "Zr": 40,
    "Nb": 41,
    "Mo": 42,
    "Tc": 43,
    "Ru": 44,
    "Rh": 45,
    "Pd": 46,
    "Ag": 47,
    "Cd": 48,
    "In": 49,
    "Sn": 50,
    "Sb": 51,
    "Te": 52,
    "I": 53,
    "Xe": 54,
    "Cs": 55,
    "Ba": 56,
    "La": 57,
    "Ce": 58,
    "Pr": 59,
    "Nd": 60,
    "Pm": 61,
    "Sm": 62,
    "Eu": 63,
    "Gd": 64,
    "Tb": 65,
    "Dy": 66,
    "Ho": 67,
    "Er": 68,
    "Tm": 69,
    "Yb": 70,
    "Lu": 71,
    "Hf": 72,
    "Ta": 73,
    "W": 74,
    "Re": 75,
    "Os": 76,
    "Ir": 77,
    "Pt": 78,
    "Au": 79,
    "Hg": 80,
    "Tl": 81,
    "Pb": 82,
    "Bi": 83,
    "Po": 84,
    "At": 85,
    "Rn": 86,
    "Fr": 87,
    "Ra": 88,
    "Ac": 89,
    "Th": 90,
    "Pa": 91,
    "U": 92,
    "Np": 93,
    "Pu": 94,
    "Am": 95,
    "Cm": 96,
    "Bk": 97,
    "Cf": 98,
    "Es": 99,
    "Fm": 100,
}

# Reverse mapping for element symbols
ATOMIC_NUMBER_TO_SYMBOL = {v: k for k, v in ELEMENT_SYMBOLS.items()}

# Space group symbol to number mapping (Hermann-Mauguin symbols)
SPACEGROUP_SYMBOLS = {
    # Triclinic
    "P 1": 1,
    "P -1": 2,
    # Monoclinic
    "P 2": 3,
    "P 21": 4,
    "C 2": 5,
    "P M": 6,
    "P C": 7,
    "C M": 8,
    "C C": 9,
    "P 2/M": 10,
    "P 21/M": 11,
    "C 2/M": 12,
    "P 2/C": 13,
    "P 21/C": 14,
    "C 2/C": 15,
    # Orthorhombic (selected)
    "P 2 2 2": 16,
    "P 2 2 21": 17,
    "P 21 21 21": 19,
    "C 2 2 21": 20,
    "C 2 2 2": 21,
    "F 2 2 2": 22,
    "I 2 2 2": 23,
    "P M M M": 47,
    "P N N N": 48,
    "P B A N": 50,
    "P N M A": 62,
    "C M C M": 63,
    "C M C A": 64,
    "C M M M": 65,
    "F M M M": 69,
    "F D D D": 70,
    "I M M M": 71,
    "I B A M": 72,
    "I B C A": 73,
    "I M M A": 74,
    # Tetragonal (selected)
    "P 4": 75,
    "P 41": 76,
    "P 42": 77,
    "P 43": 78,
    "I 4": 79,
    "I 41": 80,
    "P -4": 81,
    "I -4": 82,
    "P 4/M": 83,
    "P 42/M": 84,
    "P 4/N": 85,
    "I 4/M": 87,
    "I 41/A": 88,
    "P 4 2 2": 89,
    "P 41 2 2": 91,
    "P 42 2 2": 93,
    "I 4 2 2": 97,
    "I 41 2 2": 98,
    "P 4 M M": 99,
    "P 4/M M M": 123,
    "P 4/M C C": 124,
    "P 42/M M C": 131,
    "P 42/M C M": 132,
    "I 4/M M M": 139,
    "I 4/M C M": 140,
    "I 41/A M D": 141,
    "I 41/A C D": 142,
    # Trigonal (selected)
    "P 3": 143,
    "P 31": 144,
    "P 32": 145,
    "R 3": 146,
    "P -3": 147,
    "R -3": 148,
    "P 3 1 2": 149,
    "P 3 2 1": 150,
    "R 3 2": 155,
    "P 3 M 1": 156,
    "P -3 1 M": 162,
    "P -3 1 C": 163,
    "P -3 M 1": 164,
    "P -3 C 1": 165,
    "R -3 M": 166,
    "R -3 C": 167,
    # Hexagonal (selected)
    "P 6": 168,
    "P 61": 169,
    "P 62": 171,
    "P 63": 173,
    "P -6": 174,
    "P 6/M": 175,
    "P 63/M": 176,
    "P 6 2 2": 177,
    "P 61 2 2": 178,
    "P 6 M M": 183,
    "P 6 C C": 184,
    "P 6/M M M": 191,
    "P 6/M C C": 192,
    "P 63/M C M": 193,
    "P 63/M M C": 194,
    # Cubic
    "P 2 3": 195,
    "F 2 3": 196,
    "I 2 3": 197,
    "P 21 3": 198,
    "I 21 3": 199,
    "P M 3": 200,
    "P N 3": 201,
    "F M 3": 202,
    "F D 3": 203,
    "I M 3": 204,
    "P A 3": 205,
    "I A 3": 206,
    "P 4 3 2": 207,
    "P 42 3 2": 208,
    "F 4 3 2": 209,
    "F 41 3 2": 210,
    "I 4 3 2": 211,
    "P 43 3 2": 212,
    "P 41 3 2": 213,
    "I 41 3 2": 214,
    "P -4 3 M": 215,
    "F -4 3 M": 216,
    "I -4 3 M": 217,
    "P -4 3 N": 218,
    "F -4 3 C": 219,
    "I -4 3 D": 220,
    "P M 3 M": 221,
    "P N 3 N": 222,
    "P M 3 N": 223,
    "P N 3 M": 224,
    "F M 3 M": 225,
    "F M 3 C": 226,
    "F D 3 M": 227,
    "F D 3 C": 228,
    "I M 3 M": 229,
    "I A 3 D": 230,
}

# Alternative spellings and common variations
SPACEGROUP_ALTERNATIVES = {
    "P1": 1,
    "P-1": 2,
    "P2": 3,
    "P21": 4,
    "C2": 5,
    "PM": 6,
    "PC": 7,
    "CM": 8,
    "CC": 9,
    "P2/M": 10,
    "P21/M": 11,
    "C2/M": 12,
    "P2/C": 13,
    "P21/C": 14,
    "C2/C": 15,
    # Orthorhombic variations
    "P222": 16,
    "P2221": 17,
    "P212121": 19,
    "C2221": 20,
    "C222": 21,
    "F222": 22,
    "I222": 23,
    "Pmmm": 47,
    "Pnnn": 48,
    "Pban": 50,
    "Pnma": 62,
    "Cmcm": 63,
    "Cmca": 64,
    "Cmmm": 65,
    "Fmmm": 69,
    "Fddd": 70,
    "Immm": 71,
    "Ibam": 72,
    "Ibca": 73,
    "Imma": 74,
    # Tetragonal variations
    "P4": 75,
    "P41": 76,
    "P42": 77,
    "P43": 78,
    "I4": 79,
    "I41": 80,
    "P-4": 81,
    "I-4": 82,
    "P4/m": 83,
    "P42/m": 84,
    "P4/n": 85,
    "I4/m": 87,
    "I41/a": 88,
    "P422": 89,
    "P4122": 91,
    "P4222": 93,
    "I422": 97,
    "I4122": 98,
    "P4mm": 99,
    "P4/mmm": 123,
    "P4/mcc": 124,
    "P42/mmc": 131,
    "P42/mcm": 132,
    "I4/mmm": 139,
    "I4/mcm": 140,
    "I41/amd": 141,
    "I41/acd": 142,
    # Trigonal variations
    "P3": 143,
    "P31": 144,
    "P32": 145,
    "R3": 146,
    "P-3": 147,
    "R-3": 148,
    "P312": 149,
    "P321": 150,
    "R32": 155,
    "P3m1": 156,
    "P-31m": 162,
    "P-31c": 163,
    "P-3m1": 164,
    "P-3c1": 165,
    "R-3m": 166,
    "R-3c": 167,
    # Hexagonal variations
    "P6": 168,
    "P61": 169,
    "P62": 171,
    "P63": 173,
    "P-6": 174,
    "P6/m": 175,
    "P63/m": 176,
    "P622": 177,
    "P6122": 178,
    "P6mm": 183,
    "P6cc": 184,
    "P6/mmm": 191,
    "P6/mcc": 192,
    "P63/mcm": 193,
    "P63/mmc": 194,
    # Cubic variations
    "P23": 195,
    "F23": 196,
    "I23": 197,
    "P213": 198,
    "I213": 199,
    "Pm3": 200,
    "Pn3": 201,
    "Fm3": 202,
    "Fd3": 203,
    "Im3": 204,
    "Pa3": 205,
    "Ia3": 206,
    "P432": 207,
    "P4232": 208,
    "F432": 209,
    "F4132": 210,
    "I432": 211,
    "P4332": 212,
    "P4132": 213,
    "I4132": 214,
    "P-43m": 215,
    "F-43m": 216,
    "I-43m": 217,
    "P-43n": 218,
    "F-43c": 219,
    "I-43d": 220,
    "Pm3m": 221,
    "Pn3n": 222,
    "Pm3n": 223,
    "Pn3m": 224,
    "Fm3m": 225,
    "Fm3c": 226,
    "Fd3m": 227,
    "Fd3c": 228,
    "Im3m": 229,
    "Ia3d": 230,
    # More cubic variations with different formatting
    "FM3M": 225,
    "FM-3M": 225,
    "Fm-3m": 225,
    "FD3M": 227,
    "FD-3M": 227,
    "Fd-3m": 227,
    "IM3M": 229,
    "IM-3M": 229,
    "Im-3m": 229,
    "IA3D": 230,
    "IA-3D": 230,
    "Ia-3d": 230,
}

# Space groups with multiple origin settings that need special handling
MULTI_ORIGIN_SPACEGROUPS = {
    216: {"name": "F-43m", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    218: {"name": "P-43n", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    221: {"name": "Pm-3m", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    225: {"name": "Fm-3m", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    227: {
        "name": "Fd-3m",
        "default": "Origin 2 (ITA)",
        "crystal_code": "0 0 0",
        "alt": "Origin 1",
        "alt_crystal_code": "0 0 1",
        "default_pos": (0.125, 0.125, 0.125),
        "alt_pos": (0.0, 0.0, 0.0),
    },
    228: {"name": "Fd-3c", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    229: {"name": "Im-3m", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
    230: {"name": "Ia-3d", "default": "Origin 2 (ITA)", "crystal_code": "0 0 0"},
}

RHOMBOHEDRAL_SPACEGROUPS = [146, 148, 155, 160, 161, 166, 167]

# Elements that require ECPs in external basis sets (DZVP-REV2 and TZVP-REV2)
ECP_ELEMENTS_EXTERNAL = [
    37,
    38,
    39,
    40,
    41,
    42,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
]

# Available internal basis sets with element ranges and core types
INTERNAL_BASIS_SETS = {
    # Standard basis sets (original 7)
    "STO-3G": {
        "description": "Pople's standard minimal basis set (3 Gaussian function contractions)",
        "elements": list(range(1, 54)),  # H to I
        "all_electron": list(range(1, 54)),
        "ecp_elements": [],
        "standard": True,
    },
    "STO-6G": {
        "description": "Pople's standard minimal basis set (6 Gaussian function contractions)",
        "elements": list(range(1, 37)),  # H to Kr
        "all_electron": list(range(1, 37)),
        "ecp_elements": [],
        "standard": True,
    },
    "POB-DZVP": {
        "description": "POB Double-ζ + polarization basis set",
        "elements": list(range(1, 36)) + [49, 74],  # H to Br, In, W
        "all_electron": list(range(1, 19)),  # H to Ar
        "ecp_elements": list(range(19, 36)) + [49, 74],  # K onwards need ECP
        "standard": True,
    },
    "POB-DZVPP": {
        "description": "POB Double-ζ + double set of polarization functions",
        "elements": list(range(1, 36)) + [49, 83],  # H to Br, In, Bi
        "all_electron": list(range(1, 19)),  # H to Ar
        "ecp_elements": list(range(19, 36)) + [49, 83],  # K onwards need ECP
        "standard": True,
    },
    "POB-TZVP": {
        "description": "POB Triple-ζ + polarization basis set",
        "elements": list(range(1, 36)) + [49, 83],  # H to Br, In, Bi
        "all_electron": list(range(1, 19)),  # H to Ar
        "ecp_elements": list(range(19, 36)) + [49, 83],  # K onwards need ECP
        "standard": True,
    },
    "POB-DZVP-REV2": {
        "description": "POB-REV2 Double-ζ + polarization basis set",
        "elements": list(range(1, 36)),  # H to Br
        "all_electron": list(range(1, 19)),  # H to Ar
        "ecp_elements": list(range(19, 36)),  # K onwards need ECP
        "standard": True,
    },
    "POB-TZVP-REV2": {
        "description": "POB-REV2 Triple-ζ + polarization basis set",
        "elements": list(range(1, 36))
        + list(range(37, 54))
        + [55, 56]
        + list(range(72, 85)),
        "all_electron": list(range(1, 19)),  # H to Ar
        "ecp_elements": list(range(19, 36))
        + list(range(37, 54))
        + [55, 56]
        + list(range(72, 85)),
        "standard": True,
    },
    # Additional basis sets
    "MINIS": {
        "description": "Minimal basis set; primarily for testing and preliminary calculations",
        "elements": list(range(1, 37)),  # H to Kr
        "all_electron": list(range(1, 37)),
        "ecp_elements": [],
        "standard": False,
    },
    "6-31G*": {
        "description": "Split-valence double-zeta with polarization",
        "elements": list(range(1, 31)),  # H to Zn
        "all_electron": list(range(1, 31)),
        "ecp_elements": [],
        "standard": False,
    },
    "def2-SV(P)": {
        "description": "Split-valence with polarization on heavy atoms",
        "elements": list(range(1, 87)),  # H to Rn
        "all_electron": list(range(1, 37)),  # H to Kr
        "ecp_elements": list(range(37, 87)),  # Rb onwards need def2-ECP
        "standard": False,
    },
    "def2-SVP": {
        "description": "Split-valence with polarization; widely used",
        "elements": list(range(1, 87)),  # H to Rn
        "all_electron": list(range(1, 37)),  # H to Kr
        "ecp_elements": list(range(37, 87)),  # Rb onwards need def2-ECP
        "standard": False,
    },
    "def-TZVP": {
        "description": "Triple-zeta valence with polarization",
        "elements": list(range(1, 87)),  # H to Rn
        "all_electron": list(range(1, 37)),  # H to Kr
        "ecp_elements": list(range(37, 87)),  # Rb onwards need def2-ECP
        "standard": False,
    },
    "def2-TZVP": {
        "description": "Enhanced triple-zeta valence with polarization",
        "elements": list(range(1, 87)),  # H to Rn
        "all_electron": list(range(1, 37)),  # H to Kr
        "ecp_elements": list(range(37, 87)),  # Rb onwards need def2-ECP
        "standard": False,
    },
}

# Functional categories with complete descriptions
FUNCTIONAL_CATEGORIES = {
    "HF": {
        "name": "Hartree-Fock Methods",
        "description": "Wave function based methods (no DFT)",
        "functionals": ["RHF", "UHF", "HF3C", "HFSOL3C"],
        "basis_requirements": {"HF3C": "MINIX", "HFSOL3C": "SOLMINIX"},
        "descriptions": {
            "RHF": "Restricted Hartree-Fock (closed shell)",
            "UHF": "Unrestricted Hartree-Fock (open shell)",
            "HF3C": "Minimal basis HF with D3, gCP, and SRB corrections",
            "HFSOL3C": "HF3C revised for inorganic solids",
        },
    },
    "LDA": {
        "name": "LDA/LSD Functionals",
        "description": "Local (Spin) Density Approximation functionals",
        "functionals": ["SVWN", "VBH"],
        "descriptions": {
            "SVWN": "Slater exchange + VWN5 correlation",
            "VBH": "von Barth-Hedin LSD functional",
        },
    },
    "GGA": {
        "name": "GGA Functionals",
        "description": "Generalized Gradient Approximation functionals",
        "functionals": ["BLYP", "PBE", "PBESOL", "PWGGA", "SOGGA", "WCGGA", "B97"],
        "descriptions": {
            "BLYP": "Becke 88 exchange + Lee-Yang-Parr correlation",
            "PBE": "Perdew-Burke-Ernzerhof",
            "PBESOL": "PBE revised for solids",
            "PWGGA": "Perdew-Wang 1991 GGA",
            "SOGGA": "Second-order GGA",
            "WCGGA": "Wu-Cohen GGA",
            "B97": "Becke's 1997 GGA functional",
        },
    },
    "HYBRID": {
        "name": "Hybrid Functionals (including range-separated)",
        "description": "Global and range-separated hybrid functionals",
        "functionals": [
            "B3LYP",
            "B3PW",
            "CAM-B3LYP",
            "PBE0",
            "PBESOL0",
            "PBE0-13",
            "HSE06",
            "HSEsol",
            "mPW1PW91",
            "mPW1K",
            "B1WC",
            "WC1LYP",
            "B97H",
            "wB97",
            "wB97X",
            "SOGGA11X",
            "SC-BLYP",
            "HISS",
            "RSHXLDA",
            "LC-wPBE",
            "LC-wPBEsol",
            "LC-wBLYP",
            "LC-BLYP",
            "LC-PBE",
        ],
        "descriptions": {
            "B3LYP": "Becke 3-parameter hybrid (20% HF)",
            "B3PW": "Becke 3-parameter with PW91 correlation (20% HF)",
            "CAM-B3LYP": "Coulomb-attenuating method B3LYP",
            "PBE0": "PBE hybrid (25% HF)",
            "PBESOL0": "PBEsol hybrid for solids (25% HF)",
            "PBE0-13": "PBE0 with 1/3 HF exchange (33.33% HF)",
            "HSE06": "Heyd-Scuseria-Ernzerhof screened hybrid",
            "HSEsol": "HSE for solids",
            "mPW1PW91": "Modified PW91 hybrid (25% HF)",
            "mPW1K": "Modified PW91 for kinetics (42.8% HF)",
            "B1WC": "One-parameter WC hybrid (16% HF)",
            "WC1LYP": "WC exchange with LYP correlation (16% HF)",
            "B97H": "Re-parameterized B97 hybrid",
            "wB97": "Head-Gordon's range-separated functional",
            "wB97X": "wB97 with short-range HF exchange",
            "SOGGA11X": "Second-order GGA hybrid (40.15% HF)",
            "SC-BLYP": "Short-range corrected BLYP",
            "HISS": "Middle-range corrected functional",
            "RSHXLDA": "Long-range corrected LDA",
            "LC-wPBE": "Long-range corrected PBE",
            "LC-wPBEsol": "Long-range corrected PBEsol",
            "LC-wBLYP": "Long-range corrected BLYP",
            "LC-BLYP": "Long-range corrected BLYP (CAM-style)",
            "LC-PBE": "Long-range corrected PBE",
        },
    },
    "MGGA": {
        "name": "meta-GGA Functionals",
        "description": "Functionals that depend on kinetic energy density",
        "functionals": [
            "SCAN",
            "r2SCAN",
            "SCAN0",
            "r2SCANh",
            "r2SCAN0",
            "r2SCAN50",
            "M05",
            "M052X",
            "M06",
            "M062X",
            "M06HF",
            "M06L",
            "revM06",
            "revM06L",
            "MN15",
            "MN15L",
            "B1B95",
            "mPW1B95",
            "mPW1B1K",
            "PW6B95",
            "PWB6K",
        ],
        "descriptions": {
            "SCAN": "Strongly Constrained and Appropriately Normed",
            "r2SCAN": "Regularized SCAN with improved numerical stability",
            "SCAN0": "SCAN hybrid (25% HF)",
            "r2SCANh": "r2SCAN hybrid (10% HF)",
            "r2SCAN0": "r2SCAN hybrid (25% HF)",
            "r2SCAN50": "r2SCAN hybrid (50% HF)",
            "M05": "Minnesota 2005 hybrid (28% HF)",
            "M052X": "M05 with doubled HF exchange (56% HF)",
            "M06": "Minnesota 2006 hybrid (27% HF)",
            "M062X": "M06 with doubled HF exchange (54% HF)",
            "M06HF": "Full HF exchange meta-GGA (100% HF)",
            "M06L": "Local meta-GGA for main-group thermochemistry",
            "revM06": "Revised M06 (40.41% HF)",
            "revM06L": "Revised M06L with improved performance",
            "MN15": "Minnesota 2015 hybrid (44% HF)",
            "MN15L": "Minnesota 2015 local functional",
            "B1B95": "One-parameter hybrid with Becke95 correlation (28% HF)",
            "mPW1B95": "Modified PW91 with B95 correlation (31% HF)",
            "mPW1B1K": "Modified PW91 with B95 correlation (44% HF)",
            "PW6B95": "6-parameter functional (28% HF)",
            "PWB6K": "6-parameter functional for kinetics (46% HF)",
        },
    },
    "3C": {
        "name": "3c Composite Methods (DFT)",
        "description": "DFT composite methods with semi-classical corrections (require specific basis sets)",
        "functionals": ["PBEH3C", "HSE3C", "B973C", "PBESOL03C", "HSESOL3C"],
        "basis_requirements": {
            "PBEH3C": "def2-mSVP",
            "HSE3C": "def2-mSVP",
            "B973C": "mTZVP",
            "PBESOL03C": "SOLDEF2MSVP",
            "HSESOL3C": "SOLDEF2MSVP",
        },
        "descriptions": {
            "PBEH3C": "Modified PBE hybrid (42% HF) with D3 and gCP",
            "HSE3C": "Screened exchange hybrid optimized for molecular solids",
            "B973C": "GGA functional with D3 and SRB corrections",
            "PBESOL03C": "PBEsol0 hybrid for solids with D3 and gCP",
            "HSESOL3C": "HSEsol with semi-classical corrections for solids",
        },
    },
}

# Functionals available for D3 dispersion correction
D3_FUNCTIONALS = [
    "BLYP",
    "PBE",
    "B97",
    "B3LYP",
    "PBE0",
    "mPW1PW91",
    "M06",
    "HSE06",
    "HSEsol",
    "LC-wPBE",
]

# Available SCF convergence methods
SCF_METHODS = ["DIIS", "ANDERSON", "BROYDEN"]

# Available DFT grid sizes
DFT_GRIDS = {
    "1": "OLDGRID",  # Old default grid from CRYSTAL09, pruned (55,434)
    "2": "DEFAULT",  # Default grid in CRYSTAL23
    "3": "LGRID",  # Large grid, pruned (75,434)
    "4": "XLGRID",  # Extra large grid (default)
    "5": "XXLGRID",  # Extra extra large grid, pruned (99,1454)
    "6": "XXXLGRID",  # Ultra extra extra large grid, pruned (150,1454)
    "7": "HUGEGRID",  # Ultra extra extra large grid for SCAN, pruned (300,1454)
}

# Available optimization types
OPT_TYPES = {"1": "FULLOPTG", "2": "CVOLOPT", "3": "CELLONLY", "4": "ATOMONLY"}

# Default geom optimization settings
DEFAULT_OPT_SETTINGS = {
    "TOLDEG": 0.00003,  # RMS of the gradient
    "TOLDEX": 0.00012,  # RMS of the displacement
    "TOLDEE": 7,  # Energy difference between two steps (10^-n)
    "MAXCYCLE": 800,  # Max number of optimization steps
}

# Default frequency calculation settings (using high accuracy tolerances)
DEFAULT_FREQ_SETTINGS = {
    "NUMDERIV": 2,  # Numerical derivative level
    "TOLINTEG": "9 9 9 11 38",  # High accuracy tolerance for frequencies
    "TOLDEE": 11,  # Tighter SCF convergence for frequencies
    "mode": "GAMMA",  # Default to gamma-point frequencies
    "intensities": False,  # Calculate IR intensities
    "ir_method": "BERRY",  # Method for IR intensities
    "raman": False,  # Calculate Raman intensities
    "print_modes": True,  # Print eigenvectors
    "analysis": False,  # Analysis of vibrational modes
    "eckart": True,  # Apply Eckart conditions
    "temperature": 298.15,  # Temperature for thermodynamics (K)
    "pressure": 0.101325,  # Pressure for thermodynamics (MPa)
}

# Advanced frequency calculation settings (for high accuracy)
ADVANCED_FREQ_SETTINGS = {
    "NUMDERIV": 2,  # Numerical derivative level
    "TOLINTEG": "9 9 9 11 38",  # Advanced tolerance for frequencies
    "TOLDEE": 11,  # Tighter SCF convergence for advanced frequencies
    "mode": "GAMMA",  # Default to gamma-point frequencies
    "intensities": True,  # Calculate IR intensities
    "ir_method": "CPHF",  # Use CPHF for accurate intensities
    "raman": True,  # Calculate Raman intensities (requires CPHF)
    "cphf_max_iter": 30,  # CPHF max iterations
    "cphf_tolerance": 6,  # CPHF convergence (10^-6)
    "print_modes": True,  # Print eigenvectors
    "analysis": True,  # Analysis of vibrational modes
    "eckart": True,  # Apply Eckart conditions
    "temperature": 298.15,  # Temperature for thermodynamics (K)
    "pressure": 0.101325,  # Pressure for thermodynamics (MPa)
    "ir_spectrum": True,  # Generate IR spectrum
    "raman_spectrum": True,  # Generate Raman spectrum
    "ir_spectrum_width": 10,  # Peak width for IR spectrum (cm^-1)
    "raman_spectrum_width": 10,  # Peak width for Raman spectrum (cm^-1)
}

# Frequency calculation templates for common use cases
FREQ_TEMPLATES = {
    "basic": {
        "mode": "GAMMA",
        "numderiv": 2,
        "intensities": False,
        "print_modes": True,
    },
    "ir_spectrum": {
        "mode": "GAMMA",
        "numderiv": 2,
        "intensities": True,
        "ir_method": "BERRY",
        "irspec": True,
        "spec_range": [0, 4000],
        "spec_step": 1.0,
        "spec_dampfac": 8.0,
    },
    "raman_spectrum": {
        "mode": "GAMMA",
        "numderiv": 2,
        "intensities": True,
        "ir_method": "CPHF",
        "raman": True,
        "ramspec": True,
        "spec_range": [0, 4000],
        "spec_step": 1.0,
        "spec_dampfac": 8.0,
    },
    "ir_raman": {
        "mode": "GAMMA",
        "numderiv": 2,
        "intensities": True,
        "ir_method": "CPHF",
        "raman": True,
        "irspec": True,
        "ramspec": True,
        "spec_range": [0, 4000],
        "spec_step": 1.0,
        "spec_dampfac": 8.0,
    },
    "thermodynamics": {
        "mode": "GAMMA",
        "numderiv": 2,
        "intensities": False,
        "temprange": (20, 0, 400),  # 20 points from 0 to 400K
        "pressrange": (1, 0.101325, 0.101325),  # Atmospheric pressure
    },
    "phonon_bands": {
        "mode": "DISPERSION",
        "numderiv": 2,
        "bands": True,
        "band_path": "AUTO",  # Will need to be defined based on crystal system
        "npoints": 100,
    },
    "phonon_dos": {
        "mode": "DISPERSION", 
        "numderiv": 2,
        "pdos": True,
        "dos_range": [0, 1000],
        "dos_bins": 200,
        "projected": True,
    },
}

# Default tolerance settings
DEFAULT_TOLERANCES = {
    "TOLINTEG": "7 7 7 7 14",  # Default integration tolerances
    "TOLDEE": 7,  # SCF energy tolerance (exponent)
}

# Default recommended settings
DEFAULT_SETTINGS = {
    "symmetry_handling": "CIF",
    "symmetry_tolerance": 1e-5,
    "reduce_to_asymmetric": False,
    "validate_symmetry": False,
    "write_only_unique": True,
    "trigonal_axes": "AUTO",
    "origin_setting": "AUTO",
    "dimensionality": "CRYSTAL",
    "calculation_type": "OPT",
    "optimization_type": "FULLOPTG",
    "optimization_settings": DEFAULT_OPT_SETTINGS.copy(),
    "basis_set_type": "INTERNAL",
    "basis_set": "POB-TZVP-REV2",
    "method": "DFT",
    "dft_functional": "HSE06",
    "use_dispersion": True,
    "dft_grid": "XLGRID",
    "is_spin_polarized": True,
    "use_smearing": False,
    "tolerances": DEFAULT_TOLERANCES.copy(),
    "scf_method": "DIIS",
    "scf_maxcycle": 800,
    "fmixing": 30,
}


# Utility functions
def format_crystal_float(value):
    """
    Format a floating point value in a way that CRYSTAL23 can interpret.
    - Use decimal format to avoid scientific notation issues

    Args:
        value (float): The value to format

    Returns:
        str: The formatted value
    """
    if isinstance(value, int):
        return str(value)

    abs_value = abs(value)
    if abs_value == 0.0:
        return "0.0"
    elif abs_value < 0.0001:
        # For very small values, use a decimal with enough precision (avoid scientific notation)
        return (
            f"{value:.10f}".rstrip("0").rstrip(".")
            if "." in f"{value:.10f}"
            else f"{value:.1f}"
        )
    else:
        # Use decimal format with appropriate precision
        return (
            f"{value:.8f}".rstrip("0").rstrip(".")
            if "." in f"{value:.8f}"
            else f"{value:.1f}"
        )


def get_user_input(prompt, options, default=None):
    """
    Get validated user input from a list of options

    Args:
        prompt (str): The prompt to display to the user
        options (list or dict): Valid options
        default (str, optional): Default value

    Returns:
        str: Valid user input
    """
    if isinstance(options, dict):
        opt_str = "\n".join([f"{key}: {value}" for key, value in options.items()])
        valid_inputs = options.keys()
    else:
        opt_str = "\n".join([f"{i + 1}: {opt}" for i, opt in enumerate(options)])
        valid_inputs = [str(i + 1) for i in range(len(options))]

    default_str = f" (default: {default})" if default else ""

    while True:
        print(f"\n{prompt}{default_str}:\n{opt_str}")
        choice = input("Enter your choice: ").strip()

        if choice == "" and default:
            return default

        if choice in valid_inputs:
            return choice

        print(f"Invalid input. Please choose from {', '.join(valid_inputs)}")


def yes_no_prompt(prompt, default="yes"):
    """
    Prompt for a yes/no response

    Args:
        prompt (str): The prompt to display
        default (str): Default value ('yes' or 'no')

    Returns:
        bool: True for yes, False for no
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default == "yes":
        prompt += " [Y/n] "
    elif default == "no":
        prompt += " [y/N] "
    else:
        raise ValueError(f"Invalid default value: {default}")

    while True:
        choice = input(prompt).lower() or default
        if choice in valid:
            return valid[choice]
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def generate_unit_cell_line(spacegroup, cell_params, dimensionality):
    """Generate the unit cell line for CRYSTAL23 input"""
    if dimensionality == "MOLECULE":
        return ""  # No unit cell for molecules

    a, b, c, alpha, beta, gamma = [float(x) for x in cell_params[:6]]

    if dimensionality == "SLAB":
        return f"{a:.8f} {b:.8f} {gamma:.6f}"
    elif dimensionality == "POLYMER":
        return f"{a:.8f}"
    elif dimensionality == "CRYSTAL":
        if spacegroup >= 1 and spacegroup <= 2:  # Triclinic
            return f"{a:.8f} {b:.8f} {c:.8f} {alpha:.6f} {beta:.6f} {gamma:.6f}"
        elif spacegroup >= 3 and spacegroup <= 15:  # Monoclinic
            return f"{a:.8f} {b:.8f} {c:.8f} {beta:.6f}"
        elif spacegroup >= 16 and spacegroup <= 74:  # Orthorhombic
            return f"{a:.8f} {b:.8f} {c:.8f}"
        elif spacegroup >= 75 and spacegroup <= 142:  # Tetragonal
            return f"{a:.8f} {c:.8f}"
        elif spacegroup >= 143 and spacegroup <= 167:  # Trigonal
            return f"{a:.8f} {c:.8f}"
        elif spacegroup >= 168 and spacegroup <= 194:  # Hexagonal
            return f"{a:.8f} {c:.8f}"
        elif spacegroup >= 195 and spacegroup <= 230:  # Cubic
            return f"{a:.8f}"
        else:
            raise ValueError(f"Invalid space group: {spacegroup}")

    return ""


def generate_k_points(a, b, c, dimensionality, spacegroup):
    """
    Generate Monkhorst-Pack k-point grid based on cell parameters

    Args:
        a, b, c (float): Cell parameters
        dimensionality (str): CRYSTAL, SLAB, POLYMER, or MOLECULE
        spacegroup (int): Space group number

    Returns:
        tuple: ka, kb, kc values for shrinking factor
    """
    ks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 48, 60]

    # Initialize defaults
    ka = kb = kc = 1

    # Find appropriate values based on cell dimensions
    for k in ks:
        if k * a > 40.0 and k * a < 80.0 and ka == 1:
            ka = k
        if k * b > 40.0 and k * b < 80.0 and kb == 1:
            kb = k
        if k * c > 40.0 and k * c < 80.0 and kc == 1:
            kc = k

    # Adjust based on dimensionality
    if dimensionality == "SLAB":
        kc = 1
    elif dimensionality == "POLYMER":
        kb = kc = 1
    elif dimensionality == "MOLECULE":
        ka = kb = kc = 1

    # Ensure reasonable values
    if ka == 1 and dimensionality not in ["POLYMER", "MOLECULE"]:
        ka = 12
    if kb == 1 and dimensionality not in ["POLYMER", "MOLECULE"]:
        kb = 12
    if kc == 1 and dimensionality not in ["SLAB", "POLYMER", "MOLECULE"]:
        kc = 12

    # For non-P1 symmetry, use consistent k-points to preserve symmetry
    if spacegroup != 1 and dimensionality == "CRYSTAL":
        # For all symmetrized systems, use the maximum k-point value
        # to ensure symmetry is preserved during calculations
        k_values = [k for k in [ka, kb, kc] if k > 1]
        if k_values:
            # Use the maximum value to ensure adequate sampling
            k_uniform = max(k_values)
            # Round to nearest available k-point value
            k_uniform = min([k for k in ks if k >= k_uniform] or [k_uniform])
            
            # Apply uniform k-points to all directions for symmetrized structures
            ka = kb = kc = k_uniform

    return ka, kb, kc


def get_element_info_string(basis_set):
    """
    Get a string describing which elements are available for a basis set

    Args:
        basis_set (str): Name of the internal basis set

    Returns:
        str: Description of available elements and core treatment
    """
    if basis_set not in INTERNAL_BASIS_SETS:
        return ""

    bs_info = INTERNAL_BASIS_SETS[basis_set]
    elements = bs_info["elements"]
    all_electron = bs_info.get("all_electron", [])
    ecp_elements = bs_info.get("ecp_elements", [])

    # Create element range descriptions
    def get_range_string(elem_list):
        if not elem_list:
            return ""

        ranges = []
        start = elem_list[0]
        end = elem_list[0]

        for i in range(1, len(elem_list)):
            if elem_list[i] == end + 1:
                end = elem_list[i]
            else:
                if start == end:
                    ranges.append(f"{ATOMIC_NUMBER_TO_SYMBOL.get(start, start)}")
                else:
                    ranges.append(
                        f"{ATOMIC_NUMBER_TO_SYMBOL.get(start, start)}-{ATOMIC_NUMBER_TO_SYMBOL.get(end, end)}"
                    )
                start = end = elem_list[i]

        # Add the last range
        if start == end:
            ranges.append(f"{ATOMIC_NUMBER_TO_SYMBOL.get(start, start)}")
        else:
            ranges.append(
                f"{ATOMIC_NUMBER_TO_SYMBOL.get(start, start)}-{ATOMIC_NUMBER_TO_SYMBOL.get(end, end)}"
            )

        return ", ".join(ranges)

    # Build description
    elem_str = get_range_string(elements)

    # Add core treatment info
    if not ecp_elements:
        core_str = "All-electron"
    elif not all_electron:
        core_str = "ECP only"
    else:
        ae_str = get_range_string(all_electron)
        ecp_str = get_range_string(ecp_elements)
        core_str = f"All-electron ({ae_str}), ECP ({ecp_str})"

    return f"Elements: {elem_str} | Core: {core_str}"


def select_functional():
    """Select DFT functional by category"""
    # First, select category - ordered to match NewCifToD12.py
    category_options = {}
    ordered_categories = ["HF", "LDA", "GGA", "HYBRID", "MGGA", "3C"]

    for i, key in enumerate(ordered_categories, 1):
        info = FUNCTIONAL_CATEGORIES[key]
        category_options[str(i)] = key
        print(f"\n{i}. {info['name']}")
        print(f"   {info['description']}")
        # Show appropriate examples for each category
        if key == "HYBRID":
            print(f"   Examples: B3LYP, PBE0, HSE06, LC-wPBE")
        elif key == "3C":
            print(f"   Examples: HF-3C, PBEh-3C, HSE-3C, B97-3C")
        else:
            print(f"   Examples: {', '.join(info['functionals'][:4])}")

    category_choice = get_user_input(
        "Select functional category", category_options, "4"
    )  # Default to HYBRID
    selected_category = category_options[category_choice]

    # Then select specific functional
    category_info = FUNCTIONAL_CATEGORIES[selected_category]
    functional_options = {
        str(i + 1): func for i, func in enumerate(category_info["functionals"])
    }

    print(f"\nAvailable {category_info['name']}:")
    for key, func in functional_options.items():
        # Build the description string
        desc_parts = []

        # Add functional description if available
        if "descriptions" in category_info and func in category_info["descriptions"]:
            desc_parts.append(category_info["descriptions"][func])

        # Add D3 support indicator
        if func in D3_FUNCTIONALS:
            desc_parts.append("[D3✓]")

        # Add basis requirement for 3C methods
        if selected_category in ["3C", "HF"] and "basis_requirements" in category_info:
            basis = category_info["basis_requirements"].get(func, "")
            if basis:
                desc_parts.append(f"(requires {basis})")

        # Print the functional with description
        if desc_parts:
            print(f"{key}: {func} - {' '.join(desc_parts)}")
        else:
            print(f"{key}: {func}")

    functional_choice = get_user_input(
        f"Select {category_info['name']}", functional_options, "1"
    )
    selected_functional = functional_options[functional_choice]

    # Check if functional has basis set requirement
    if "basis_requirements" in category_info:
        required_basis = category_info["basis_requirements"].get(selected_functional)
        return selected_functional, required_basis

    return selected_functional, None


def check_basis_set_compatibility(basis_set, atomic_numbers, basis_set_type="INTERNAL"):
    """
    Check if the selected basis set is compatible with all elements in the structure

    Args:
        basis_set (str): Name of the basis set
        atomic_numbers (list): List of atomic numbers in the structure
        basis_set_type (str): "INTERNAL" or "EXTERNAL"

    Returns:
        tuple: (is_compatible, missing_elements_list)
    """
    missing_elements = []

    if basis_set_type == "INTERNAL":
        if basis_set in INTERNAL_BASIS_SETS:
            available_elements = INTERNAL_BASIS_SETS[basis_set]["elements"]
            for atom_num in set(atomic_numbers):
                if atom_num not in available_elements:
                    missing_elements.append(atom_num)
    else:  # EXTERNAL
        # For external basis sets, check if elements need ECP
        # External basis sets go up to element 99, but some need ECP
        for atom_num in set(atomic_numbers):
            if atom_num > 99:
                missing_elements.append(atom_num)

    return len(missing_elements) == 0, missing_elements


def unique_elements(element_list):
    """Get unique elements from a list, sorted"""
    unique_list = []
    for element in element_list:
        if element not in unique_list:
            unique_list.append(element)
    return sorted(unique_list)


def write_basis_set_section(
    f, basis_set_type, basis_set, atomic_numbers, external_basis_reader=None
):
    """
    Write the basis set section of the D12 file

    Args:
        f: File handle
        basis_set_type: "INTERNAL" or "EXTERNAL"
        basis_set: Basis set name or path
        atomic_numbers: List of atomic numbers
        external_basis_reader: Function to read external basis files
    """
    if basis_set_type == "EXTERNAL":
        if external_basis_reader:
            # Get unique elements - use original atomic numbers without ECP modification
            unique_atoms = unique_elements([int(str(num).replace('2', '')) if str(num).startswith('2') and len(str(num)) > 2 else num for num in atomic_numbers])

            # Include basis sets for each unique element
            for atomic_number in unique_atoms:
                basis_content = external_basis_reader(basis_set, atomic_number)
                print(basis_content, end="", file=f)

        # Only add 99 0 and END lines for external basis sets
        print("99 0", file=f)
        print("END", file=f)
    else:  # Internal basis set
        # For internal basis sets, only write BASISSET and the basis set name
        # NO END statement for internal basis sets!
        print(f"BASISSET", file=f)
        print(f"{basis_set}", file=f)


def write_optimization_section(f, optimization_type, optimization_settings):
    """Write the optimization section of the D12 file"""
    print("OPTGEOM", file=f)
    
    # Add PREOPT if specified
    if optimization_settings.get("PREOPT", False):
        print("PREOPT", file=f)
        if "PREOPT_MAXCYCLE" in optimization_settings:
            print(optimization_settings["PREOPT_MAXCYCLE"], file=f)
        else:
            print("50", file=f)  # Default PREOPT cycles
    
    print(optimization_type, file=f)

    print("MAXCYCLE", file=f)
    print(optimization_settings["MAXCYCLE"], file=f)
    print("TOLDEG", file=f)
    print(format_crystal_float(optimization_settings["TOLDEG"]), file=f)
    print("TOLDEX", file=f)
    print(format_crystal_float(optimization_settings["TOLDEX"]), file=f)
    print("TOLDEE", file=f)
    print(optimization_settings["TOLDEE"], file=f)

    # Add MAXTRADIUS if specified
    if "MAXTRADIUS" in optimization_settings:
        print("MAXTRADIUS", file=f)
        print(format_crystal_float(optimization_settings["MAXTRADIUS"]), file=f)

    print("ENDGEOM", file=f)


def write_minimal_raman_section(f):
    """
    Write a minimal Raman calculation section with CPHF
    This produces exactly:
    FREQCALC
    INTENS
    INTRAMAN
    INTCPHF
    ENDCPHF
    ENDFREQ
    """
    print("FREQCALC", file=f)
    print("INTENS", file=f)
    print("INTRAMAN", file=f)
    print("INTCPHF", file=f)
    print("ENDCPHF", file=f)
    print("ENDFREQ", file=f)


def write_frequency_section(f, freq_settings):
    """
    Write the frequency calculation section of the D12 file
    
    Args:
        f: File handle
        freq_settings: Dictionary with frequency calculation settings
            Required keys:
            - mode: str - Type of frequency calculation (e.g., "GAMMA", "DISPERSION")
            
            Optional keys for basic settings:
            - numderiv: int - Numerical derivative method (1 or 2, default 2)
            - intensities: bool - Calculate IR intensities (default False)
            - ir_method: str - Method for IR intensities: "BERRY" (default), "WANNIER", "CPHF"
            - raman: bool - Calculate Raman intensities (default False)
            - dielectric_tensor: list[float] - 3x3 dielectric tensor for LO/TO splitting
            - dielectric_constant: float - Isotropic dielectric constant (simpler than tensor)
            - temperature: float - Temperature for thermodynamic analysis (default 298.15 K)
            - pressure: float - Pressure for thermodynamic analysis (default 0.101325 MPa)
            - print_modes: bool - Print eigenvectors (default True)
            - analysis: bool - Analysis of vibrational modes (default False)
            - restart: bool - Restart from previous calculation (default False)
            
            Advanced frequency options:
            - preoptgeom: bool - Optimize geometry before frequencies (default False)
            - optgeom_settings: dict - Settings for PREOPTGEOM block
            - isotopes: dict - Modified isotope masses {atom_label: mass}
            - stepsize: float - Step size for numerical derivatives (default 0.003 Å)
            - eckart: bool - Apply Eckart conditions (default True)
            - fragment: list[int] - Calculate frequencies for atom fragment only
            - temprange: tuple - (n_temps, t_min, t_max) for temperature range
            - pressrange: tuple - (n_press, p_min, p_max) for pressure range
            - neglectfreq: int - Number of lowest frequencies to neglect in thermodynamics
            - multitask: int - Number of parallel tasks for HPC
            
            IR intensity specific options:
            - born_tensor_norm: bool - Normalize Born tensor to fulfill sum rule
            - relocalize_wannier: bool - Relocalize Wannier functions at each point
            - cphf_settings: dict - Settings for CPHF calculation
            
            Raman intensity specific options:
            - ramanexp: tuple - (temperature, laser_wavelength_nm) for experimental conditions
            - chi2tensor: list[float] - 3x9 second-order dielectric tensor for LO Raman
            - norenorm: bool - Turn off renormalization to highest peak
            - tensonly: bool - Only calculate tensors then stop
            
            Spectral generation options:
            - irspec: bool - Generate IR spectrum (default False)
            - ramspec: bool - Generate Raman spectrum (default False)
            - spec_range: tuple - (min_freq, max_freq) in cm^-1
            - spec_step: float - Step size for spectra in cm^-1 (default 1.0)
            - spec_broadening: float - Peak broadening factor (default 8.0)
            - spec_voigt: float - Voigt mixing parameter for Raman (0-1, default 1.0)
            
            Mode analysis and property options:
            - scanmode: dict - Scan along normal modes {"modes": [int], "range": (start, end, step)}
            - combmode: str - Combination modes: "ALL", "IR", "RAMAN", "IRRAMAN" (default)
            - dispersion: bool - Calculate phonon dispersion (default False)
            - supercell: tuple - Supercell size for dispersion (Lx, Ly, Lz)
            - bands: dict - Band structure settings {"path": str, "npoints": int}
            - pdos: dict - Phonon DOS settings {"max_freq": float, "nbins": int, "projected": bool}
            - ins: dict - INS spectrum settings {"max_freq": float, "nbins": int, "neutron_type": int}
            - adp: dict - Anisotropic displacement parameters {"temperature": float, "type": int}
            - intraphonon: dict - Fourier interpolation settings
            - wang: list[float] - 3x3 dielectric tensor for polar corrections
            
            Anharmonic options:
            - anharm: int - Atom label for X-H anharmonic stretching
            - anharm_points: int - Number of points for anharmonic PES (7 or 26)
            - anhapes: dict - Anharmonic PES settings {"modes": [int], "scheme": int, "step": float}
            - vscf: dict - VSCF settings {"tolerance": float, "mixing": float}
            - vci: dict - VCI settings {"quanta": int, "modes": int, "guess": int}
    """
    # Check for minimal Raman mode
    if freq_settings.get("minimal_raman", False):
        write_minimal_raman_section(f)
        return
    
    print("FREQCALC", file=f)
    
    # Handle restart
    if freq_settings.get("restart", False):
        print("RESTART", file=f)
    
    # Pre-optimization if requested
    if freq_settings.get("preoptgeom", False):
        print("PREOPTGEOM", file=f)
        opt_settings = freq_settings.get("optgeom_settings", {})
        if opt_settings.get("fulloptg", False):
            print("FULLOPTG", file=f)
        # Optimization tolerances
        if "toldeg" in opt_settings:
            print("TOLDEG", file=f)
            print(format_crystal_float(opt_settings["toldeg"]), file=f)
        if "toldex" in opt_settings:
            print("TOLDEX", file=f)
            print(format_crystal_float(opt_settings["toldex"]), file=f)
        if "finalrun" in opt_settings:
            print("FINALRUN", file=f)
            print(opt_settings["finalrun"], file=f)
        print("END", file=f)
    
    # Mode analysis
    if freq_settings.get("analysis", False):
        print("ANALYSIS", file=f)
    elif freq_settings.get("noanalysis", False):
        print("NOANALYSIS", file=f)
    
    # Eckart conditions
    if not freq_settings.get("eckart", True):
        print("NOECKART", file=f)
    
    # Fragment calculation
    if "fragment" in freq_settings:
        fragment_atoms = freq_settings["fragment"]
        print("FRAGMENT", file=f)
        print(len(fragment_atoms), file=f)
        print(" ".join(str(a) for a in fragment_atoms), file=f)
    
    # Modified isotopes
    if "isotopes" in freq_settings:
        isotopes = freq_settings["isotopes"]
        print("ISOTOPES", file=f)
        print(len(isotopes), file=f)
        for atom_label, mass in isotopes.items():
            print(f"{atom_label} {mass}", file=f)
    
    # Numerical derivative method (skip if minimal_raman is True)
    if not freq_settings.get("minimal_raman", False):
        numderiv = freq_settings.get("numderiv", 2)
        print("NUMDERIV", file=f)
        print(numderiv, file=f)
    
    # Step size for numerical derivatives
    if "stepsize" in freq_settings:
        print("STEPSIZE", file=f)
        print(format_crystal_float(freq_settings["stepsize"]), file=f)
    
    # Temperature range
    if "temprange" in freq_settings:
        temprange = freq_settings["temprange"]
        # Handle both tuple and dict formats
        if isinstance(temprange, dict):
            n_temps = temprange.get("n_temps", 20)
            t_min = temprange.get("t_min", 0)
            t_max = temprange.get("t_max", 400)
        else:
            # Assume it's a tuple/list
            try:
                n_temps, t_min, t_max = temprange
            except (ValueError, TypeError):
                # Fallback to defaults if unpacking fails
                n_temps, t_min, t_max = 20, 0, 400
        print("TEMPERAT", file=f)
        print(f"{n_temps} {t_min} {t_max}", file=f)
    
    # Pressure range
    if "pressrange" in freq_settings:
        pressrange = freq_settings["pressrange"]
        # Handle both tuple and dict formats
        if isinstance(pressrange, dict):
            n_press = pressrange.get("n_press", 20)
            p_min = pressrange.get("p_min", 0)
            p_max = pressrange.get("p_max", 10)
        else:
            # Assume it's a tuple/list
            try:
                n_press, p_min, p_max = pressrange
            except (ValueError, TypeError):
                # Fallback to defaults if unpacking fails
                n_press, p_min, p_max = 20, 0, 10
        print("PRESSURE", file=f)
        print(f"{n_press} {p_min} {p_max}", file=f)
    
    # Neglect lowest frequencies
    if "neglectfreq" in freq_settings:
        print("NEGLEFRE", file=f)
        print(freq_settings["neglectfreq"], file=f)
    
    # Multitask for HPC
    if "multitask" in freq_settings:
        print("MULTITASK", file=f)
        print(freq_settings["multitask"], file=f)
    
    # Mode printing
    if not freq_settings.get("print_modes", True):
        print("NOMODES", file=f)
    
    # Frequency scaling
    if "freqscale" in freq_settings:
        print("FREQSCAL", file=f)
        print(format_crystal_float(freq_settings["freqscale"]), file=f)
    
    # Dielectric tensor or constant for LO/TO splitting
    if "dielectric_tensor" in freq_settings:
        tensor = freq_settings["dielectric_tensor"]
        print("DIELTENS", file=f)
        # Print 3x3 tensor (9 values)
        tensor_str = " ".join(format_crystal_float(v) for v in tensor[:9])
        print(tensor_str, file=f)
    elif "dielectric_constant" in freq_settings:
        print("DIELISO", file=f)
        print(format_crystal_float(freq_settings["dielectric_constant"]), file=f)
    
    # Chi2 tensor for Raman LO modes
    if "chi2tensor" in freq_settings:
        tensor = freq_settings["chi2tensor"]
        print("CHI2TENS", file=f)
        # Print 3x9 tensor (27 values)
        for i in range(0, 27, 9):
            tensor_str = " ".join(format_crystal_float(v) for v in tensor[i:i+9])
            print(tensor_str, file=f)
    
    # IR intensities
    if freq_settings.get("intensities", False):
        print("INTENS", file=f)
        
        ir_method = freq_settings.get("ir_method", "BERRY").upper()
        if ir_method == "WANNIER":
            print("INTLOC", file=f)
            
            # Wannier function settings
            if freq_settings.get("relocalize_wannier", False):
                print("DIPOMOME", file=f)
                print("RELOCAL", file=f)
                print("END", file=f)
        elif ir_method == "CPHF":
            print("INTCPHF", file=f)
            # CPHF settings block
            cphf_settings = freq_settings.get("cphf_settings", {})
            if "fmixing" in cphf_settings:
                print("FMIXING", file=f)
                print(cphf_settings["fmixing"], file=f)
            if "tolalpha" in cphf_settings:
                print("TOLALPHA", file=f)
                print(cphf_settings["tolalpha"], file=f)
            if "maxcycle" in cphf_settings:
                print("MAXCYCLE", file=f)
                print(cphf_settings["maxcycle"], file=f)
            # Print ENDCPHF to close the INTCPHF block
            print("ENDCPHF", file=f)
        # else: default is Berry phase (INTPOL), no keyword needed
        
        # Born tensor normalization
        if freq_settings.get("born_tensor_norm", False):
            print("NORMBORN", file=f)
    else:
        print("NOINTENS", file=f)
    
    # Raman intensities
    if freq_settings.get("raman", False):
        print("INTRAMAN", file=f)
        
        # Always need INTCPHF for Raman
        if not (freq_settings.get("intensities", False) and 
                freq_settings.get("ir_method", "BERRY").upper() == "CPHF"):
            print("INTCPHF", file=f)
            # CPHF settings for Raman
            cphf_settings = freq_settings.get("cphf_settings", {})
            if "fmixing2" in cphf_settings:
                print("FMIXING2", file=f)
                print(cphf_settings["fmixing2"], file=f)
            if "tolgamma" in cphf_settings:
                print("TOLGAMMA", file=f)
                print(cphf_settings["tolgamma"], file=f)
            if "maxcycle2" in cphf_settings:
                print("MAXCYCLE2", file=f)
                print(cphf_settings["maxcycle2"], file=f)
            print("ENDCPHF", file=f)
        
        # Experimental conditions
        if "ramanexp" in freq_settings:
            temp, laser_nm = freq_settings["ramanexp"]
            print("RAMANEXP", file=f)
            print(f"{temp} {laser_nm}", file=f)
        
        # Other Raman options
        if freq_settings.get("norenorm", False):
            print("NORENORM", file=f)
        if freq_settings.get("tensonly", False):
            print("TENSONLY", file=f)
    
    # Combination modes
    if "combmode" in freq_settings:
        print("COMBMODE", file=f)
        mode_type = freq_settings["combmode"].upper()
        if mode_type in ["IR", "RAMAN", "ALL"]:
            print(mode_type, file=f)
        # IRRAMAN is default, no keyword needed
        
        # Frequency range for combination modes
        if "combmode_range" in freq_settings:
            print("FREQRANGE", file=f)
            fmin, fmax = freq_settings["combmode_range"]
            print(f"{fmin} {fmax}", file=f)
        print("END", file=f)
    
    # Mode scanning
    if "scanmode" in freq_settings:
        scan_settings = freq_settings["scanmode"]
        modes = scan_settings.get("modes", [])
        if modes:
            print("SCANMODE", file=f)
            scan_range = scan_settings.get("range", (-10, 10, 0.2))
            print(f"{len(modes)} {scan_range[0]} {scan_range[1]} {scan_range[2]}", file=f)
            print(" ".join(str(m) for m in modes), file=f)
    
    # Phonon dispersion
    if freq_settings.get("dispersion", False):
        print("DISPERSION", file=f)
        
        # Supercell for phonon calculation
        if "scelphono" in freq_settings:
            supercell = freq_settings["scelphono"]
            print("SCELPHONO", file=f)
            # Can be either expansion factors or full transformation matrix
            if isinstance(supercell, list) and len(supercell) == 3:
                # Simple expansion factors [nx, ny, nz]
                print(" ".join(str(n) for n in supercell), file=f)
            elif isinstance(supercell, list) and len(supercell) == 9:
                # Full transformation matrix (3x3)
                for i in range(0, 9, 3):
                    print(" ".join(str(supercell[j]) for j in range(i, i+3)), file=f)
        
        # Fourier interpolation
        if "interphess" in freq_settings:
            interp = freq_settings["interphess"]
            print("INTERPHESS", file=f)
            l_params = interp.get("expand", [2, 2, 2])
            print(" ".join(str(l) for l in l_params[:3]), file=f)
            print(interp.get("print", 0), file=f)
        
        # Wang correction for polar materials
        if "wang" in freq_settings:
            wang_tensor = freq_settings["wang"]
            print("WANG", file=f)
            tensor_str = " ".join(format_crystal_float(v) for v in wang_tensor[:9])
            print(tensor_str, file=f)
        
        # Band structure
        if "bands" in freq_settings:
            band_settings = freq_settings["bands"]
            print("BANDS", file=f)
            print(band_settings.get("shrink", 16), file=f)
            print(band_settings.get("npoints", 100), file=f)
            
            # Band path
            path = band_settings.get("path", [])
            print(len(path), file=f)
            for segment in path:
                if isinstance(segment, str):
                    # High symmetry point labels (e.g., "G", "X")
                    print(f"{segment[0]} {segment[1]}", file=f)
                else:
                    # Fractional coordinates
                    start, end = segment
                    print(f"{start[0]} {start[1]} {start[2]} {end[0]} {end[1]} {end[2]}", file=f)
        
        # Phonon DOS
        if "pdos" in freq_settings:
            pdos_settings = freq_settings["pdos"]
            print("PDOS", file=f)
            print(f"{pdos_settings.get('max_freq', 2000)} {pdos_settings.get('nbins', 200)}", file=f)
            print(1 if pdos_settings.get("projected", True) else 0, file=f)
        
        # INS spectrum
        if "ins" in freq_settings:
            ins_settings = freq_settings["ins"]
            print("INS", file=f)
            print(f"{ins_settings.get('max_freq', 3000)} {ins_settings.get('nbins', 300)}", file=f)
            print(ins_settings.get("neutron_type", 2), file=f)  # 0=coherent, 1=incoherent, 2=both
    
    # Anisotropic displacement parameters
    if "adp" in freq_settings:
        adp_settings = freq_settings["adp"]
        print("ADP", file=f)
        print(f"{adp_settings.get('type', 0)} {adp_settings.get('neglect', 0)}", file=f)
    
    # IR spectrum generation
    if freq_settings.get("irspec", False):
        print("IRSPEC", file=f)
        
        # Spectrum settings
        if "spec_range" in freq_settings:
            print("RANGE", file=f)
            print(f"{freq_settings['spec_range'][0]} {freq_settings['spec_range'][1]}", file=f)
        if "spec_step" in freq_settings:
            print("LENSTEP", file=f)
            print(format_crystal_float(freq_settings["spec_step"]), file=f)
        if "spec_dampfac" in freq_settings:
            print("DAMPFAC", file=f)
            print(format_crystal_float(freq_settings["spec_dampfac"]), file=f)
        if freq_settings.get("spec_gaussian", False):
            print("GAUSS", file=f)
        if "spec_angle" in freq_settings:
            print("ANGLE", file=f)
            print(format_crystal_float(freq_settings["spec_angle"]), file=f)
        if freq_settings.get("spec_refrind", False):
            print("REFRIND", file=f)
        if freq_settings.get("spec_dielfun", False):
            print("DIELFUN", file=f)
        
        print("END", file=f)
    
    # Raman spectrum generation
    if freq_settings.get("ramspec", False):
        print("RAMSPEC", file=f)
        
        # Spectrum settings
        if "spec_range" in freq_settings:
            print("RANGE", file=f)
            print(f"{freq_settings['spec_range'][0]} {freq_settings['spec_range'][1]}", file=f)
        if "spec_step" in freq_settings:
            print("LENSTEP", file=f)
            print(format_crystal_float(freq_settings["spec_step"]), file=f)
        if "raman_voigt" in freq_settings:
            print("VOIGT", file=f)
            print(format_crystal_float(freq_settings["raman_voigt"]), file=f)
        elif "spec_voigt" in freq_settings:
            print("VOIGT", file=f)
            print(format_crystal_float(freq_settings["spec_voigt"]), file=f)
        if "raman_dampfac" in freq_settings:
            print("DAMPFAC", file=f)
            print(format_crystal_float(freq_settings["raman_dampfac"]), file=f)
        elif "spec_dampfac" in freq_settings:
            print("DAMPFAC", file=f)
            print(format_crystal_float(freq_settings["spec_dampfac"]), file=f)
        
        print("END", file=f)
    
    # Anharmonic PES calculation
    if "anhapes" in freq_settings:
        anha_settings = freq_settings["anhapes"]
        print("ANHAPES", file=f)
        modes = anha_settings.get("modes", [])
        print(len(modes), file=f)
        print(" ".join(str(m) for m in modes), file=f)
        print(f"{anha_settings.get('scheme', 3)} {format_crystal_float(anha_settings.get('step', 0.9))}", file=f)
        
        # Restart PES
        if anha_settings.get("restpes", False):
            print("RESTPES", file=f)
    
    # VSCF calculation
    if "vscf" in freq_settings:
        vscf_settings = freq_settings["vscf"]
        print("VSCF", file=f)
        
        if "tolerance" in vscf_settings:
            print("VSCFTOL", file=f)
            print(int(-np.log10(vscf_settings["tolerance"])), file=f)
        if "mixing" in vscf_settings:
            print("VSCFMIX", file=f)
            print(int(vscf_settings["mixing"]), file=f)
    
    # VCI calculation
    if "vci" in freq_settings:
        vci_settings = freq_settings["vci"]
        print("VCI", file=f)
        print(f"{vci_settings.get('quanta', 6)} {vci_settings.get('modes', 3)}", file=f)
        print(vci_settings.get("guess", 1), file=f)  # 0=harmonic, 1=VSCF
    
    # End FREQCALC block
    print("ENDFREQ", file=f)


def write_anharm_section(f, anharm_settings):
    """
    Write anharmonic X-H stretching section (outside FREQCALC)
    
    Args:
        f: File handle
        anharm_settings: Dictionary with anharmonic settings
            - atom_label: int - Label of H/D atom to displace
            - points: int - Number of points (7 or 26, default 7)
            - isotopes: dict - Modified isotope masses {atom_label: mass}
            - keepsymm: bool - Keep symmetry by moving all equivalent atoms
            - noguess: bool - Use atomic densities as SCF guess at each point
    """
    print("ANHARM", file=f)
    print(anharm_settings["atom_label"], file=f)
    
    # Modified isotopes
    if "isotopes" in anharm_settings:
        isotopes = anharm_settings["isotopes"]
        print("ISOTOPES", file=f)
        print(len(isotopes), file=f)
        for atom_label, mass in isotopes.items():
            print(f"{atom_label} {mass}", file=f)
    
    # Keep symmetry
    if anharm_settings.get("keepsymm", False):
        print("KEEPSYMM", file=f)
    
    # SCF guess
    if anharm_settings.get("noguess", False):
        print("NOGUESS", file=f)
    
    # Number of points
    if anharm_settings.get("points", 7) == 26:
        print("POINTS26", file=f)
    
    print("END", file=f)


def write_dft_section(f, functional, use_dispersion, dft_grid, is_spin_polarized):
    """Write the DFT section of the D12 file"""
    print("DFT", file=f)

    if is_spin_polarized:
        print("SPIN", file=f)

    # Map functionals to their correct CRYSTAL keywords
    functional_keyword_map = {
        "PBESOL": "PBESOLXC",
        "SOGGA": "SOGGAXC",
        "VBH": "VBHLYP",
        "PWGGA": "PW91GGA",
        "WCGGA": "WCGGAPBE",
    }

    # Handle special functional keywords
    if functional in ["PBEH3C", "HSE3C", "B973C", "PBESOL03C", "HSESOL3C"]:
        # These are standalone keywords in CRYSTAL23
        print(f"{functional}", file=f)
        # For HSESOL3C, we need XLGRID (even if not specified or DEFAULT)
        if functional == "HSESOL3C":
            # Always use XLGRID for HSESOL3C
            print("XLGRID", file=f)
    elif functional == "mPW1PW91" and use_dispersion:
        print("PW1PW-D3", file=f)
        # Add DFT grid size only if not default and not None
        if dft_grid and dft_grid != "DEFAULT":
            print(dft_grid, file=f)
    elif functional in functional_keyword_map:
        # Use the mapped keyword for functionals that need special syntax
        mapped_functional = functional_keyword_map[functional]
        if use_dispersion and functional in D3_FUNCTIONALS:
            print(f"{mapped_functional}-D3", file=f)
        else:
            print(f"{mapped_functional}", file=f)
        
        # Add DFT grid size only if not default and not None
        if dft_grid and dft_grid != "DEFAULT":
            print(dft_grid, file=f)
    else:
        # Standard functional
        if use_dispersion and functional in D3_FUNCTIONALS:
            print(f"{functional}-D3", file=f)
        else:
            print(f"{functional}", file=f)

        # Add DFT grid size only if not default and not None
        if dft_grid and dft_grid != "DEFAULT":
            print(dft_grid, file=f)

    print("ENDDFT", file=f)


def write_scf_section(
    f,
    tolerances,
    k_points,
    dimensionality,
    use_smearing,
    smearing_width,
    scf_method,
    scf_maxcycle,
    fmixing,
    num_atoms,
    spacegroup=1,
):
    """Write the SCF parameters section of the D12 file"""
    # Tolerance settings with proper fallback handling
    print("TOLINTEG", file=f)
    tolinteg_value = tolerances.get("TOLINTEG", "7 7 7 7 14")  # Default fallback
    if tolinteg_value is None:
        tolinteg_value = "7 7 7 7 14"
    print(tolinteg_value, file=f)
    
    print("TOLDEE", file=f)
    toldee_value = tolerances.get("TOLDEE", 7)  # Default fallback
    if toldee_value is None:
        toldee_value = 7
    print(toldee_value, file=f)

    # K-points
    if k_points and dimensionality != "MOLECULE":
        if isinstance(k_points, str):
            # Pre-formatted k-points string
            print("SHRINK", file=f)
            print("0 24", file=f)
            print(k_points, file=f)
        else:
            # Tuple of (ka, kb, kc)
            ka, kb, kc = k_points
            
            # Check if k-points are uniform for simplified SHRINK format
            # For symmetrized structures (non-P1), prefer uniform k-points
            use_simplified = False
            if dimensionality == "CRYSTAL" and ka == kb == kc:
                use_simplified = True
            elif dimensionality == "CRYSTAL" and spacegroup != 1:
                # For symmetrized structures, convert to uniform k-points
                k_max = max(ka, kb, kc)
                ka = kb = kc = k_max
                use_simplified = True
                
            if use_simplified:
                # Use simplified format: SHRINK k n_shrink
                n_shrink = ka * 2
                print("SHRINK", file=f)
                print(f"{ka} {n_shrink}", file=f)
            else:
                # Use directional format: SHRINK 0 n_shrink, then ka kb kc
                n_shrink = max(ka, kb, kc) * 2
                print("SHRINK", file=f)
                print(f"0 {n_shrink}", file=f)

                if dimensionality == "CRYSTAL":
                    print(f"{ka} {kb} {kc}", file=f)
                elif dimensionality == "SLAB":
                    print(f"{ka} {kb} 1", file=f)
                elif dimensionality == "POLYMER":
                    print(f"{ka} 1 1", file=f)

    # Fermi smearing
    if use_smearing:
        print("SMEAR", file=f)
        print(f"{smearing_width:.6f}", file=f)

    # SCF settings
    print("SCFDIR", file=f)

    # Add BIPOSIZE and EXCHSIZE for large systems
    if num_atoms > 5:
        print("BIPOSIZE", file=f)
        print("110000000", file=f)
        print("EXCHSIZE", file=f)
        print("110000000", file=f)

    # SCF convergence
    print("MAXCYCLE", file=f)
    print(scf_maxcycle, file=f)

    print("FMIXING", file=f)
    print(fmixing, file=f)

    print(scf_method, file=f)

    if scf_method == "DIIS":
        print("HISTDIIS", file=f)
        print("100", file=f)

    # Print options
    print("PPAN", file=f)  # Print Mulliken population analysis

    # End of input
    print("END", file=f)
