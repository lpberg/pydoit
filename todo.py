from datetime import datetime, timedelta
import json
import uuid

class TodoItem:
	def __init__(self, data):
		self.duration_table = {
			"minute": 60,
			"hourly": 3600,
			"daily": 86400,
			"weekly": 604800,
			"monthly":2628000,
			"quarterly": 2628000*3,
			"biannually":2628000*6,
			"annually":2628000*12
		}
		self.id = data["id"]
		self.name = data["name"]
		self.last = datetime.strptime(data["last"],'%Y-%m-%d %H:%M:%S')
		self.frequency = data["frequency"]
		self.frequency_seconds = timedelta(seconds = int(self.duration_table[self.frequency]))
		self.next = self.last + self.frequency_seconds

	def getProgress(self):
		total = (self.next - self.last).total_seconds()
		elapsed = (datetime.now() - self.last).total_seconds()
		self.seconds_remaining = total - elapsed
		pct =  int(round((elapsed / total) * 100, 0))
		pct = max(0, min(pct, 100))
		return pct

	def updateLast(self):
		self.last = datetime.now()
		self.next = self.last + self.frequency_seconds

	def getData(self, ui=True):
		json = {}
		json["id"] = str(self.id)
		json["name"] = self.name
		json["last"] = self.last.strftime("%Y-%m-%d %H:%M:%S")
		json["frequency"] = self.frequency
		if ui:
			json["last"] = self.last
			json["next"] = self.next
			json["progress"] = self.getProgress()
			json["seconds_remaining"] = self.seconds_remaining
		return(json)

class TodoList:
	def __init__(self, file):
		self.file = file
		with open(self.file,"r") as file:
			self.data = json.load(file)
		self.items = {}
		for item in self.data:
			if "id" not in item:
				item["id"] = uuid.uuid4()
			self.items[item["id"]] = TodoItem(item)
		self.writeToFile()

	def getItems(self):
		data = {}
		for idx, obj in self.items.items():
			data[idx] = obj.getData()
		return data

	def update(self, item_id):
		self.items[item_id].updateLast()
		self.writeToFile()

	def writeToFile(self):
		with open(self.file, "w") as json_file:
			items = []
			for idx, item in self.items.items():
				items.append(item.getData(ui=False))
			json.dump(items, json_file, indent=4)
