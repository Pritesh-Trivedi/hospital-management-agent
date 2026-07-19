# Default fallback location: Borivali West, Mumbai — used only if the
# frontend didn't provide coordinates (e.g. location permission denied
# and no manual location was set). In production you'd want to force
# the frontend to always send *something* before reaching this node.
DEFAULT_LATITUDE = 19.2288
DEFAULT_LONGITUDE = 72.8567

def location_node(state):

    lat = state.get("patient_latitude")
    lon = state.get("patient_longitude")

    if lat is None or lon is None:
        state["patient_latitude"] = DEFAULT_LATITUDE
        state["patient_longitude"] = DEFAULT_LONGITUDE

        state["steps"].append(
            "Location: no coordinates provided, using default location"
        )
    else:
        state["steps"].append(
            f"Location: patient location received ({lat:.4f}, {lon:.4f})"
        )

    return state