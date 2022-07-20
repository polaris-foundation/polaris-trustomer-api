from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import INCLUDE, Schema, fields

dhos_trustomer_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Trustomer API",
    info={
        "description": "The DHOS Trustomer API is responsible for managing trustomer configuration"
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)


@openapi_schema(dhos_trustomer_api_spec)
class PatientBarcodeSchema(Schema):
    class Meta:
        title = "Patient barcode format"
        unknown = INCLUDE
        ordered = True

    barcode = fields.String(
        description="Patient barcode", required=True, example="12345"
    )


@openapi_schema(dhos_trustomer_api_spec)
class PatientBarcodeResponseSchema(Schema):
    class Meta:
        title = "Parsed patient barcode"
        unknown = INCLUDE
        ordered = True

    firstname = fields.String(description="Patient's first name", example="John")
    lastname = fields.String(description="Patient's last name", example="Smith")
    sex = fields.String(description="Patient's sex", example="M", enum=["M", "F", "U"])
    nhs = fields.String(description="Patient's NHS Number", example="111222333")
    mrn = fields.String(
        description="Patient's Medical Record Number", example="111222333"
    )


@openapi_schema(dhos_trustomer_api_spec)
class TrustomerConfigSchema(Schema):
    class Meta:
        title = "Trustomer details"
        unknown = INCLUDE
        ordered = True

    gdm_config = fields.Dict(keys=fields.String(), required=True)
    send_config = fields.Dict(keys=fields.String(), required=True)
    gdm_clinician_terms_content = fields.String(
        description="Clinician terms of use (HTML)",
        example="Lorem ipsum",
        required=True,
    )
    gdm_clinician_terms_version = fields.String(
        description="Version number of clinician terms of use",
        example="1",
        required=True,
    )
    gdm_terms_content = fields.String(
        description="Patient terms of use (HTML)", example="Lorem ipsum", required=True
    )
    gdm_terms_version = fields.String(
        description="Version number of patient terms of use", example="1", required=True
    )
    hl7_config = fields.Dict(keys=fields.String(), required=True)
    measurement_system = fields.String(
        description="System of measurement", example="metric", required=True
    )
    created = fields.DateTime(
        description="Record creation date/time",
        example="2017-09-23T08:29:19.123+00:00",
        required=True,
    )
    gdm_phone_midwife = fields.String(
        description="Midwife telephone number", example="07777777777", required=True
    )
    gdm_phone_ward = fields.String(
        description="Ward telephone number", example="01276777777", required=True
    )
    modified = fields.DateTime(
        description="Record modification date/time",
        example="2017-09-23T08:29:19.123+00:00",
        required=True,
    )
    name = fields.String(
        description="Trust description",
        example="Forest NHS Foundation Trust",
        required=True,
    )
    uuid = fields.String(
        description="UUID of the Trustomer configuration record",
        example="2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
        required=True,
    )


@openapi_schema(dhos_trustomer_api_spec)
class EscalationPolicySchema(Schema):
    class Meta:
        title = "Trustomer escalation policy"
        unknown = INCLUDE
        ordered = True

    routine_monitoring = fields.String(
        description="Routine monitoring instructions", example="Do something"
    )
    low_monitoring = fields.String(
        description="Low monitoring instructions", example="Do something"
    )
    low_medium_monitoring = fields.String(
        description="Low medium monitoring instructions", example="Do something"
    )
    medium_monitoring = fields.String(
        description="Medium monitoring instructions", example="Do something"
    )
    high_monitoring = fields.String(
        description="High monitoring instructions", example="Do something"
    )


initialise_apispec(dhos_trustomer_api_spec)
