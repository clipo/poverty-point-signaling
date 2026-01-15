"""
Poverty Point Model Calibration Data

Compiled from PDF extraction (January 2026).
Sources: Webb 1956, Webb 1968, Ford 1954, Kidder 2002, Kidder 2006,
         Hays 2018, Sassaman 2005, and others.

This module provides empirical data for calibrating the Poverty Point
agent-based model.
"""

# =============================================================================
# CHRONOLOGY
# =============================================================================

# Poverty Point occupation span (calibrated)
CHRONOLOGY = {
    "start_cal_bp": 3600,      # ~1700 BCE
    "end_cal_bp": 3100,        # ~1100 BCE
    "duration_years": 500,     # Approximate occupation span
    "peak_construction": (3400, 3200),  # cal BP range of most intensive building
}

# Key radiocarbon dates from the literature
# Format: (lab_number, date_bp, error, calibrated_range, site, context)
RADIOCARBON_DATES = [
    # From Ford 1954 - Jaketown
    ("Kulp-114", 2350, 80, None, "Jaketown", "Poverty Point complex"),

    # From Kidder 2006 - Regional chronology
    # Note: Many dates in text refer to calibrated ranges, not raw dates
    # Late Archaic to Early Woodland transition: ca. 3100-2500 cal BP

    # Nolan site (from Kidder 2006)
    (None, None, None, (5200, 4800), "16MA201", "Nolan site occupation"),

    # Raffman site Early Woodland
    (None, None, None, (2600, 2200), "16MA20", "Early Woodland occupation"),
]

# Regional cultural chronology
CULTURAL_PHASES = {
    "late_archaic": (5000, 3000),        # cal BP
    "poverty_point": (3600, 3100),       # cal BP - core PP period
    "early_woodland": (2900, 2200),      # cal BP
    "regional_hiatus": (3100, 2500),     # cal BP - gap between LA and EW
}


# =============================================================================
# CONSTRUCTION DATA
# =============================================================================

# Total earthwork volume at Poverty Point
TOTAL_EARTHWORK_VOLUME_M3 = 750_000  # From Kidder 2006

# Alternative estimate
TOTAL_EARTHWORK_VOLUME_YD3 = 1_000_000  # "nearly one million cubic yards" - Webb 1968

# Individual feature measurements (from Webb 1956, Webb 1968, Ford 1954)
MOUND_DIMENSIONS = {
    "mound_a": {
        "name": "Poverty Point Mound / Bird Mound",
        "height_ft": 70,
        "height_m": 21.3,
        "length_ns_ft": 640,
        "length_ns_m": 195,
        "platform_height_ft": 23,
        "platform_dimensions_ft": (240, 300),
        "description": "Bird-shaped mound, largest at site",
    },
    "mound_b": {
        "name": "Mound B",
        "height_ft": 21,
        "height_m": 6.4,
        "diameter_ft": 195,
        "diameter_m": 59.4,
        "description": "Conical mound north of Mound A",
    },
    "motley_mound": {
        "name": "Motley Mound",
        "height_ft": 51,
        "height_m": 15.5,
        "length_ew_ft": 560,
        "length_ns_ft": 400,
        "description": "Located 1.5 mi north of village center",
    },
}

# Ridge/terrace dimensions
RIDGE_SYSTEM = {
    "num_ridges": 6,
    "ridge_height_ft": (4, 6),
    "ridge_spacing_ft": 150,          # crest to crest
    "ridge_width_ft": 150,            # depression to depression
    "village_diameter_ft": 3960,
    "village_diameter_m": 1207,
    "shape": "octagonal with spoke-like gaps",
}


# =============================================================================
# EXOTIC MATERIALS
# =============================================================================

# Artifact counts at Poverty Point (from Hays 2018, Table 1)
POVERTY_POINT_ARTIFACTS = {
    "copper_objects": 155,
    "steatite_objects": 2221,
    "steatite_vessel_fragments": 3000,  # "almost 3000" - Webb 1956
    "galena_objects": 702,
    "plummets": 2790,
    "projectile_points": 11714,
    "stone_beads": 1214,
    "microliths": 30000,              # "ca. 30,000"
    "stone_gorgets": 546,
    "pendants": 296,
    "celts_adzes_axes": 445,
    "hammerstones": 348,
    "bannerstones_boatstones": 67,
    "clay_figurines": 133,
    "pipes": 50,                      # "50+"
}

# Comparison sites (from Hays 2018, Table 1)
INDIAN_KNOLL_ARTIFACTS = {
    "copper_objects": 5,
    "steatite_objects": 0,
    "galena_objects": 0,
    "plummets": 0,
    "projectile_points": 8714,
    "stone_beads": 88,
    "microliths": 0,
}

# Exotic material sources and distances
EXOTIC_SOURCES = {
    "copper": {
        "source_region": "Great Lakes / Upper Michigan",
        "distance_km": 1600,          # Approximate straight-line distance
        "notes": "Native copper, Lake Superior region",
    },
    "steatite": {
        "source_region": "Southern Piedmont (Georgia/Alabama)",
        "distance_km": 600,           # From Sassaman 2005
        "route": "Gulf Coast and Mississippi River",
        "notes": "West Georgia / East Alabama quarries",
    },
    "galena": {
        "source_region": "Southeast Missouri / Upper Mississippi",
        "distance_km": 500,           # Approximate
        "notes": "Lead ore deposits",
    },
    "novaculite": {
        "source_region": "Ouachita Mountains, Arkansas",
        "distance_km": 300,
        "notes": "Fine-grained siliceous stone for tools",
    },
    "quartz_crystal": {
        "source_region": "Arkansas / Appalachian",
        "distance_km": (300, 800),    # Variable depending on source
    },
}


