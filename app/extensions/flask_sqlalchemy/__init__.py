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


import sys
import sqlite3

from flask import current_app
from sqlalchemy import engine
from sqlalchemy.exc import InvalidRequestError
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy

from app.utils import create_response_item


def set_sqlite_pragma(dbapi_connection, connection_record):
    # pylint: disable=unused-argument
    """
    SQLite supports FOREIGN KEY syntax when emitting CREATE statements for tables.

    By default these constraints have no effect on the
    operation of the table.

    http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#foreign-key-support

    Args:
        dbapi_connection ([type]): [description]
        connection_record ([type]): [description]
    """
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class AlembicDatabaseMigrationConfig:
    """
    Helper config holder that provides missing functions of Flask-Alembic.

    Args:
        object ([type]): [description]
    """

    def __init__(self, database, directory="migrations", **kwargs):
        self.db = database  # pylint: disable=invalid-name
        self.directory = directory
        self.configure_args = kwargs


class SQLAlchemy(BaseSQLAlchemy):
    """
    Customized Flask-SQLAlchemy adapter

    Args:
        BaseSQLAlchemy ([type]): [description]
    """

    def __init__(self, *args, **kwargs):
        """
        Init method
        """

        if "session_options" not in kwargs:
            kwargs["session_options"] = {}
        kwargs["session_options"]["autocommit"] = False
        # Configure Constraint Naming Conventions:
        # http://docs.sqlalchemy.org/en/latest/core/constraints.html
        # #constraint-naming-conventions
        """
        kwargs["metadata"] = MetaData(
            naming_convention={
                "pk": "pk_%(table_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "ix": "ix_%(table_name)s_%(column_0_name)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
            }
        )
        """
        super().__init__(*args, **kwargs)

    def init_app(self, app):
        """
        Called to init extension.

        Args:
            app ([type]): [description]
        """
        super().init_app(app)

        database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_uri or database_uri == "sqlite:///:memory:":
            raise Exception("SQLALCHEMY_DATABASE_URI must be configured!")
        # assert database_uri, "SQLALCHEMY_DATABASE_URI must be configured!"
        if database_uri.startswith("sqlite:"):
            self.event.listens_for(engine.Engine, "connect")(set_sqlite_pragma)

        app.extensions["migrate"] = AlembicDatabaseMigrationConfig(
            self, compare_type=True
        )

    def get_db_items(self, sql_alchemy_model, dict_schema, ma_schema, query_params):
        """
        Returns resource based on the passed models and query parameter

        Args:
            sql_alchemy_model ([type]): SQLAlchemy ORM model
            dict_schema ([type]): dict with flask fields
            ma_schema ([type]): marshmallows schema
            query_params (dict): query parameters

        Returns:
            dict: {"data": {"total": int, "rows": list},
                    "message" : str,
                    "error": str
                    }
        """
        offset = 0
        limit = current_app.config.get("PAGINATION_ITEMS_LIMIT")
        info_msg = None
        error_msg = None

        if "offset" in query_params.keys():
            offset = query_params.get("offset")
        if "limit" in query_params.keys():
            limit = query_params.get("limit")

        query = sql_alchemy_model.query
        total = query.count()

        # Filter items based on schema keys
        schema_keys = {}
        for key in query_params.keys():
            if key in dict_schema.keys():
                schema_keys[key] = query_params.get(key)

        if schema_keys:
            try:
                query = query.filter_by(**schema_keys)
            except InvalidRequestError as ex:
                print(ex)
                error_msg = "Unable to filter items based on query items (%s)" % str(ex)

        query = query.limit(limit).offset(offset)
        items = ma_schema.dump(query, many=True)[0]

        response_dict = create_response_item(info_msg, error_msg, total, items)

        return response_dict

    def get_db_item_by_params(self, sql_alchemy_model, ma_schema, item_id_dict):
        """
        Returns data base item by its Id.

        Args:
            item_id (int):

        Returns:
            dict: info dict
        """
        db_item = sql_alchemy_model.query.filter_by(**item_id_dict).first()
        db_item_json = ma_schema.dump(db_item)[0]

        return db_item_json

    def add_db_item(self, sql_alchemy_model, ma_schema, data):
        """
        Adds item to db.

        Args:
            sql_alchemy_model ([type]): [description]
            data (dict): [description]

        Returns:
            SQLAlchemy db item: [description]
        """
        db_item_json = None
        try:
            db_item = sql_alchemy_model(**data)
            self.session.add(db_item)
            self.session.commit()
            db_item_json = ma_schema.dump(db_item)[0]
        except Exception as ex:
            print(ex)
            # app.logger.exception(str(ex))
            self.session.rollback()
        return db_item_json
            

    def update_db_item(self, sql_alchemy_model, item_id_dict, item_update_dict):
        """
        Updates item in db

        Args:
            sql_alchemy_model ([type]): [description]
            item_id_dict ([type]): [description]
            item_update_dict ([type]): [description]

        Returns:
            [type]: [description]
        """
        result = None
        db_item = sql_alchemy_model.query.filter_by(**item_id_dict).first()
        if db_item:
            print(item_update_dict)
            result = True

        return result

    def patch_db_item(self, sql_alchemy_model, item_id_dict, item_update_dict):
        """
        Patch db item

        Args:
            sql_alchemy_model ([type]): [description]
            item_id_dict ([type]): [description]
            item_update_dict ([type]): [description]

        Returns:
            [type]: [description]
        """
        result = None
        db_item = sql_alchemy_model.query.filter_by(**item_id_dict).first()
        if db_item:
            for key, value in item_update_dict.items():
                if hasattr(db_item, key):
                    setattr(db_item, key, value)
                else:
                    print("Attribute %s not defined in the item model" % key)
            self.session.commit()
            result = True

        return result

    def delete_db_item(self, sql_alchemy_model, item_id_dict):
        """
        Deletes db item

        Args:
            sql_alchemy_model ([type]): [description]
            item_id_dict ([type]): [description]

        Returns:
            [type]: [description]
        """
        db_item = sql_alchemy_model.query.filter_by(**item_id_dict).first()
        if not db_item:
            return None
        else:
            try:
                self.session.delete(db_item)
                self.session.commit()
                return True
            except BaseException as ex:
                print(ex)
                # log.exception(str(ex))
                self.session.rollback()
