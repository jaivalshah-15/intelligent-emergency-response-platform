function IncidentDashboard({ incidents }) {
  return (
    <div className="incident-dashboard">
      <h2>Incident Monitoring</h2>

      {incidents.length === 0 ? (
        <p>No incidents found.</p>
      ) : (
        <div className="incident-table-wrapper">
          <table className="incident-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Source</th>
              </tr>
            </thead>

            <tbody>
              {incidents.map((incident) => (
                <tr key={incident.id}>
                  <td>{incident.id}</td>
                  <td>{incident.title}</td>
                  <td>{incident.incident_type}</td>
                  <td>{incident.severity}</td>
                  <td>{incident.priority}</td>
                  <td>{incident.status}</td>
                  <td>{incident.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default IncidentDashboard;