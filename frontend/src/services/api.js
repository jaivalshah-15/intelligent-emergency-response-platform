const API_URL = import.meta.env.VITE_API_URL;

export async function fetchResources() {
  const response = await fetch(
    `${API_URL}/api/resources/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch resources");
  }

  return response.json();
}

export async function fetchHospitals() {
  const response = await fetch(
    `${API_URL}/api/hospitals/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch hospitals");
  }

  return response.json();
}

export async function fetchAssignments() {
  const response = await fetch(
    `${API_URL}/api/assignments/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch assignments");
  }

  return response.json();
}

export async function fetchAlerts() {
  const response = await fetch(
    `${API_URL}/api/alerts/`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch alerts"
    );
  }

  return response.json();
}


export async function acknowledgeAlert(
  alertId
) {
  const response = await fetch(
    `${API_URL}/api/alerts/${alertId}/acknowledge`,
    {
      method: "PATCH",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to acknowledge alert"
    );
  }

  return response.json();
}


export async function resolveAlert(
  alertId
) {
  const response = await fetch(
    `${API_URL}/api/alerts/${alertId}/resolve`,
    {
      method: "PATCH",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to resolve alert"
    );
  }

  return response.json();
}