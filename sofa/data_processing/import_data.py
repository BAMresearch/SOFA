"""
This file is part of SOFA.
SOFA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SOFA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SOFA.  If not, see <http://www.gnu.org/licenses/>.
"""
from typing import Dict

import data_processing.named_tuples as nt
from data_processing.import_formats.import_ibw_data import import_ibw_data

def import_data(
	importParameter: nt.ImportParameter,
) -> Dict:
	"""
	Import data in the selected file format.

	Parameters
	----------
	importParameter : nt.ImportParameter
		Contains format of the measurement data, the 
		path to the measurement data and if selected 
		the paths to additional image or channel files. 

	Returns
	-------
	importedData : dict
		Combined data of all the imported data files.
	"""
	importedData = importFunctions[importParameter.dataFormat][0](importParameter)

	return importedData
	

# Defines all available import options.
importFunctions = {
	".ibw": (import_ibw_data, "*.ibw"),
}