SECTIONS = {
    "io", "stft", "start_time", "carrier", "velocity",
    "material", "spall", "hel", "uncertainty", "plotting",
}


def flatten_config(config: dict) -> dict:
    """Flatten a nested section-based config into a single flat dict.

    Raises ValueError if no recognised section keys are found, if unknown
    sections are present, or if the same key appears in multiple sections.
    """
    has_sections = any(k in SECTIONS for k in config)
    if not has_sections:
        raise ValueError(
            f"Config must use nested sections. "
            f"Expected top-level keys from: {sorted(SECTIONS)}. "
            f"Got: {sorted(config.keys())}"
        )
    unknown = [k for k in config if k not in SECTIONS]
    if unknown:
        raise ValueError(
            f"Unknown config sections: {unknown}. "
            f"Valid sections are: {sorted(SECTIONS)}"
        )
    flat = {}
    for section, value in config.items():
        if isinstance(value, dict):
            clashes = [k for k in value if k in flat]
            if clashes:
                raise ValueError(
                    f"Config key collision in section '{section}': "
                    f"{clashes} already defined in a previous section."
                )
            flat.update(value)
    return flat
