from datetime import datetime
from random import randint

class Part:
    def __init__(self, model_number, q_in_stock, q_req, unit_price, vendor, last_counted, order_size):
        self.model_number = model_number
        self.q_in_stock = q_in_stock
        self.q_req = q_req
        self.unit_price = unit_price
        self.vendor = vendor
        self.last_counted = last_counted
        self.order_size = order_size
        self.col_w = 20

        self.spacer = "-"
        self.val_spacer = " "
        self.padchar = "\t"
        self.indent = "\t"
        self.cols_per_line = 2

    def get_field(self, name: str, value: str):
        if len(value) > self.col_w:
            print("ERROR! DOES NOT FIT")
        return (name.center(self.col_w, self.spacer), value.center(self.col_w, self.val_spacer))
    
    def __str__(self):
        short_of_req = max(0, self.q_req - self.q_in_stock)
        units_to_order = 0
        while units_to_order < short_of_req:
            units_to_order += self.order_size
        next_order_cost = units_to_order * self.unit_price

        output = f"ITEM {self.model_number}\n"
        fields = []
        fields.append(self.get_field("QUANTITY IN STOCK", str(self.q_in_stock)))
        fields.append(self.get_field("QUANTITY REQUESTED", str(self.q_req)))
        fields.append(self.get_field("UNIT PRICE", str(self.unit_price)))
        fields.append(self.get_field("VENDOR", str(self.vendor)))
        fields.append(self.get_field("LAST INVENTORIED", f"{datetime.fromtimestamp(self.last_counted).strftime('%Y-%m-%d %H:%M')}"))
        fields.append(self.get_field("ORDER SIZE IN UNITS", str(self.order_size)))
        fields.append(self.get_field("QUANTITY SHORT", str(short_of_req)))
        fields.append(self.get_field("QUANTITY TO ORDER", str(units_to_order)))
        fields.append(self.get_field("NEXT ORDER COST", str(next_order_cost)))

        index = 0
        while index < len(fields):
            output += self.indent
            c_index = index
            for _ in range(self.cols_per_line):
                if index >= len(fields):
                    break
                output += fields[index][0]
                output += self.padchar
                index += 1
            index = c_index
            output += "\n"
            output += self.indent
            for _ in range(self.cols_per_line):
                if index >= len(fields):
                    break
                output += fields[index][1]
                output += self.padchar
                index += 1
            output += "\n\n"
        # output += self.indent + "QUANTITY REQUESTED".center(self.col_w, self.spacer) + self.padchar
        return output

parts = [
    Part("WDX50934", 374, 29, 29, "Whirlpool", 1760491976 + randint(0, 604800), 16),
    Part("PRT-109D", 5, 7, 14, "LG", 1760491976 + randint(0, 604800), 30),
    Part("BQ-5543", 1, 2, 85, "Bosch", 1760491976 + randint(0, 604800), 5),
    Part("BQ-5543", 30, 5, 18, "KitchenAid", 1760491976 + randint(0, 604800), 10),
    Part("SGX04QAB", 50, 10, 5, "Samsung", 1760491976 + randint(0, 604800), 100),
]

report_type = "exception"

if report_type == "detail":
    print("--- DETAIL REPORT ---")
    for part in parts:
            print(part)
elif report_type == "exception":
    print("--- PARTS THAT ARE OUT OF STOCK OR HAVE LOWER STOCK THAN REQUESTED BY TECHNICIANS ---")
    for part in parts:
        if part.q_in_stock <= part.q_req:
            print(part)