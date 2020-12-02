"""
Project: py-ispyb.

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
from app.extensions.auth import auth_provider
from app.utils import create_response_item

from ispyb_core import models, schemas

from ispyb_core.modules import beamline_setup, session, proposal


def get_sessions(request):
    """
    Returns session based on query parameters.

    Args:
        query_params ([type]): [description]

    Returns:
        [type]: [description]
    """
    query_params = request.args.to_dict()

    user_info = auth_provider.get_user_info_by_auth_header(
        request.headers.get("Authorization")
    )

    # If the user has no admin role then allow retreive sessions 
    # from particular proposals
    # 
    # Do we need to retrieve sessions from all proposals?
    # Add sessions from session_has_person
    run_query = False
    msg = None

    if user_info.get("is_admin"):
        run_query = True
    else:
        if "proposalId" not in query_params.keys():
            msg = "User is not admin. No proposalId in query parameters"
        else:
            # Check if proposal belongs to the person
            user_proposals, status_code = proposal.get_proposals(request)
            for user_proposal in user_proposals["data"]["rows"]:
                if user_proposal.get("proposalId") == int(query_params.get("proposalId")):
                    run_query = True
                    break
            
            if not run_query:
                msg = "Proposal with id %s is not associated with user %s" % (
                    query_params.get("proposalId"),
                    user_info.get("username")
                )

    if run_query:
        return db.get_db_items(
            models.BLSession,
            schemas.session.dict_schema,
            schemas.session.ma_schema,
            query_params,
        )
    else:
        return create_response_item(msg=msg)


def add_session(data_dict):
    """
    Adds new session.

    Args:
        session_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    return db.add_db_item(models.BLSession, schemas.session.ma_schema, data_dict)


def get_session_by_id(session_id):
    """
    Returns session info by its sessionId.

    Args:
        session_id (int): corresponds to sessionId in db

    Returns:
        dict: info about session as dict
    """
    data_dict = {"sessionId": session_id}
    return db.get_db_item_by_params(
        models.BLSession, schemas.session.ma_schema, data_dict
    )


def get_session_info_by_id(session_id):
    """
    Returns session info by its sessionId.

    Args:
        session_id (int): corresponds to sessionId in db

    Returns:
        dict: info about session as dict
    """
    session_json = get_session_by_id(session_id)
    if session_json:
        session_json["local_contact"] = session.get_session_by_id(
            session_json["sessionId"]
        )
        session_json["beamline_setup"] = beamline_setup.get_beamline_setup_by_id(
            session_json["beamLineSetupId"]
        )
        # session_json["data_collections_groups"] = data_collection.
        # get_data_collection_groups({"sessionId" : session_id})["data"]["rows"]

    return session_json


def get_sessions_by_date(start_date=None, end_date=None, beamline=None):
    """
    Returns list of sessions by start_date, end_date and beamline.

    Args:
        start_date (datetime, optional): start date. Defaults to None.
        end_date (datetime, optional): end date. Defaults to None.
        beamline (str, optional): beamline name. Defaults to None.

    Returns:
        list: list of session dicts
    """
    query = models.BLSession.query
    if start_date:
        query = query.filter(models.BLSession.startDate >= start_date)
    if end_date:
        query = query.filter(models.BLSession.endDate <= end_date)
    if beamline:
        query = query.filter(models.BLSession.beamLineName == beamline)
    return schemas.session.ma_schema.dump(query, many=True)


def update_session(session_id, data_dict):
    """
    Updates session.

    Args:
        session_id ([type]): [description]
        session_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    id_dict = {"sessionId": session_id}
    return db.update_db_item(
        models.BLSession, schemas.session.ma_schema, id_dict, data_dict
    )


def patch_session(session_id, data_dict):
    """
    Patch a session.

    Args:
        session_id ([type]): [description]
        data_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    id_dict = {"sessionId": session_id}
    return db.patch_db_item(
        models.BLSession, schemas.session.ma_schema, id_dict, data_dict
    )


def delete_session(session_id):
    """
    Deletes session item from db.

    Args:
        session_id (int): sessionId column in db

    Returns:
        bool: True if the session exists and deleted successfully,
        otherwise return False
    """
    id_dict = {"sessionId": session_id}
    return db.delete_db_item(models.BLSession, id_dict)


def get_beam_calendars(request):
    """
    Returns beam_calendar items based on query parameters.

    Args:
        query_params (dict): [description]

    Returns:
        [type]: [description]
    """
    query_params = request.args.to_dict()

    return db.get_db_items(
        models.BeamCalendar,
        schemas.beam_calendar.dict_schema,
        schemas.beam_calendar.ma_schema,
        query_params,
    )


def add_beam_calendar(data_dict):
    """
    Adds data collection item.

    Args:
        beam_calendar_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    return db.add_db_item(
        models.BeamCalendar, schemas.beam_calendar.ma_schema, data_dict
    )


def get_beam_calendar_by_id(beam_calendar_id):
    """
    Returns beam_calendar by its beam_calendarId.

    Args:
        beam_calendar_id (int): corresponds to beamlineSetupId in db

    Returns:
        dict: info about beam_calendar as dict
    """
    data_dict = {"beamCalendarId": beam_calendar_id}
    return db.get_db_item_by_params(
        models.BeamCalendar, schemas.beam_calendar.ma_schema, data_dict
    )


def update_beam_calendar(beam_calendar_id, data_dict):
    """
    Updates beam_calendar.

    Args:
        beam_calendar_id ([type]): [description]
        beam_calendar_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    id_dict = {"beamCalendarId": beam_calendar_id}
    return db.update_db_item(
        models.BeamCalendar, schemas.beam_calendar.ma_schema, id_dict, data_dict
    )


def patch_beam_calendar(beam_calendar_id, data_dict):
    """
    Patch a beam_calendar.

    Args:
        beam_calendar_id ([type]): [description]
        data_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    id_dict = {"beamCalendarId": beam_calendar_id}
    return db.patch_db_item(
        models.BeamCalendar, schemas.beam_calendar.ma_schema, id_dict, data_dict
    )


def delete_beam_calendar(beam_calendar_id):
    """
    Deletes beam_calendar item from db.

    Args:
        beam_calendar_id (int): beam_calendarId column in db

    Returns:
        bool: True if the beam_calendar exists and deleted successfully,
        otherwise return False
    """
    id_dict = {"beamCalendarId": beam_calendar_id}
    return db.delete_db_item(models.BeamCalendar, id_dict)
