import matplotlib.pyplot as plt


def get_number_of_flights_to_finish_order_plot(order_to_paths, max_flight_capacity):

    n_flights = [
        order_to_trips.get_total_flights(max_flight_capacity)
        for order, order_to_trips in order_to_paths.items()
    ]

    fig, ax = plt.subplots()

    ax.hist(n_flights, bins=range(min(n_flights), max(n_flights) + 1, 1))

    ax.set_xlabel("Number of flights to finish order")
    ax.set_ylabel("Frequency")
    ax.set_title("Flights for orders")
    ax.grid(True)

    return fig, ax