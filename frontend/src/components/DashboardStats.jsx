function DashboardStats({ incidents }) {
  const activeCount = incidents.filter(
    (incident) => incident.status === "ACTIVE"
  ).length;

  const criticalCount = incidents.filter(
    (incident) => incident.severity === "CRITICAL"
  ).length;

  const highCount = incidents.filter(
    (incident) => incident.severity === "HIGH"
  ).length;

  return (
    <div className="dashboard-stats">
      <div className="stat-card">
        <h3>Active Incidents</h3>
        <p>{activeCount}</p>
      </div>

      <div className="stat-card">
        <h3>Critical Incidents</h3>
        <p>{criticalCount}</p>
      </div>

      <div className="stat-card">
        <h3>High Severity</h3>
        <p>{highCount}</p>
      </div>

      <div className="stat-card">
        <h3>Total Incidents</h3>
        <p>{incidents.length}</p>
      </div>
    </div>
  );
}

export default DashboardStats;