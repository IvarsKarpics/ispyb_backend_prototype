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


import datetime
import importlib

import jwt
from flask import current_app


class AuthProvider:
    """Allows to authentificate users and create tokens"""

    def __init__(self):
        self.tokens = {}
        self.site_auth = None

    def init_app(self, app):
        module_name = app.config["AUTH_MODULE"]
        class_name = app.config["AUTH_CLASS"]
        cls = getattr(importlib.import_module(module_name), class_name)
        self.site_auth = cls()

        assert app.config["SECRET_KEY"], "SECRET_KEY must be configured!"

    def get_roles(self, user, password):
        return self.site_auth.get_roles(user, password)

    def generate_token(self, username, roles):
        """
        User is authentificated via site specific auth
        """
        if username in self.tokens:
            # Check if the previously generated token is still valid
            try:
                jwt.decode(
                    self.tokens[username],
                    current_app.config["SECRET_KEY"],
                    algorithms=current_app.config["JWT_CODING_ALGORITHM"],
                )
                return self.tokens[username]
            except jwt.ExpiredSignatureError:
                pass

        token = jwt.encode(
            {
                "sub": username,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(minutes=current_app.config["TOKEN_EXP_TIME"]),
            },
            current_app.config["SECRET_KEY"],
            algorithm=current_app.config["JWT_CODING_ALGORITHM"],
        )
        dec_token = token.decode("UTF-8")
        self.tokens[username] = dec_token

        return dec_token
