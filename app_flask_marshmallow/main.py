import requests
from flask import Flask, request
from marshmallow import Schema, fields, validate


app = Flask(__name__)


class LocationSchema(Schema):
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)


class SkillSchema(Schema):
    subject = fields.Str(required=True)
    subject_id = fields.Integer(required=True)
    category = fields.Str(required=True)
    qual_level = fields.Str(required=True)
    qual_level_id = fields.Integer(required=True)
    qual_level_ranking = fields.Float(default=0)


class Model(Schema):
    id = fields.Integer(required=True)
    client_name = fields.Str(validate=validate.Length(max=255), required=True)
    sort_index = fields.Float(required=True)
    client_phone = fields.Str(validate=validate.Length(max=255), allow_none=True)

    location = fields.Nested(LocationSchema)

    contractor = fields.Integer(validate=validate.Range(min=0), allow_none=True)
    upstream_http_referrer = fields.Str(validate=validate.Length(max=1023), allow_none=True)
    grecaptcha_response = fields.Str(validate=validate.Length(min=20, max=1000), required=True)
    last_updated = fields.DateTime(allow_none=True)

    skills = fields.Nested(SkillSchema, many=True)


model_schema = Model()


@app.route("/api/create", methods=["POST"])
def create():
    json_data = request.get_json()
    data = model_schema.load(json_data)
    return {"success": True}, 201


@app.route("/api/iojob", methods=["GET"])
def iojob():
    response = requests.get('http://network_service:8000/job')
    assert response.status_code == 200
    return {"success": True}, 200
