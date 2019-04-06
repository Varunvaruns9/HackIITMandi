from .models import User


def stable_match():

	class Organ:

		def __init__(self, obj):
			self.pk = str(obj.pk) + str(obj.lol)
			self.donor = obj.first_name
			self.type = obj.lol
			self.bloodgroup = obj.bloodgroup
			self.rh = obj.rh
			self.allocated = 0


	class Patient:

		def __init__(self, obj):
			self.id = obj.id
			self.name = obj.first_name
			self.ailments = obj.ailments
			self.age = obj.age
			self.bloodgroup = obj.bloodgroup
			self.rh = obj.rh
			self.requirements = []
			self.requested = obj.organs
			for requirement in obj.organs:
				if requirement:
					self.requirements.append(donor_map[requirement])
			self.allocated = []

		def stat(self):
			if self.ailments == True:
				return "Ineligible"
			elif not self.allocated:
				return "In Wait-List"
			else:
				allocated_list = []
				for i in self.allocated:
					allocated_list.append(str(donors[i].donor) + " (" + str(donors[i].type) + ") ")
				return allocated_list

		def amend(self, req):
			donors[req].allocated = self.name
			self.allocated.append(req)

		def allot(self):
			status = -1
			flag = 0
			bloodgroup = self.bloodgroup
			rh = self.rh
			for req in self.requirements:
				if donors[req].allocated != 0:
					continue
				for i in self.allocated:
					if donors[i].type == donors[req].type:
						flag = -1
						break
				if flag == -1:
					continue
				donor_group = donors[req].bloodgroup
				donor_factor = donors[req].rh
				if bloodgroup == "O":
					if rh == "-":
						if donor_group == "O" and donor_factor == "-":
							self.amend(req)
							status = req
					elif donor_group == "O":
						self.amend(req)
						status = req
				elif bloodgroup == "A":
					if rh == "-":
						if (donor_group == "A" or donor_group == "O") and donor_factor == "-":
							self.amend(req)
							status = req
					elif donor_group == "O" or donor_group == "A":
						self.amend(req)
						status = req
				elif self.bloodgroup == "B":
					if rh == "-":
						if (donor_group == "B" or donor_group == "O") and donor_factor == "-":
							self.amend(req)
							status = req
					elif donor_group == "B" or donor_group == "O":
						self.amend(req)
						status = req
				else:
					if rh == "-":
						if donor_factor == "-":
							self.amend(req)
							status = req
					else:
						self.amend(req)
						status = req

			if status != -1:
				self.requirements = self.requirements[0:self.requirements.index(status)]
			return status

	donors = []
	patients = []
	num_organs = 0
	donor_map = {}
	ineligible_patients = []
	final_list = []
	final_donor_list = []

	for row in User.objects.all():
		if row.donor == True:
			for entry in row.organs:
				a = row
				a.lol = entry
				allocated_organ = Organ(a)
				donors.append(allocated_organ)
				donor_map[allocated_organ.type] = allocated_organ.pk
				num_organs = num_organs + 1
		else:
			new_patient = Patient(row)
			if new_patient.ailments == False:
				patients.append(new_patient)
			else:
				ineligible_patients.append(new_patient)

	to_delete = []
	temp_patients = patients[:]
	assigned = len(patients)

	while len(temp_patients) != 0 and assigned != 0:
		assigned = 0
		for i, current_patient in enumerate(temp_patients):
			current_allotment = current_patient.allocated
			organ_alloted = current_patient.allot()
			if not current_patient.requirements:
				assigned = assigned + 1
				to_delete.append(i)
			elif organ_alloted != -1:
				if organ_alloted not in current_allotment:
					assigned = assigned + 1
		to_delete = to_delete[::-1]
		for i in to_delete:
			temp_patients.pop(i)
		del to_delete[:]

	patients.extend(ineligible_patients)
	patients = list(sorted(patients, key=lambda x: (x.id, x.name.lower())))

	for current_patient in patients:
		final_list.append([current_patient.id, current_patient.name, current_patient.requested, current_patient.final_status()])
	for current_donor in donors:
		final_donor_list.append([current_donor.type, current_donor.allocated])

	return final_list, final_donor_list
