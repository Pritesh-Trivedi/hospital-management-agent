import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const DEFAULT_CENTER = [19.2288, 72.8567] // Borivali West, Mumbai — fallback map center

async function reverseGeocode(lat, lon) {
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
    )
    const data = await res.json()
    return data.display_name || `${lat.toFixed(4)}, ${lon.toFixed(4)}`
  } catch {
    return `${lat.toFixed(4)}, ${lon.toFixed(4)}`
  }
}

async function searchPlaces(query) {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&limit=5&q=${encodeURIComponent(query)}`
  )
  return res.json()
}

function LocationGate({ onConfirm }) {
  const [mode, setMode] = useState('prompt') // 'prompt' | 'map' | 'locating'
  const [geoError, setGeoError] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [selected, setSelected] = useState(null) // { lat, lon, address }

  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markerRef = useRef(null)

  const placeMarker = async (lat, lon, knownAddress) => {
    if (!mapInstanceRef.current) return

    if (markerRef.current) {
      markerRef.current.remove()
    }
    markerRef.current = L.circleMarker([lat, lon], {
      radius: 9,
      color: '#0f7a8c',
      fillColor: '#0f7a8c',
      fillOpacity: 0.85,
      weight: 2,
    }).addTo(mapInstanceRef.current)

    mapInstanceRef.current.setView([lat, lon], 14)

    const address = knownAddress || (await reverseGeocode(lat, lon))
    setSelected({ lat, lon, address })
  }

  // Initialize the Leaflet map once we enter map mode
  useEffect(() => {
    if (mode !== 'map' || mapInstanceRef.current) return

    const map = L.map(mapRef.current).setView(DEFAULT_CENTER, 12)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map)

    map.on('click', (e) => {
      placeMarker(e.latlng.lat, e.latlng.lng)
    })

    mapInstanceRef.current = map

    // Fix sizing glitch that happens when a Leaflet map is created inside
    // a container that wasn't visible/sized at mount time.
    setTimeout(() => map.invalidateSize(), 100)

    return () => {
      map.remove()
      mapInstanceRef.current = null
    }
  }, [mode])

  const requestBrowserLocation = () => {
    setGeoError('')
    setMode('locating')

    if (!navigator.geolocation) {
      setGeoError('Your browser does not support location access.')
      setMode('map')
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        onConfirm({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        })
      },
      () => {
        setGeoError('Location access was denied or unavailable. Please pick your location on the map instead.')
        setMode('map')
      },
      { enableHighAccuracy: true, timeout: 8000 }
    )
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    const results = await searchPlaces(searchQuery.trim())
    setSearchResults(results)

    if (results.length > 0) {
      const first = results[0]
      placeMarker(parseFloat(first.lat), parseFloat(first.lon), first.display_name)
    }
  }

  const handleSelectResult = (result) => {
    placeMarker(parseFloat(result.lat), parseFloat(result.lon), result.display_name)
    setSearchResults([])
    setSearchQuery(result.display_name)
  }

  const handleConfirmLocation = () => {
    if (!selected) return
    onConfirm({ latitude: selected.lat, longitude: selected.lon })
  }

  const handleChangeLocation = () => {
    setSelected(null)
    setSearchQuery('')
    setSearchResults([])
    if (markerRef.current) {
      markerRef.current.remove()
      markerRef.current = null
    }
  }

  return (
    <div className="location-gate-overlay">
      <div className="location-gate-card">
        {mode === 'prompt' && (
          <>
            <h2 className="location-gate-title">📍 Allow Location Access?</h2>
            <p className="location-gate-text">
              The agent uses your location to find the closest, best-matched hospital.
              You can also enter it manually instead.
            </p>
            <div className="location-gate-actions">
              <button className="location-btn location-btn--primary" onClick={requestBrowserLocation}>
                Yes, use my location
              </button>
              <button className="location-btn location-btn--secondary" onClick={() => setMode('map')}>
                No, let me pick manually
              </button>
            </div>
          </>
        )}

        {mode === 'locating' && (
          <div className="location-gate-loading">
            <span className="spinner" aria-hidden="true"></span>
            <span>Getting your location…</span>
          </div>
        )}

        {mode === 'map' && (
          <>
            <h2 className="location-gate-title">📍 Choose Your Location</h2>
            {geoError && <p className="location-gate-error">{geoError}</p>}

            <form className="location-search-row" onSubmit={handleSearch}>
              <input
                type="text"
                placeholder="Search for a place or address…"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button type="submit" className="location-search-btn">Search</button>
            </form>

            {searchResults.length > 0 && (
              <ul className="location-results-list">
                {searchResults.map((result) => (
                  <li key={result.place_id}>
                    <button type="button" onClick={() => handleSelectResult(result)}>
                      {result.display_name}
                    </button>
                  </li>
                ))}
              </ul>
            )}

            <div ref={mapRef} className="location-map"></div>

            {selected && (
              <p className="location-selected-address">
                <strong>Selected:</strong> {selected.address}
              </p>
            )}

            <div className="location-gate-actions">
              <button
                className="location-btn location-btn--primary"
                onClick={handleConfirmLocation}
                disabled={!selected}
              >
                Confirm Location
              </button>
              <button className="location-btn location-btn--secondary" onClick={handleChangeLocation}>
                Change Location
              </button>
              <button className="location-btn location-btn--tertiary" onClick={requestBrowserLocation}>
                Use Current Location Instead
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default LocationGate
