
from marshmallow import Schema, fields as ma_fields
from flask_restplus import fields as f_fields

proposal_dict = {
        'proposalId': f_fields.Integer(required=True, description=''),
        'personId': f_fields.Integer(required=True, description=''),
        'title': f_fields.String(required=False, description=''),
        'proposalCode': f_fields.String(required=False, description=''),
        'proposalNumber': f_fields.String(required=False, description=''),
        'proposalType': f_fields.String(required=False, description='Proposal type: MX, BX'),
        'bltimeStamp': f_fields.DateTime(required=True, description=''),
        'externalId': f_fields.Integer(required=False, description=''),
        'state': f_fields.String(required=False, description='enum(Open,Closed,Cancelled)'),
        }

class ProposalSchema(Schema):
    proposalId = ma_fields.Integer()
    personId = ma_fields.Integer()
    title = ma_fields.String()
    proposalCode = ma_fields.String()
    proposalNumber = ma_fields.String()
    proposalType = ma_fields.String()
    bltimeStamp = ma_fields.DateTime()
    externalId = ma_fields.Integer()
    state = ma_fields.String()
