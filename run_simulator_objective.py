from dronedelivery.simulator import Simulator
import pickle


def main():

    (full_problem, drone_schedule) = pickle.load(open("test.pkl", "rb"))

    simulator = Simulator(problem=full_problem)
    objective = simulator.get_objective(drone_schedule)

    print(f"The objective for this drone schedule in {objective}")


if __name__ == "__main__":
    main()