import csv


class Main():
    facilities = {}
    covenants = {}

    def solution(self, covenants_file, facilities_file, loans_file):
        self.read_facilities(facilities_file)
        self.read_covenants(covenants_file)
        self.assign_loans(loans_file)

    def read_facilities(self, facilties_file):
        with open(facilties_file, newline='') as csvfile:
            facilities_reader = csv.DictReader(csvfile)
            for row in facilities_reader:
                self.facilities[(row["bank_id"], row["id"])] = {
                    'amount': row["amount"],
                    'interest_rate': row["interest_rate"]
                }

    def read_covenants(self, covenants_file):
        with open(covenants_file, newline='') as csvfile:
            covenants_reader = csv.DictReader(csvfile)
            for row in covenants_reader:
                if not row["facility_id"]:
                    row["facility_id"] = "ALL"
                if row["bank_id"] not in self.covenants:
                    self.covenants[row["bank_id"]] = []
                if row["max_default_likelihood"] is None:
                    row["max_default_likelihood"] = 1
                self.covenants[row["bank_id"]].append({'facility_id': row["facility_id"],  # Can be None
                                                       'max_default_likelihood': row["max_default_likelihood"],
                                                       # Can be None
                                                       'banned_state': row["banned_state"]  # Can be None
                                                       })

    # bank_id , facility_id,max_default_likelihood,banned_state
    def get_covenant_matching_facilities(self, default_likelihood, loan_state):
        banks = set()
        banned = set()
        for bank_id in self.covenants:
            for facility in self.covenants[bank_id]:
                if facility['banned_state'] == loan_state:
                    banned.add((bank_id, facility["facility_id"]))

        for bank_id in self.covenants:
            for facility in self.covenants[bank_id]:
                if (bank_id, facility["facility_id"]) not in banned:
                    default_max_likelihood = facility['max_default_likelihood']
                    if (default_max_likelihood >= default_likelihood or not default_max_likelihood):
                        banks.add((bank_id, facility['facility_id']))

        #print(banks)
        return banks

    def get_cheapest_facility(self, banks, amount, default_likelihood, loan_interest_rate):
        cheapest_interest_rate = float("inf")
        #cheapeast_facility_yield = sys.maxsize
        cheapest_facility = {}
        cheapest_bank_id = None
        cheapest_facility_id = None

        for bank_id, facility_id in banks:
            facility = self.facilities[(bank_id, facility_id)]

            if facility_id == "ALL":
                for facility_tuple in self.facilities:
                    if facility_tuple[0] == bank_id:
                        facility = self.facilities[facility_tuple]
                        facility_amount = float(facility["amount"])
                        facility_interest_rate = float(facility["interest_rate"])
                        # facility["id"] == facility_id or facility_id == "ALL")
                        if facility_amount >= amount and facility_interest_rate < cheapest_interest_rate:
                            cheapest_interest_rate = facility_interest_rate
                            cheapest_facility = facility
                            cheapest_bank_id = bank_id
                            cheapest_facility_id = facility_tuple[1]

            else:
                facility_amount = float(facility["amount"])
                facility_interest_rate = float(facility["interest_rate"])
                if facility_amount >= amount and facility_interest_rate < cheapest_interest_rate:
                    cheapest_interest_rate = facility_interest_rate
                    cheapest_facility = facility
                    cheapest_bank_id = bank_id
                    cheapest_facility_id = facility_id



        if "amount" in cheapest_facility:
            cheapeast_facility_yield = (1 - default_likelihood) * loan_interest_rate * amount \
                                   - default_likelihood * amount \
                                   - cheapest_interest_rate * amount
            cheapest_facility["amount"] = float(cheapest_facility["amount"]) - amount
        else:
            return (None, None, None)




        #print((bank_id, facility_id , cheapeast_facility_yield))
        return (cheapest_bank_id, cheapest_facility_id, cheapeast_facility_yield)

    def assign_loans(self, loans_file):
        with open(loans_file, newline='') as csvfile:
            loan_reader = csv.DictReader(csvfile)
            yields = {}
            assignments = {}
            for row in loan_reader:
                banks = self.get_covenant_matching_facilities(row["default_likelihood"], row["state"])
                bank_id, facility_id, cheapeast_facility_yield = self.get_cheapest_facility(banks, float(row["amount"]), float(row["default_likelihood"]),
                                           float(row["interest_rate"]))
                print (row["id"], bank_id, facility_id, cheapeast_facility_yield)
                if cheapeast_facility_yield is None:
                    continue
                else:
                    if facility_id not in yields:
                        yields[facility_id] = 0.0
                    yields[facility_id] += cheapeast_facility_yield
                    assignments[row["id"]] = facility_id

            with open('output/'+loans_file.split("/")[0] + 'yields.csv', 'w', newline='') as csv_file:
                    fieldnames = ['facility_id', 'expected_yield']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    writer.writeheader()
                    for facility_id, expected_yield in yields.items():
                        writer.writerow({'facility_id': facility_id, 'expected_yield': expected_yield})

            with open('output/'+loans_file.split("/")[0] + 'assignments.csv', 'w', newline='') as csv_file:
                    fieldnames = ['loan_id','facility_id']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    writer.writeheader()
                    for loan_id , facility_id in assignments.items():
                        writer.writerow({'loan_id': loan_id , 'facility_id': facility_id})


if __name__ == '__main__':
    main = Main()
    main.solution("small/covenants.csv","small/facilities.csv","small/loans.csv")
    main.solution("large/covenants.csv", "large/facilities.csv", "large/loans.csv")

