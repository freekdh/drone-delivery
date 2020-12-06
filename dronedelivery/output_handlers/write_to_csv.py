from .standard_output_handler_interface import OutputHandler


class WriteToCSV(OutputHandler):
    def __init__(self):
        pass

    def run(self, drone_schedule_configuration, output_file):
        list_of_command_string_representations = (
            self._get_list_of_command_string_representations(
                drone_schedule_configuration
            )
        )

        self._write_to_csv(list_of_command_string_representations, output_file)

    def _get_list_of_command_string_representations(self, drone_schedule_configuration):
        list_of_command_string_representations = []
        for drone in drone_schedule_configuration.get_drones():
            for command in drone_schedule_configuration.get_drone_commands(drone):
                list_of_command_string_representations.append(
                    command.get_string_representation()
                )
        return list_of_command_string_representations

    def _write_to_csv(self, data_list, output_file):
        with open(output_file, "w") as write_output:
            for data_element in data_list:
                write_output.write(data_element + "\n")
