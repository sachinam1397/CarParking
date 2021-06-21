import re

class parking_lot:
    __instance = None
    vehicle_instance_mapping = dict()                 # car_instance mapped with vehicle number
    total_slots = 0                                   # total slot available in parking slot
    closest_available_slot = 0 
    occupied = list()                                 # boolean list of occupied slots
    vehicle_regex = "^[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}$" # regex to validate vehicle number

    def __init__(self,total_slots):
        # Only one instance of parking lot is allowed
        if parking_lot.__instance != None:
            print("Multiple parking lot is not valid")
        else:
            if(total_slots < 1):
                print("Parking slots cannot be 0")
                return
            parking_lot.__instance = self
            parking_lot.total_slots = total_slots
            parking_lot.closest_available_slot = 1
            parking_lot.occupied = [False for i in range(total_slots+1)]
            print("Created Parking of {} slots".format(total_slots))

    def Park(self,vehicle_number,driver_age):
        # Parking full
        if(parking_lot.closest_available_slot > parking_lot.total_slots):
            print("Sorry no slot available.")
            return
        # Vehicle Number is not valid
        if(re.search(parking_lot.vehicle_regex,vehicle_number) == None):
            print("Invalid Vehicle Number. Please recheck the number.")
            return
        car_instance = car_details(
            vehicle_number,
            driver_age,
            parking_lot.closest_available_slot
            )
        parking_lot.vehicle_instance_mapping[vehicle_number] = car_instance;
        parking_lot.occupied[parking_lot.closest_available_slot] = True
        print("Car with vehicle registration number \"{}\" has been parked at slot number \"{}\"".format(vehicle_number,parking_lot.closest_available_slot))
        # Find next closest available slot 
        for slot_index,is_occupied in enumerate(parking_lot.occupied):
            if(is_occupied or slot_index == 0):
                parking_lot.closest_available_slot += 1
                continue
            parking_lot.closest_available_slot = slot_index
            break;
        
        return

    def Leave(self,slot_number):
        # Vacant Slot
        if(not parking_lot.occupied[slot_number]):
            print("Slot Number is already vacant.")
            return
        parking_lot.occupied[slot_number] = False
        car_instance = None
        # Deleting Car instance from Vehicle Slot mapping
        for key,value in parking_lot.vehicle_instance_mapping.items():
            if(value.slot_number == slot_number):
                car_instance = value
                del parking_lot.vehicle_instance_mapping[key]
                break
        print("Slot number {} vacated, the car with vehicle registration number \"{}\" left the space, the driver of the car was of age {}".format(slot_number,car_instance.vehicle_number,car_instance.driver_age))
        if(parking_lot.closest_available_slot > slot_number):
            parking_lot.closest_available_slot = slot_number
        return

    def Slot_number_for_car_with_number(self,vehicle_number):
        # Vehicle Number is not valid
        if(re.search(parking_lot.vehicle_regex,vehicle_number) == None):
            print("Invalid vehicle number. Please recheck")
            return
        if(parking_lot.vehicle_instance_mapping[vehicle_number] is None):
            print("The car with vehicle number {} is not in the parking area".format(vehicle_number))
            return
        print(parking_lot.vehicle_instance_mapping[vehicle_number].slot_number)
        return

    def list_of_values(self,driver_age):
        # Age cannot be negative
        if(driver_age < 1):
            print("Age cannot be negative or zero")
        list_of_values = []
        for key, value in parking_lot.vehicle_instance_mapping:
            if(value.driver_age == driver_age):
                list_of_values.append(str(value.vehicle_number))
        if(len(list_of_values) == 0):
            print("No such driver with matching age have parked the car.")
        print(",".join(list_of_values))

    def Slot_numbers_for_driver_of_age(self,driver_age):
        # Age cannot be negative
        if(driver_age < 1):
            print("Age cannot be negative or zero")
        list_of_slots = []
        for key, value in parking_lot.vehicle_instance_mapping.items():
            if(value.driver_age == driver_age):
                list_of_slots.append(str(value.slot_number))
        if(len(list_of_slots) == 0):
            print("")
            return
        print(",".join(list_of_slots))

    def Vehicle_registration_number_for_driver_of_age(self,driver_age):
        # Age cannot be negative
        if(driver_age < 1):
            print("Age cannot be negative or zero")
        list_of_vehicle_numbers = []
        for key, value in parking_lot.vehicle_instance_mapping.items():
            if(value.driver_age == driver_age):
                list_of_vehicle_numbers.append(str(value.vehicle_number))
        if(len(list_of_vehicle_numbers) == 0):
            print("")
            return
        print(",".join(list_of_vehicle_numbers))
    


class car_details:
    def __init__(self,vehicle_number,driver_age,slot_number):
        self.slot_number = int(slot_number)
        self.vehicle_number = vehicle_number
        self.driver_age = int(driver_age)


if __name__ == "__main__":
    input_file = open('input.txt', 'r')
    Lines = input_file.readlines()
    parking_lot_instance = None
    for line in Lines:
        parking_input = line.strip().split(" ")
        if(parking_lot_instance == None and parking_input[0] != "Create_parking_lot"):
            print("No parking lot is created till now.")
            continue;
        if(parking_input[0] == 'Create_parking_lot'):
            try:
                parking_lot_instance = parking_lot(int(parking_input[1]))
            except Exception as error:
                print("[ ERROR ] " + str(error))
            continue
        try:
            parking_action = getattr(parking_lot_instance,parking_input[0])
        except Exception as error:
            print("[ ERROR ] " + str(error))
        try:
            if(len(parking_input) == 4):
                parking_action(
                    int(parking_input[1]) if parking_input[1].isdigit() else parking_input[1],
                    int(parking_input[3]) if parking_input[3].isdigit() else parking_input[3])
            elif(len(parking_input) == 2):
                parking_action(int(parking_input[1]) if parking_input[1].isdigit() else parking_input[1])
            else:
                print("Wrong Input")
        except Exception as error:
            print("[ ERROR ] " + str(error))