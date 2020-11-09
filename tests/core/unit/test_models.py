from tests.core import data

from ispyb_core import schemas


def test_data_collection_model():
    data_collection = schemas.data_collection.DataCollectionSchema().dump(data.test_data_collection)

    assert data_collection.errors == {}


def test_proposal_model():
    proposal = schemas.proposal.ProposalSchema().dump(data.test_proposal)

    assert proposal.errors == {}

def test_session_model():
    session = schemas.session.SessionSchema().dump(data.test_session)

    assert session.errors == {}

def test_local_contact_model():
    local_contact = schemas.lab_contact.LabContactSchema().dump(data.test_local_contact)

    assert local_contact.errors == {}

def test_shipment():
    shipmenmt = schemas.shipping.ShippingSchema().dump(data.test_shippment)

    assert shipmenmt.errors == {}
