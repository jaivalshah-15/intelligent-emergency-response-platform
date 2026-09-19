import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import ResourceMap from "./ResourceMap";
import HospitalMap from "./HospitalMap";

function IncidentMap({
  incidents,
  resources = [],
  hospitals = [],
}) {
  const validIncidents = incidents.filter(
    (incident) =>
      incident.latitude !== null &&
      incident.longitude !== null
  );

  const center =
    validIncidents.length > 0
      ? [
          validIncidents[0].latitude,
          validIncidents[0].longitude,
        ]
      : [23.0225, 72.5714];

  return (
    <div className="map-container">
      <MapContainer
        center={center}
        zoom={12}
        style={{
          height: "500px",
          width: "100%",
        }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {validIncidents.map((incident) => (
          <Marker
            key={incident.id}
            position={[
              incident.latitude,
              incident.longitude,
            ]}
          >
            <Popup>
              <strong>
                #{incident.id} - {incident.title}
              </strong>

              <br />

              Type: {incident.incident_type}

              <br />

              Severity: {incident.severity}

              <br />

              Priority: {incident.priority}

              <br />

              Status: {incident.status}
            </Popup>
          </Marker>
        ))}

        <ResourceMap resources={resources} />
        <HospitalMap hospitals={hospitals} />
      </MapContainer>
    </div>
  );
}

export default IncidentMap;