# =============================================================================
# SITE HIERARCHY
# =============================================================================

# Regional Poverty Point culture sites
SITE_HIERARCHY = {
    "poverty_point": {
        "trinomial": "16WC5",
        "area_km2": 3.0,
        "earthwork_volume_m3": 750000,
        "location": "Macon Ridge, NE Louisiana",
        "coordinates": (32.63, -91.41),
        "notes": "Type site, largest PP site",
    },
    "jaketown": {
        "trinomial": "22HU505",
        "notes": "Major PP site in Yazoo Basin, Mississippi",
    },
    "claiborne": {
        "trinomial": "22HA501",
        "shape": "crescent-shaped shell midden",
        "width_m": 250,
        "notes": "Gateway site for soapstone, Gulf Coast",
    },
    "terral_lewis": {
        "trinomial": "16MA16",
        "notes": "PP culture site near Poverty Point",
    },
    "copes": {
        "trinomial": "16MA47",
        "notes": "Good faunal/botanical preservation",
    },
}

# Site trinomials from extraction
KNOWN_SITES = [
    "16WC5",    # Poverty Point
    "16MA47",   # Copes
    "16MA16",   # Terral Lewis
    "16CT5",    # Caney Mound
    "16OR40",   # Linsley
    "16LY5",    # Beau Rivage
    "16SM20",   # Ruth Canal
    "16MA201",  # Nolan
    "16MA20",   # Raffman
    "16MA57",   # Borrow Pit
    "16CT147",  # Cowpen Slough
    "22HU505",  # Jaketown
    "22CR504",  # Teoc Creek
    "22HA501",  # Claiborne
    "22JA530",  # Apple Street
    "3AS379",   # Lake Enterprise Mound (Arkansas)
]


# =============================================================================
# ENVIRONMENTAL CONTEXT
# =============================================================================

# Geographic setting
GEOGRAPHIC_SETTING = {
    "landform": "Macon Ridge",
    "elevation_above_floodplain_ft": (15, 20),
    "bluff_height_ft": 20,           # Eastern escarpment
    "bayou": "Bayou Macon",
    "river": "Mississippi (to east)",
    "formation": "Arkansas River outwash fan",
}

# Ecotone characteristics
ECOTONE = {
    "zones": ["aquatic", "terrestrial", "upland"],
    "advantage": "Multi-zone resource access",
    "seasonal_resources": {
        "spring": "fish runs",
        "summer": "aquatic resources",
        "fall": "nuts, deer",
        "winter": "reduced but diverse",
    },
}


# =============================================================================
# MODEL CALIBRATION TARGETS
# =============================================================================

# Target metrics for model validation
CALIBRATION_TARGETS = {
    # Construction
    "total_volume_m3": 750000,
    "construction_duration_years": 500,
    "volume_per_year_m3": 1500,       # Average rate

    # Population (estimates uncertain)
    "aggregation_population": (1000, 5000),  # Range of estimates
    "regional_band_count": (30, 100),

    # Exotic goods
    "copper_objects_total": 155,
    "steatite_objects_total": 2221,
    "galena_objects_total": 702,

    # Site hierarchy
    "pp_site_dominance": True,        # PP >> other sites
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_chronology_midpoint():
    """Return midpoint of PP occupation in cal BP."""
    return (CHRONOLOGY["start_cal_bp"] + CHRONOLOGY["end_cal_bp"]) / 2


def convert_ft_to_m(feet: float) -> float:
    """Convert feet to meters."""
    return feet * 0.3048


def convert_yd3_to_m3(cubic_yards: float) -> float:
    """Convert cubic yards to cubic meters."""
    return cubic_yards * 0.764555


def convert_ft3_to_m3(cubic_feet: float) -> float:
    """Convert cubic feet to cubic meters."""
    return cubic_feet * 0.0283168


if __name__ == "__main__":
    # Print summary
    print("Poverty Point Calibration Data Summary")
    print("=" * 50)
    print(f"\nChronology: {CHRONOLOGY['start_cal_bp']}-{CHRONOLOGY['end_cal_bp']} cal BP")
    print(f"Duration: ~{CHRONOLOGY['duration_years']} years")
    print(f"\nTotal earthwork: {TOTAL_EARTHWORK_VOLUME_M3:,} m³")
    print(f"Annual construction rate: ~{CALIBRATION_TARGETS['volume_per_year_m3']:,} m³/year")
    print(f"\nExotic materials at Poverty Point:")
    print(f"  Copper objects: {POVERTY_POINT_ARTIFACTS['copper_objects']}")
    print(f"  Steatite objects: {POVERTY_POINT_ARTIFACTS['steatite_objects']}")
    print(f"  Galena objects: {POVERTY_POINT_ARTIFACTS['galena_objects']}")
    print(f"\nExotic source distances:")
    for material, data in EXOTIC_SOURCES.items():
        dist = data['distance_km']
        if isinstance(dist, tuple):
            print(f"  {material}: {dist[0]}-{dist[1]} km")
        else:
            print(f"  {material}: {dist} km")
    print(f"\nKnown PP culture sites: {len(KNOWN_SITES)}")
