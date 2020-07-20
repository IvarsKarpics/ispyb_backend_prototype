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


from ispyb_core.models import ImageQualityIndicator as ImageQualityIndicatorsModel
from ispyb_core.schemas.image_quality_indicators import (
    image_quality_indicators_f_schema,
    image_quality_indicators_ma_schema,
)


def get_image_quality_indicators_list():
    image_quality_indicators_list = ImageQualityIndicatorsModel.query.all()
    return image_quality_indicators_ma_schema.dump(image_quality_indicators_list)
