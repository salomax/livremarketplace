
#!/usr/bin/env python
#coding: utf-8
#
# Copyright 2016, Marcos Salomão.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"

class CurrencyProperty(ndb.IntegerProperty):
	"""http://stackoverflow.com/questions/10035133/ndb-decimal-property
	"""

    def _validate(self, value):
        if not isinstance(value, (Decimal, float, str, unicode, int, long)):
            raise TypeError("value can't be converted to a Decimal.")

    def _to_base_type(self, value):
        return int(round(Decimal(value) * 100))

    def _from_base_type(self, value):
        return Decimal(value) / 100
