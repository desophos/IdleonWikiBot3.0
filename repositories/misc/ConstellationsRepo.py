from typing import List

from definitions.misc.Constellation import Constellation
from helpers.HelperFunctions import getFromSplitArray
from repositories.master.Repository import Repository
from repositories.misc.MapNameRepo import MapNameRepo


class ConstellationsRepo(Repository[Constellation]):
	"""
	Dependent on: MapNameRepo
	"""

	@classmethod
	def initDependencies(cls):
		MapNameRepo.initialise(cls.codeReader)

	@classmethod
	def getSections(cls) -> List[str]:
		return ["Constellations"]

	@classmethod
	def generateRepo(cls) -> None:
		prefixes = ["A", "B", "C"]
		# StarQuests
		data = getFromSplitArray(cls.getSection())
		fillterCount = 1 # used to handle multiple constellsations with the same name.
		for n, const in enumerate(data):
			if const[0] == '':
				cls.add(f"Filler{fillterCount}", Constellation(
					name = f"Filler",
					area = "",
					x = 0,
					y = 0,
					num1 = 0,
					num2 = 0,
					num3 = 0,
					starChartPoints = 0,
					requirement = "",
					type = 0,
				))
				fillterCount += 1
				continue
			
			# If map id < 50, it's world 1
			if int(const[0]) < 50:
				prefix = "A"
				number = 1 + n
			# If map id > 50 but < 100, world 2
			elif int(const[0]) < 100:
				prefix = "B"
				number = 1 + n - 12
			# else world 3
			else:
				prefix = "C"
				number = 1 + n - 23
			mapName = MapNameRepo.get(int(const[0])).name
			constName = f"{prefix}-{number}"
			finalData = [constName, mapName, *const[1:]]
			cls.add(constName, Constellation.fromList(finalData))
