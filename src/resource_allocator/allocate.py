from dataclasses import dataclass

@dataclass
class Customer():
    base: float
    grow: float
    shrink: float

@dataclass
class CustomerToResources:
    index: int
    allocated_compute_units: float
    customer_init_details: Customer

class CustomerAllocations:
    def __init__(self, compute_units: float, customers: list[Customer]):
        self.__grow_sum = 0
        self.__shrink_sum = 0
        self.__compute_units = compute_units
        self.__remaining_compute_units = compute_units
        self.__customers = customers
        self.__customer_to_resources: dict[int, CustomerToResources] = {}
        self.__initialize_customer_to_resources()



    def __initialize_customer_to_resources(self):
        for index, customer in enumerate(self.__customers):
            self.__customer_to_resources[index] = CustomerToResources(index, customer.base, customer)
            self.__remaining_compute_units -= customer.base
            self.__grow_sum += customer.grow
            self.__shrink_sum += customer.shrink

    def __relocate_excess_compute_units(self, compute_units: float):
        for customer in self.__customer_to_resources.values():
            customer.allocated_compute_units += (compute_units *
                                                 self.__get_customer_grow_factor(customer.customer_init_details))
        self.__remaining_compute_units = 0

    def __relocate_missing_compute_units(self, compute_units: float):
        shrink_sum_to_reduce = 0
        for customer in self.__customer_to_resources.values():
            if customer.allocated_compute_units == 0:
                continue

            shrink_amount = compute_units * self.__get_customer_shrink_factor(customer.customer_init_details)

            if shrink_amount > customer.allocated_compute_units:
                self.__remaining_compute_units += customer.allocated_compute_units
                customer.allocated_compute_units = 0
                shrink_sum_to_reduce += customer.customer_init_details.shrink
            else:
                self.__remaining_compute_units += shrink_amount
                customer.allocated_compute_units -= shrink_amount

        self.__shrink_sum -= shrink_sum_to_reduce

    def __get_customer_grow_factor(self, customer: Customer) -> float:
        return customer.grow / self.__grow_sum

    def __get_customer_shrink_factor(self, customer: Customer) -> float:
        return customer.shrink / self.__shrink_sum

    def allocate(self) -> list[float]:
        while self.__remaining_compute_units != 0.0:
            if self.__remaining_compute_units > 0.0:
                self.__relocate_excess_compute_units(self.__remaining_compute_units)
            elif self.__remaining_compute_units < 0.0:
                self.__relocate_missing_compute_units(abs(self.__remaining_compute_units))

        return [customer.allocated_compute_units for customer in self.__customer_to_resources.values()]

    def show_allocations(self):
        print(self.__customer_to_resources)


def allocate(compute_units: float, customers: list[Customer]) -> list[float]:
    customer_allocations = CustomerAllocations(compute_units, customers)
    customer_allocations.show_allocations()
    return customer_allocations.allocate()


def main():
    customers = [
        Customer(10, 1, 1),
        Customer(10, 1, 1)
    ]
    print(allocate(23, customers))


if __name__ == "__main__":
    main()
