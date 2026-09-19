def classify_incident(
    title: str,
    description: str,
    incident_type: str = "OTHER"
):
    text = f"{title} {description}".lower()

    # Infer incident type from the report text
    if any(word in text for word in [
        "fire",
        "burning",
        "flames",
        "smoke",
        "blaze"
    ]):
        detected_type = "FIRE"

    elif any(word in text for word in [
        "flood",
        "flooded",
        "water level",
        "waterlogging",
        "overflow"
    ]):
        detected_type = "FLOOD"

    elif any(word in text for word in [
        "accident",
        "collision",
        "crash",
        "vehicle",
        "car",
        "truck"
    ]):
        detected_type = "ACCIDENT"

    elif any(word in text for word in [
        "factory",
        "chemical leak",
        "gas leak",
        "industrial",
        "plant",
        "explosion"
    ]):
        detected_type = "INDUSTRIAL"

    elif any(word in text for word in [
        "heart attack",
        "unconscious",
        "medical",
        "ambulance",
        "injured",
        "injury"
    ]):
        detected_type = "MEDICAL"

    else:
        detected_type = incident_type

    severity = "MEDIUM"
    priority = "NORMAL"
    confidence = 0.60
    reasons = []

    critical_words = [
        "trapped",
        "multiple casualties",
        "many injured",
        "fatality",
        "deceased",
        "collapsed",
        "explosion",
        "major fire",
        "large fire",
    ]

    high_words = [
        "injured",
        "injury",
        "unconscious",
        "heavy smoke",
        "spreading fire",
        "severe flooding",
        "people stranded",
    ]

    if any(word in text for word in critical_words):
        severity = "CRITICAL"
        priority = "HIGH"
        confidence = 0.95
        reasons.append(
            "Critical emergency indicators were detected."
        )

    elif any(word in text for word in high_words):
        severity = "HIGH"
        priority = "HIGH"
        confidence = 0.85
        reasons.append(
            "High-severity emergency indicators were detected."
        )

    else:
        reasons.append(
            "No strong critical or high-severity indicators were detected."
        )

    if detected_type in [
        "FIRE",
        "INDUSTRIAL",
        "ACCIDENT"
    ] and priority == "NORMAL":
        priority = "MEDIUM"

    if detected_type == "FIRE":
        reasons.append(
            "Fire incidents may require rapid emergency response."
        )

    elif detected_type == "FLOOD":
        reasons.append(
            "Flood incidents may require rescue and evacuation support."
        )

    elif detected_type == "ACCIDENT":
        reasons.append(
            "Road accidents may require medical and rescue support."
        )

    elif detected_type == "INDUSTRIAL":
        reasons.append(
            "Industrial incidents may involve multiple hazards."
        )

    elif detected_type == "MEDICAL":
        reasons.append(
            "Medical emergencies may require rapid medical assistance."
        )

    return {
        "incident_type": detected_type,
        "severity": severity,
        "priority": priority,
        "confidence": confidence,
        "reasoning": " ".join(reasons),
    }