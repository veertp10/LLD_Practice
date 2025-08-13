from enum import Enum
import heapq

class Direction(Enum):
    UP = 1
    DOWN = 2

class ElevatorState(Enum):
    MOVING = 1
    IDLE = 2

class ElevatorDisplay:
    def __init__(self):
        self.floor = 0
        self.direction = Direction.UP

    def set_display(self, floor, direction):
        self.floor = floor
        self.direction = direction

    def show_display(self):
        print(f"Current Floor: {self.floor}, Direction: {self.direction.name}")

class InternalButtons:
    def __init__(self):
        self.dispatcher = InternalDispatcher()
        self.available_buttons = list(range(1, 11))
        self.button_selected = 0

    def press_button(self, destination, elevator_car):
        if destination in self.available_buttons:
            self.dispatcher.submit_internal_request(destination, elevator_car)
        else:
            print(f"Invalid floor number: {destination}")

class ElevatorCar:
    def __init__(self):
        self.id = 0
        self.display = ElevatorDisplay()
        self.internal_buttons = InternalButtons()
        self.elevator_state = ElevatorState.IDLE
        self.current_floor = 0
        self.elevator_direction = Direction.UP
        self.elevator_door = ElevatorDoor()

    def show_display(self):
        self.display.show_display()

    def press_button(self, destination):
        self.internal_buttons.press_button(destination, self)

    def set_display(self):
        self.display.set_display(self.current_floor, self.elevator_direction)

    def move_elevator(self, direction, destination_floor):
        start_floor = self.current_floor
        self.elevator_direction = direction

        if direction == Direction.UP:
            for i in range(start_floor, destination_floor + 1):
                self.current_floor = i
                self.set_display()
                self.show_display()
                if i == destination_floor:
                    return True
        
        elif direction == Direction.DOWN:
            for i in range(start_floor, destination_floor - 1, -1):
                self.current_floor = i
                self.set_display()
                self.show_display()
                if i == destination_floor:
                    return True
        return False

class ElevatorDoor:
    def __init__(self):
        self.is_open = False
    
    def open_door(self):
        print("Opening door...")
        self.is_open = True
    
    def close_door(self):
        print("Closing door...")
        self.is_open = False

class ElevatorController:
    def __init__(self, elevator_car):
        self.up_min_pq = []
        self.down_max_pq = []
        self.elevator_car = elevator_car

    def submit_external_request(self, floor, direction):
        if direction == Direction.DOWN:
            heapq.heappush(self.down_max_pq, -floor)
        else:
            heapq.heappush(self.up_min_pq, floor)

    def submit_internal_request(self, floor):
        if floor > self.elevator_car.current_floor:
            heapq.heappush(self.up_min_pq, floor)
        elif floor < self.elevator_car.current_floor:
            heapq.heappush(self.down_max_pq, -floor)
        else:
            print("Already on this floor.")

    def control_elevator(self):
        while self.up_min_pq or self.down_max_pq:
            if self.elevator_car.elevator_direction == Direction.UP:
                while self.up_min_pq:
                    next_floor = heapq.heappop(self.up_min_pq)
                    self.elevator_car.move_elevator(Direction.UP, next_floor)
                    self.elevator_car.elevator_door.open_door()
                    self.elevator_car.elevator_door.close_door()
                if self.down_max_pq:
                    self.elevator_car.elevator_direction = Direction.DOWN

            elif self.elevator_car.elevator_direction == Direction.DOWN:
                while self.down_max_pq:
                    next_floor = -heapq.heappop(self.down_max_pq)
                    self.elevator_car.move_elevator(Direction.DOWN, next_floor)
                    self.elevator_car.elevator_door.open_door()
                    self.elevator_car.elevator_door.close_door()
                if self.up_min_pq:
                    self.elevator_car.elevator_direction = Direction.UP

class ExternalDispatcher:
    def __init__(self):
        self.elevator_controller_list = ElevatorCreator.elevator_controller_list

    def submit_external_request(self, floor, direction):
        print(f"External request submitted for floor {floor}, direction {direction.name}")
        for elevator_controller in self.elevator_controller_list:
            elevator_id = elevator_controller.elevator_car.id
            if (elevator_id % 2 == 1 and floor % 2 == 1) or \
               (elevator_id % 2 == 0 and floor % 2 == 0):
                elevator_controller.submit_external_request(floor, direction)
                print(f"Request assigned to Elevator {elevator_id}")
                return

class InternalDispatcher:
    def submit_internal_request(self, destination, elevator_car):
        for controller in ElevatorCreator.elevator_controller_list:
            if controller.elevator_car.id == elevator_car.id:
                controller.submit_internal_request(destination)
                return



class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.external_dispatcher = ExternalDispatcher()

    def press_button(self, direction):
        print(f"Button pressed on floor {self.floor_number} for direction {direction.name}")
        self.external_dispatcher.submit_external_request(self.floor_number, direction)

class Building:
    def __init__(self, floors):
        self.floor_list = floors

    def add_floors(self, new_floor):
        self.floor_list.append(new_floor)

    def remove_floors(self, remove_floor):
        self.floor_list.remove(remove_floor)

    def get_all_floor_list(self):
        return self.floor_list

class ElevatorCreator:
    elevator_controller_list = []

    @staticmethod
    def initialize_elevators():
        elevator_car_1 = ElevatorCar()
        elevator_car_1.id = 1
        controller_1 = ElevatorController(elevator_car_1)

        elevator_car_2 = ElevatorCar()
        elevator_car_2.id = 2
        controller_2 = ElevatorController(elevator_car_2)

        ElevatorCreator.elevator_controller_list.append(controller_1)
        ElevatorCreator.elevator_controller_list.append(controller_2)

# Main execution block
if __name__ == '__main__':
    # Initialize the system
    ElevatorCreator.initialize_elevators()

    # Create floors
    floors = [Floor(i) for i in range(11)]

    # Create building
    building = Building(floors)

    # Example usage
    print("--- User on Floor 3 wants to go UP ---")
    building.get_all_floor_list()[3].press_button(Direction.UP)

    print("\n--- User inside Elevator 1 wants to go to Floor 7 ---")
    elevator1_controller = ElevatorCreator.elevator_controller_list[0]
    elevator1_controller.submit_internal_request(7)

    print("\n--- User on Floor 8 wants to go DOWN ---")
    building.get_all_floor_list()[8].press_button(Direction.DOWN)

    # Simulate elevator operation
    print("\n--- Starting elevator control loop for Elevator 1 ---")
    elevator1_controller.control_elevator()

    print("\n--- Starting elevator control loop for Elevator 2 ---")
    elevator2_controller = ElevatorCreator.elevator_controller_list[1]
    elevator2_controller.control_elevator()
