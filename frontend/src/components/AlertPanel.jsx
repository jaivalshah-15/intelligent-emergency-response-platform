function AlertPanel({
  alerts,
  onAcknowledge,
  onResolve,
}) {
  const activeAlerts = alerts.filter(
    (alert) =>
      alert.status !== "RESOLVED"
  );

  return (
    <div className="alert-panel">
      <h2>Active Alerts</h2>

      {activeAlerts.length === 0 ? (
        <p>No active alerts.</p>
      ) : (
        activeAlerts.map((alert) => (
          <div
            className={`alert-card ${alert.level.toLowerCase()}`}
            key={alert.id}
          >
            <h3>{alert.title}</h3>

            <p>
              {alert.message}
            </p>

            <p>
              Level: {alert.level}
            </p>

            <p>
              Status: {alert.status}
            </p>

            {alert.status === "ACTIVE" && (
              <button
                onClick={() =>
                  onAcknowledge(alert.id)
                }
              >
                Acknowledge
              </button>
            )}

            {alert.status !== "RESOLVED" && (
              <button
                onClick={() =>
                  onResolve(alert.id)
                }
              >
                Resolve
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default AlertPanel;