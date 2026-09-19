import { Marker, Popup } from "react-leaflet";

function HospitalMap({ hospitals }) {
  return (
    <>
      {hospitals
        .filter(
          (hospital) =>
            hospital.latitude !== null &&
            hospital.longitude !== null
        )
        .map((hospital) => (
          <Marker
            key={`hospital-${hospital.id}`}
            position={[
              hospital.latitude,
              hospital.longitude,
            ]}
          >
            <Popup>
              <strong>
                {hospital.name}
              </strong>

              <br />

              Available Beds:{" "}
              {hospital.available_beds}

              <br />

              Status: {hospital.status}
            </Popup>
          </Marker>
        ))}
    </>
  );
}

export default HospitalMap;