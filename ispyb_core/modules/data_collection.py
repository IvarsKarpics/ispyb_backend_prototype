# encoding: utf-8
#
#  Project: py-ispyb
#  https://github.com/ispyb/py-ispyb
#
#  This file is part of py-ispyb software.
#
#  py-ispyb is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  py-ispyb is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.


__license__ = "LGPLv3+"


import logging

from app.extensions import get_db_items, get_db_item_by_id, add_db_item

from ispyb_core.models import DataCollection as DataCollectionModel
from ispyb_core.models import DataCollectionGroup as DataCollectionGroupModel
from ispyb_core.schemas.data_collection import (
    data_collection_ma_schema,
    data_collection_dict_schema,
)
from ispyb_core.schemas.data_collection_group import (
    data_collection_group_ma_schema,
    data_collection_group_dict_schema,
)


log = logging.getLogger(__name__)


def get_data_collections(query_params):
    """Returns data collection items based on query parameters

    Args:
        query_params ([type]): [description]

    Returns:
        [type]: [description]
    """
    return get_db_items(
        DataCollectionModel,
        data_collection_dict_schema,
        data_collection_ma_schema,
        query_params,
    )


def add_data_collection(data_collection_dict):
    """Adds data collection item

    Args:
        data_collection_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    return add_db_item(DataCollectionModel, data_collection_dict)

def get_data_collection_by_id(data_collection_id):
    """Returns data_collection by its data_collectionId

    Args:
        data_collection_id (int): corresponds to dataCollectionId in db

    Returns:
        dict: info about data_collection as dict
    """
    data_collection = DataCollectionModel.query.filter_by(dataCollectionId=data_collection_id).first()
    data_collection_json = data_collection_ma_schema.dump(data_collection)[0]

    return data_collection_json

def get_data_collection_groups(query_params):
    """Returns data collection group items based on query parameters

    Args:
        query_params ([type]): [description]

    Returns:
        [type]: [description]
    """
    return get_resource(
        DataCollectionGroupModel,
        data_collection_group_dict_schema,
        data_collection_group_ma_schema,
        query_params,
    )


def add_data_collection_group(data_collection_group_dict):
    """Adds data collection item

    Args:
        data_collection_dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    return add_resource(DataCollectionGroupModel, data_collection_group_dict)
