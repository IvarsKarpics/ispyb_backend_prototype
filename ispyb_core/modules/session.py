"""
Project: py-ispyb
https://github.com/ispyb/py-ispyb

This file is part of py-ispyb software.

py-ispyb is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-ispyb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.
"""


__license__ = "LGPLv3+"


from app.extensions import db

from ispyb_core import models, schemas

from ispyb_core.modules import beamline_setup, data_collection, proposal


def get_sessions(request):
    """Returns session based on query parameters

    Args:
        query_params ([type]): [description]

    Returns:
        [type]: [description]
    """
    query_params = request.args.to_dict()

    return db.get_db_items(
        models.BLSession,
        schemas.session.dict_schema,
        schemas.session.ma_schema,
        query_params
    )


def add_session(data_dict):
    """Adds new session

    Args:
        session_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    return db.add_db_item(
        models.BLSession,
        schemas.session.ma_schema,
        data_dict
        )


def get_session_by_id(session_id):
    """Returns session info by its sessionId

    Args:
        session_id (int): corresponds to sessionId in db

    Returns:
        dict: info about session as dict
    """
    data_dict = {"sessionId": session_id}
    return db.get_db_item_by_params(
        models.BLSession,
        schemas.session.ma_schema,
        data_dict
        )


def get_session_info_by_id(session_id):
    """Returns session info by its sessionId

    Args:
        session_id (int): corresponds to sessionId in db

    Returns:
        dict: info about session as dict
    """
    session_json = get_session_by_id(session_id)
    if session_json:
        session_json["proposal"] = proposal.get_proposal_by_id(
            session_json["proposalId"]
        )
        session_json["beamline_setup"] = beamline_setup.get_beamline_setup_by_id(
            session_json["beamLineSetupId"]
        )
        # session_json["data_collections_groups"] = data_collection.get_data_collection_groups({"sessionId" : session_id})["data"]["rows"]

    return session_json
