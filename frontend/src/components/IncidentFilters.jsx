function IncidentFilters({
  severity,
  setSeverity,
  type,
  setType,
  status,
  setStatus,
}) {
  return (
    <div className="incident-filters">
      <select
        value={severity}
        onChange={(event) =>
          setSeverity(event.target.value)
        }
      >
        <option value="">All Severity</option>
        <option value="CRITICAL">Critical</option>
        <option value="HIGH">High</option>
        <option value="MEDIUM">Medium</option>
      </select>

      <select
        value={type}
        onChange={(event) =>
          setType(event.target.value)
        }
      >
        <option value="">All Types</option>
        <option value="FIRE">Fire</option>
        <option value="FLOOD">Flood</option>
        <option value="ACCIDENT">Accident</option>
        <option value="INDUSTRIAL">Industrial</option>
        <option value="MEDICAL">Medical</option>
        <option value="OTHER">Other</option>
      </select>

      <select
        value={status}
        onChange={(event) =>
          setStatus(event.target.value)
        }
      >
        <option value="">All Status</option>
        <option value="ACTIVE">Active</option>
        <option value="ASSIGNED">Assigned</option>
        <option value="RESOLVED">Resolved</option>
      </select>
    </div>
  );
}

export default IncidentFilters;