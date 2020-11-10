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


from tests.core import data


def test_person(ispyb_core_app, ispyb_core_token):
    client = ispyb_core_app.test_client()
    headers = {
        "Authorization": "Bearer " + ispyb_core_token
    }
    route = ispyb_core_app.config["API_ROOT"] + "/contacts/persons"
    response = client.post(route, json=data.get_test_person(), headers=headers)

    assert response.status_code == 200, "Wrong status code"

    resp_data = response.json
    lab_id = resp_data["laboratoryId"]
    assert lab_id

    response = client.get(route, headers=headers)
    assert response.status_code == 200, "Wrong status code"

    route = ispyb_core_app.config["API_ROOT"] + "/contacts/persons/" + str(lab_id)
    mod_laboratory = {
        "familyName": "Other name"
    }
    response = client.patch(route, json=mod_laboratory, headers=headers)

    assert response.status_code == 200, "Wrong status code"
    response = client.delete(route, headers=headers)

    assert response.status_code == 200, "Wrong status code"
    
    route = ispyb_core_app.config["API_ROOT"] + "/contacts/persons"
    response = client.post(route, json=data.get_test_person(), headers=headers)