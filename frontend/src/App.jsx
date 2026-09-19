import { useEffect, useState } from "react";      
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
   const [incidents, setIncidents] = useState([]);
   const [loading, setLoading] = useState(true);
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
  useEffect(() => {
  fetchIncidents();
  }, []);
  async function fetchIncidents() {
    try {
      const response = await fetch(
        `${API_URL}/api/incidents/`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch incidents");
      }
      const data = await response.json();

      setIncidents(data);
    } catch (error) {
        setError(error.message);
      } 
      finally {
        setLoading(false);
      }
  }
 

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setError("");

    const dataToSend = {
      title: formData.title,
      description: formData.description,
      incident_type: formData.incident_type,
      source: formData.source,
      address: formData.address || null,
      latitude: formData.latitude
        ? Number(formData.latitude)
        : null,
      longitude: formData.longitude
        ? Number(formData.longitude)
        : null,
    };

    try {
      const response = await fetch(
        `${API_URL}/api/incidents/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(dataToSend),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Failed to create incident"
        );
      }

      const result = await response.json();
      await fetchIncidents();
      setMessage(
        `Incident created successfully. ID: ${result.id}`
      );

      setFormData({
        title: "",
        description: "",
        incident_type: "FIRE",
        source: "CITIZEN",
        address: "",
        latitude: "",
        longitude: "",
      });
    } catch (error) {
      setError(error.message);
    }
  }

  return (
    <div className="app">
      <div className="form-container">
        <h1>Report an Emergency</h1>

        <form onSubmit={handleSubmit}>
          <label>Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Example: Factory Fire"
            required
          />

          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the emergency"
            required
          />

          <label>Incident Type</label>
          <select
            name="incident_type"
            value={formData.incident_type}
            onChange={handleChange}
          >
            <option value="FIRE">Fire</option>
            <option value="FLOOD">Flood</option>
            <option value="ACCIDENT">Road Accident</option>
            <option value="INDUSTRIAL">Industrial Accident</option>
            <option value="MEDICAL">Medical Emergency</option>
            <option value="OTHER">Other</option>
          </select>

          <label>Source</label>
          <select
            name="source"
            value={formData.source}
            onChange={handleChange}
          >
            <option value="CITIZEN">Citizen</option>
            <option value="FIELD_TEAM">Field Team</option>
            <option value="SENSOR">Sensor</option>
            <option value="EMERGENCY_CALL">
              Emergency Call
            </option>
          </select>

          <label>Address</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="Example: Ahmedabad"
          />

          <label>Latitude</label>
          <input
            type="number"
            step="any"
            name="latitude"
            value={formData.latitude}
            onChange={handleChange}
            placeholder="Example: 23.0225"
          />

          <label>Longitude</label>
          <input
            type="number"
            step="any"
            name="longitude"
            value={formData.longitude}
            onChange={handleChange}
            placeholder="Example: 72.5714"
          />

          <button type="submit">
            Submit Incident
          </button>
        </form>
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
              </div>
            ))
          )}
        </div>

        {message && (
          <p className="message">
            {message}
          </p>
        )}

        {error && (
          <p className="error">
            Error: {error}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;