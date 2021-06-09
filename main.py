import csv
import sys


class Main():
    facilities = {}
    covenants = {}

    def solution(self):
        self.read_facilities()
        self.read_covenants()
        self.assign_loans()

    def read_facilities(self):
        with open('small/facilities.csv', newline='') as csvfile:
            facilities_reader = csv.DictReader(csvfile)
            for row in facilities_reader:
                if row["bank_id"] not in self.facilities:
                    self.facilities[row["bank_id"]] = []
                self.facilities[(row["bank_id"], row["id"])] = {
                    'amount': row["amount"],
                    'interest_rate': row["interest_rate"]
                }

    def read_covenants(self):
        with open('small/covenants.csv', newline='') as csvfile:
            covenants_reader = csv.DictReader(csvfile)
            for row in covenants_reader:
                if not row["facility_id"]:
                    row["facility_id"] = "ALL"
                if row["bank_id"] not in self.covenants:
                    self.covenants[row["bank_id"]] = []
                self.covenants[row["bank_id"]].append({'facility_id': row["facility_id"],  # Can be None
                                                       'max_default_likelihood': row["max_default_likelihood"],
                                                       # Can be None
                                                       'banned_state': row["banned_state"].upper()  # Can be None
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
                    loan_state = loan_state.upper()
                    if (default_max_likelihood >= default_likelihood or not default_max_likelihood):
                        banks.add((bank_id, facility['facility_id']))
        return banks


    def get_cheapest_facility(self, banks, amount, default_likelihood, loan_interest_rate):
        lowest_interest_rate = float("inf")
        cheapeast_facility_yield = sys.maxsize

        for bank_id, facility_id in banks:
            facility = self.facilities[(bank_id, facility_id)]
            facility_amount = float(facility["amount"])
            facility_interest_rate = float(facility["interest_rate"])
            #facility["id"] == facility_id or facility_id == "ALL")
            if  facility_amount >= amount and facility_interest_rate < lowest_interest_rate:
                lowest_interest_rate = facility_interest_rate
                cheapeast_facility_yield = (1 - default_likelihood) * loan_interest_rate * amount \
                            - default_likelihood * amount \
                            - facility_interest_rate * amount
                facility["amount"] = float(facility["amount"]) - amount

        print((facility_id, bank_id, cheapeast_facility_yield))
        return (facility_id, bank_id, cheapeast_facility_yield)

    def assign_loans(self):
        with open('small/loans.csv', newline='') as csvfile:
            loan_reader = csv.DictReader(csvfile)
            for row in loan_reader:
                banks = self.get_covenant_matching_facilities(row["default_likelihood"], row["state"])
                self.get_cheapest_facility(banks, float(row["amount"]), float(row["default_likelihood"]),
                                           float(row["interest_rate"]))
            # interest_rate,amount,id,default_likelihood,state


if __name__ == '__main__':
    main = Main()
    main.solution()
