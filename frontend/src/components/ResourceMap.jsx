import {
  Marker,
  Popup,
} from "react-leaflet";

function ResourceMap({ resources }) {
  return (
    <>
      {resources
        .filter(
          (resource) =>
            resource.latitude !== null &&
            resource.longitude !== null
        )
        .map((resource) => (
          <Marker
            key={`resource-${resource.id}`}
            position={[
              resource.latitude,
              resource.longitude,
            ]}
          >
            <Popup>
              <strong>
                Resource #{resource.id}
              </strong>

              <br />

              Type: {resource.resource_type}

              <br />

              Status: {resource.status}
            </Popup>
          </Marker>
        ))}
    </>
  );
}

export default ResourceMap;