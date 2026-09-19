function ResourceRecommendations({
  recommendations,
  onStatusChange,
}) {
  return (
    <div className="resource-recommendations">
      <h2>Recommended Resources</h2>

      {recommendations.length === 0 ? (
        <p>No recommendations found.</p>
      ) : (
        recommendations.map((item) => (
          <div
            className="resource-card"
            key={item.id}
          >
            <h3>
              Resource #{item.resource_id}
            </h3>

            <p>
              Score: {item.score}
            </p>

            <p>
              Distance:{" "}
              {item.distance_km !== null
                ? `${item.distance_km} km`
                : "Unknown"}
            </p>

            <p>
              Reason: {item.reason}
            </p>

            <p>
              Status: {item.status}
            </p>

            {item.status === "PENDING" && (
              <>
                <button
                  onClick={() =>
                    onStatusChange(
                      item.id,
                      "ACCEPTED"
                    )
                  }
                >
                  Accept
                </button>

                <button
                  onClick={() =>
                    onStatusChange(
                      item.id,
                      "REJECTED"
                    )
                  }
                >
                  Reject
                </button>
              </>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default ResourceRecommendations;