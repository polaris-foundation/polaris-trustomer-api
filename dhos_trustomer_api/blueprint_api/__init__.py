import connexion
from flask import Blueprint, Response, jsonify, request
from flask_batteries_included.helpers.routes import deprecated_route

from dhos_trustomer_api.blueprint_api import controller

api_blueprint = Blueprint("trustomer", __name__)


@api_blueprint.route("/trustomer", methods=["GET"])
@deprecated_route(superseded_by="GET /dhos/v1/trustomer/<customer_code>")
def get_trustomer_config() -> Response:
    """---
    get:
      summary: Get a trustomer's config
      description: Get a trustomer's configuration including product-specific settings
      tags: [trustomer]
      parameters:
        - description: Trustomer code
          in: header
          name: X-Trustomer
          required: true
          schema:
            example: ouh
            type: string
      responses:
        '200':
          description: The requested trustomer's config
          content:
            application/json:
              schema: TrustomerConfigSchema
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    trustomer_code: str = request.headers["X-Trustomer"]
    return jsonify(controller.get_trustomer_config(trustomer_code))


@api_blueprint.route("/escalation_policy/<policy_name>", methods=["GET"])
@deprecated_route(superseded_by="GET /dhos/v1/trustomer/<customer_code>")
def get_escalation_policy_content(policy_name: str) -> Response:
    """---
    get:
      summary: Get a trustomer's escalation policy
      description: Get a trustomer's escalation policy
      tags: [trustomer]
      parameters:
        - name: policy_name
          in: path
          required: true
          description: Policy name
          schema:
            type: string
            example: 'news2'
        - description: Trustomer code
          in: header
          name: X-Trustomer
          required: true
          schema:
            example: ouh
            type: string
      responses:
        '200':
          description: The trustomer's escalation policy
          content:
            application/json:
              schema: EscalationPolicySchema
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    trustomer_code: str = request.headers["X-Trustomer"]
    return jsonify(
        controller.get_escalation_policy_content(
            trustomer_code=trustomer_code, name=policy_name
        )
    )


@api_blueprint.route("/parse_patient_barcode", methods=["POST"])
# This should be done in the SEND BFF, it has no successor in this service.
@deprecated_route(superseded_by=None)
def parse_patient_barcode() -> Response:
    """---
    post:
      summary: Parse a patient barcode
      description: >-
        Parse a patient barcode into its constituent parts, including name and identifiers
      tags: [trustomer]
      parameters:
        - description: Trustomer code
          in: header
          name: X-Trustomer
          required: true
          schema:
            example: ouh
            type: string
      requestBody:
        description: Data for creation of patient barcode
        required: true
        content:
          application/json:
            schema: PatientBarcodeSchema
      responses:
        '200':
          description: Parsed barcode successfully
          content:
            application/json:
              schema: PatientBarcodeResponseSchema
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    barcode: str = connexion.request.get_json()["barcode"]
    trustomer_code: str = request.headers["X-Trustomer"]
    return jsonify(
        controller.parse_patient_barcode(trustomer_code=trustomer_code, barcode=barcode)
    )


@api_blueprint.route("/trustomer/<customer_code>", methods=["GET"])
def get_trustomer_config_by_code(customer_code: str) -> Response:
    """---
    get:
      summary: Get config for the specified trustomer
      description: Get specified trustomer's configuration including product-specific settings
      tags: [trustomer]
      parameters:
        - description: Customer code
          in: path
          name: customer_code
          required: true
          schema:
            example: ouh
            type: string
        - description: Trustomer code
          in: header
          name: X-Trustomer
          required: true
          schema:
            example: ouh
            type: string
        - description: Product name
          in: header
          name: X-Product
          required: true
          schema:
            example: gdm
            type: string
      responses:
        '200':
          description: The requested trustomer's config
          content:
            application/json:
              schema: TrustomerConfigSchema
        default:
          description: Error, e.g. 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    trustomer_code_header: str = request.headers["X-Trustomer"].lower()
    if trustomer_code_header.lower() != customer_code.lower():
        raise PermissionError(
            f"Can't request config for '{customer_code}' with X-Trustomer header '{trustomer_code_header}'"
        )
    return jsonify(controller.get_trustomer_config(customer_code.lower()))
