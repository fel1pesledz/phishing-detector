from flask import Blueprint, jsonify, request

from app.services import url_analyzer, url_validator

bp = Blueprint("scan", __name__)


@bp.route("/api/scan", methods=["POST"])
def scan():
    payload = request.get_json(silent=True)
    if not payload or "url" not in payload:
        return jsonify({"error": "missing_field", "message": "'url' is required"}), 400

    url = payload["url"]
    is_valid, error_code, message = url_validator.validate(url)
    if not is_valid:
        return jsonify({"error": error_code, "message": message}), 400

    result = url_analyzer.analyze(url)
    return jsonify({
        "url": url,
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "reasons": result["reasons"],
    }), 200
