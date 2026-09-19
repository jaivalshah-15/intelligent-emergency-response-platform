function ResourceAssignment({
  incidentId,
  resourceId,
  onAssigned,
}) {
  async function assignResource() {
    try {
      const response = await fetch(
        "http://localhost:8000/api/assignments/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            incident_id: incidentId,
            resource_id: resourceId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Failed to assign resource"
        );
      }

      const data = await response.json();

      onAssigned(data);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <button onClick={assignResource}>
      Assign Resource
    </button>
  );
}

export default ResourceAssignment;