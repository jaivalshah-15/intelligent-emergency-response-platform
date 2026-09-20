import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = (
  import.meta.env.VITE_API_URL || "http://localhost:8000"
).replace(/\/$/, "");

function App() {
  const [wsConnected, setWsConnected] = useState(false);
  const [incidents, setIncidents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [alertLoading, setAlertLoading] = useState(true);
  const [assistantResults, setAssistantResults] = useState({});
  const [assistantLoadingId, setAssistantLoadingId] = useState(null);
  const [assistantError, setAssistantError] = useState("");
  const [analytics, setAnalytics] = useState(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    incident_type: "FIRE",
    source: "CITIZEN",
    address: "",
    latitude: "",
    longitude: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // =========================
  // FETCH INCIDENTS
  // =========================
  async function fetchIncidents() {
    try {
      const response = await fetch(`${API_URL}/api/incidents/`);

      if (!response.ok) {
        throw new Error("Failed to fetch incidents");
      }

      const data = await response.json();
      setIncidents(data);
    } catch (err) {
      console.error("Incident fetch error:", err);
      setError("Unable to load incidents.");
    } finally {
      setLoading(false);
    }
  }

  // =========================
  // FETCH ALERTS
  // =========================
  async function fetchAlerts() {
    try {
      const response = await fetch(`${API_URL}/api/alerts/`);

      if (!response.ok) {
        throw new Error("Failed to fetch alerts");
      }

      const data = await response.json();
      setAlerts(data);
    } catch (err) {
      console.error("Alert fetch error:", err);
    } finally {
      setAlertLoading(false);
    }
  }

  // =========================
  // fetchassistantsummary
  // =========================

async function fetchAssistantSummary(incidentId) {
  setAssistantLoadingId(incidentId);
  setAssistantError("");

  try {
    const response = await fetch(
      `${API_URL}/api/incidents/${incidentId}/summary`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to generate AI assistance"
      );
    }

    setAssistantResults((previous) => ({
      ...previous,
      [incidentId]: data,
    }));
  } catch (err) {
    console.error("AI assistant error:", err);
    setAssistantError(err.message);
  } finally {
    setAssistantLoadingId(null);
  }
}
  // =========================
  // FETCH ANALYTICS
  // =========================
async function fetchAnalytics() {
  try {
    const response = await fetch(`${API_URL}/api/analytics/`);

    if (!response.ok) {
      throw new Error("Failed to fetch analytics");
    }

    const data = await response.json();
    setAnalytics(data);
  } catch (err) {
    console.error("Analytics fetch error:", err);
  } finally {
    setAnalyticsLoading(false);
  }
}
  // =========================
  // LOAD DATA
  // =========================
 useEffect(() => {
    fetchIncidents();
    fetchAlerts();
    fetchAnalytics();

    const dataInterval = setInterval(() => {
      fetchIncidents();
      fetchAlerts();
      fetchAnalytics();
    }, 5000);

    return () => clearInterval(dataInterval);
  }, []);
  

  useEffect(() => {
  let socket;
  let reconnectTimer;

  const connectWebSocket = () => {
    const wsUrl = `${API_URL.replace(/^http/, "ws")}/api/ws`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      setWsConnected(true);
    };

    socket.onmessage = async () => {
      await fetchIncidents();
      await fetchAlerts();
      await fetchAnalytics();
    };

    socket.onclose = () => {
      setWsConnected(false);
      reconnectTimer = setTimeout(connectWebSocket, 3000);
    };

    socket.onerror = () => {
      setWsConnected(false);
    };
  };
  connectWebSocket();
  return () => {
    clearTimeout(reconnectTimer);
    if (socket) {
      socket.close();
    }
  };
}, []);

  // =========================
  // HANDLE FORM INPUT
  // =========================
  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  // =========================
  // CREATE INCIDENT
  // =========================
  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setError("");

    try {
      const payload = {
        title: formData.title,
        description: formData.description,
        incident_type: formData.incident_type,
        source: formData.source,
        address: formData.address,
        latitude:
          formData.latitude === "" ? null : Number(formData.latitude),
        longitude:
          formData.longitude === "" ? null : Number(formData.longitude),
      };

      const response = await fetch(`${API_URL}/api/incidents/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail
            ? JSON.stringify(result.detail)
            : "Failed to create incident"
        );
      }

      setMessage(`Incident created successfully. ID: ${result.id}`);

      // Refresh both incidents and alerts
      await fetchIncidents();
      await fetchAlerts();
      await fetchAnalytics();

      // Clear form
      setFormData({
        title: "",
        description: "",
        incident_type: "FIRE",
        source: "CITIZEN",
        address: "",
        latitude: "",
        longitude: "",
      });
    } catch (err) {
      console.error("Create incident error:", err);
      setError(err.message || "Failed to create incident.");
    }
  }

  // =========================
  // ACKNOWLEDGE ALERT
  // =========================
  async function acknowledgeAlert(alertId) {
    try {
      const response = await fetch(
        `${API_URL}/api/alerts/${alertId}/acknowledge`,
        {
          method: "PATCH",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to acknowledge alert");
      }

      await fetchAlerts();
    } catch (err) {
      console.error("Acknowledge alert error:", err);
      setError("Unable to acknowledge alert.");
    }
  }

  // =========================
  // RESOLVE ALERT
  // =========================
  async function resolveAlert(alertId) {
    try {
      const response = await fetch(
        `${API_URL}/api/alerts/${alertId}/resolve`,
        {
          method: "PATCH",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to resolve alert");
      }

      await fetchAlerts();
    } catch (err) {
      console.error("Resolve alert error:", err);
      setError("Unable to resolve alert.");
    }
  }
  
  // =========================
  // RESOLVE INCIDENT
  // =========================
async function resolveIncident(incidentId) {
  const confirmed = window.confirm(
    `Resolve incident #${incidentId}? This will remove it from the active incident list.`
  );

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/api/incidents/${incidentId}/resolve`,
      {
        method: "PATCH",
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "Failed to resolve incident"
      );
    }

    setMessage(
      `Incident #${incidentId} resolved and deleted.`
    );

    await fetchIncidents();
    await fetchAlerts();
    await fetchAnalytics();
  } catch (err) {
    console.error("Resolve incident error:", err);
    setError(
      err.message || "Unable to resolve incident."
    );
  }
}
  // =========================
  // ACTIVE ALERTS
  // =========================
  const activeAlerts = alerts.filter(
    (alert) => alert.status !== "RESOLVED"
  );

  return (
    <div className="app">
      <header className="app-header">
        <h1>Intelligent Emergency Response Platform</h1>
        <p>Emergency incident monitoring and response dashboard</p>
      </header>

      <main className="app-container">

        {/* =========================
            ALERT PANEL
        ========================= */}
        <div className="alert-panel">
          <h2>🚨 Emergency Alerts</h2>

          {alertLoading ? (
            <p>Loading alerts...</p>
          ) : activeAlerts.length === 0 ? (
            <p>No active alerts.</p>
          ) : (
            activeAlerts.map((alert) => (
              <div
                key={alert.id}
                className={`alert-card ${alert.level.toLowerCase()}`}
              >
                <h3>
                  {alert.level === "CRITICAL" ? "🚨 " : "⚠️ "}
                  {alert.title}
                </h3>

                <p>{alert.message}</p>

                <p>
                  <strong>Level:</strong> {alert.level}
                </p>

                <p>
                  <strong>Incident ID:</strong> #{alert.incident_id}
                </p>

                <p>
                  <strong>Status:</strong> {alert.status}
                </p>

                <p>
                  <strong>Created:</strong>{" "}
                  {new Date(alert.created_at).toLocaleString()}
                </p>

                <div className="alert-actions">
                  {alert.status === "ACTIVE" && (
                    <button
                      type="button"
                      onClick={() => acknowledgeAlert(alert.id)}
                    >
                      Acknowledge
                    </button>
                  )}

                  {alert.status !== "RESOLVED" && (
                    <button
                      type="button"
                      onClick={() => resolveAlert(alert.id)}
                    >
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
        
        <div className="analytics-panel">
            <h2>📊 Emergency Analytics</h2>

                {analyticsLoading ? (
            <p>Loading analytics...</p>
          ) : !analytics ? (
            <p>Analytics unavailable.</p>
          ) : (
      <>
          <div className="analytics-cards">

          <div className="analytics-card">
            <h3>Total Incidents</h3>
            <p>{analytics.total_incidents}</p>
          </div>

        <div className="analytics-card">
          <h3>Active Incidents</h3>
          <p>{analytics.active_incidents}</p>
        </div>

        <div className="analytics-card">
          <h3>Critical Incidents</h3>
          <p>{analytics.critical_incidents}</p>
        </div>

        <div className="analytics-card">
          <h3>High Priority</h3>
          <p>{analytics.high_priority_incidents}</p>
        </div>

        <div className="analytics-card">
          <h3>Active Alerts</h3>
          <p>{analytics.active_alerts}</p>
        </div>

        <div className="analytics-card">
          <h3>Available Resources</h3>
          <p>{analytics.available_resources}</p>
        </div>

        <div className="analytics-card">
          <h3>Assigned Resources</h3>
          <p>{analytics.assigned_resources}</p>
        </div>

        <div className="analytics-card">
          <h3>Active Assignments</h3>
          <p>{analytics.active_assignments}</p>
        </div>

      </div>
      <div className="analytics-section">
        <h3>Incidents by Type</h3>
          {Object.entries(analytics.incidents_by_type).map(
          ([type, count]) => (
      <div className="analytics-row" key={type}>
            <span>{type}</span>
            <strong>{count}</strong>
      </div>
          )
        )}
      </div>

      <div className="analytics-section">
        <h3>Incidents by Severity</h3>

        {Object.entries(analytics.incidents_by_severity).map(
          ([severity, count]) => (
            <div className="analytics-row" key={severity}>
              <span>{severity}</span>
              <strong>{count}</strong>
            </div>
          )
        )}
      </div>

      <div className="analytics-section">
        <h3>Incidents by Priority</h3>

        {Object.entries(analytics.incidents_by_priority).map(
          ([priority, count]) => (
            <div className="analytics-row" key={priority}>
              <span>{priority}</span>
              <strong>{count}</strong>
            </div>
          )
        )}
      </div>

      <div className="analytics-section">
              <h3>Alerts by Level</h3>
              {Object.entries(analytics.alerts_by_level).map(
                ([level, count]) => (
                  <div className="analytics-row" key={level}>
                    <span>{level}</span>
                    <strong>{count}</strong>
                  </div>
                )
              )}
            </div>
          </>
        )}
      </div>

      <div className="map-panel">
  <div className="panel-header">
    <h2>🗺️ Emergency Map</h2>
    <span className={wsConnected ? "ws-status connected" : "ws-status"}>
      {wsConnected ? "● Live" : "○ Offline"}
    </span>
  </div>

  <MapContainer
    center={[22.3072, 73.1812]}
    zoom={11}
    scrollWheelZoom={true}
    className="emergency-map"
  >
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />

    {incidents
      .filter(
        (incident) =>
          incident.latitude !== null &&
          incident.longitude !== null
      )
      .map((incident) => (
        <CircleMarker
          key={incident.id}
          center={[incident.latitude, incident.longitude]}
          radius={10}
        >
          <Popup>
            <strong>{incident.title}</strong>
            <br />
            Type: {incident.incident_type}
            <br />
            Severity: {incident.severity}
            <br />
            Priority: {incident.priority}
            <br />
            Status: {incident.status}
          </Popup>
        </CircleMarker>
      ))}
  </MapContainer>
</div>
        {/* =========================
            CREATE INCIDENT
        ========================= */}
        <div className="incident-form-section">
          <h2>Report New Incident</h2>

          {message && (
            <p className="success-message">
              {message}
            </p>
          )}

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <form onSubmit={handleSubmit} className="incident-form">

            <label>
              Title
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Enter incident title"
                required
              />
            </label>

            <label>
              Description
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe the emergency"
                rows="4"
                required
              />
            </label>

            <label>
              Incident Type
              <select
                name="incident_type"
                value={formData.incident_type}
                onChange={handleChange}
              >
                <option value="FIRE">FIRE</option>
                <option value="FLOOD">FLOOD</option>
                <option value="ACCIDENT">ACCIDENT</option>
                <option value="INDUSTRIAL">INDUSTRIAL</option>
                <option value="MEDICAL">MEDICAL</option>
                <option value="OTHER">OTHER</option>
              </select>
            </label>

            <label>
              Source
              <select
                name="source"
                value={formData.source}
                onChange={handleChange}
              >
                <option value="CITIZEN">CITIZEN</option>
                <option value="SENSOR">SENSOR</option>
                <option value="EMERGENCY_CALL">EMERGENCY_CALL</option>
                <option value="FIELD_TEAM">FIELD_TEAM</option>
              </select>
            </label>

            <label>
              Address
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Enter location"
              />
            </label>

            <label>
              Latitude
              <input
                type="number"
                step="any"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                placeholder="e.g. 22.3072"
              />
            </label>

            <label>
              Longitude
              <input
                type="number"
                step="any"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                placeholder="e.g. 73.1812"
              />
            </label>

            <button type="submit">
              Report Incident
            </button>
          </form>
        </div>

        {/* =========================
            INCIDENT LIST
        ========================= */}
        <div className="incident-list">
          <h2>Active Incidents</h2>

          {loading ? (
            <p>Loading incidents...</p>
          ) : incidents.length === 0 ? (
            <p>No incidents found.</p>
          ) : (
            incidents.map((incident) => (
              <div
                className="incident-card"
                key={incident.id}
              >
                <h3>
                  #{incident.id} - {incident.title}
                </h3>

                <p>
                  <strong>Type:</strong>{" "}
                  {incident.incident_type}
                </p>

                <p>
                  <strong>Severity:</strong>{" "}
                  {incident.severity}
                </p>

                <p>
                  <strong>Priority:</strong>{" "}
                  {incident.priority}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {incident.status}
                </p>

                <p>
                  <strong>Source:</strong>{" "}
                  {incident.source}
                </p>

                <p>
                  <strong>Address:</strong>{" "}
                  {incident.address || "Not provided"}
                </p>

                <p>
                  <strong>AI Confidence:</strong>{" "}
                  {incident.classification_confidence !== null &&
                  incident.classification_confidence !== undefined
                    ? `${Math.round(
                        incident.classification_confidence * 100
                      )}%`
                    : "Not available"}
                </p>

                <p>
                  <strong>AI Reason:</strong>{" "}
                  {incident.classification_reasoning ||
                    "Not available"}
                </p>

                <p>
                  <strong>Reported:</strong>{" "}
                  {incident.reported_at
                    ? new Date(
                        incident.reported_at
                      ).toLocaleString()
                    : "Not available"}
                </p>
                <button
                  type="button"
                  className="resolve-incident-button"
                  onClick={() => resolveIncident(incident.id)}
                >
                  ✅ Resolve Incident
                </button>
                <button
                    type="button"
                    className="ai-assistant-button"
                    onClick={() => fetchAssistantSummary(incident.id)}
                    disabled={assistantLoadingId === incident.id}
                  >
                    {assistantLoadingId === incident.id
                      ? "Generating..."
                      : "🤖 AI Assistance"}
                </button>

                  {assistantError && (
                    <p className="assistant-error">
                      {assistantError}
                    </p>
                  )}

                  {assistantResults[incident.id] && (
                    <div className="assistant-panel">
                      <h4>🤖 AI Incident Assistance</h4>

                      <p>
                        <strong>Summary:</strong>{" "}
                        {assistantResults[incident.id].summary}
                      </p>

                      <p>
                        <strong>Situation:</strong>{" "}
                        {assistantResults[incident.id].situation}
                      </p>

                      <div>
                        <strong>Key Findings:</strong>
                        <ul>
                          {assistantResults[incident.id].key_findings.map(
                            (item, index) => (
                              <li key={index}>{item}</li>
                            )
                          )}
                        </ul>
                      </div>

                      <div>
                        <strong>Recommended Actions:</strong>
                        <ul>
                          {assistantResults[incident.id].recommended_actions.map(
                            (item, index) => (
                              <li key={index}>{item}</li>
                            )
                          )}
                        </ul>
                      </div>

                      <div>
                        <strong>Recommended Resources:</strong>
                        <ul>
                          {assistantResults[incident.id].resource_needs.map(
                            (item, index) => (
                              <li key={index}>{item}</li>
                            )
                          )}
                        </ul>
                      </div>

                      <p>
                        <strong>Generated by:</strong>{" "}
                        {assistantResults[incident.id].generated_by}
                      </p>
                    </div>
                  )}
              </div>
            ))
          )}
        </div>

      </main>
    </div>
  );
}

export default App;