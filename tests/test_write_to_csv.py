from dronedelivery.output_handlers.write_to_csv import WriteToCSV
from tests.fixtures import fixture, nonsense_drone_schedule_configuration
import os


@fixture
def write_to_csv():
    return WriteToCSV()


def test_get_list_of_command_string_representation(
    write_to_csv, nonsense_drone_schedule_configuration
):
    list_of_command_string_representations = (
        write_to_csv._get_list_of_command_string_representations(
            drone_schedule_configuration=nonsense_drone_schedule_configuration
        )
    )

    assert len(list_of_command_string_representations) > 1
    assert isinstance(list_of_command_string_representations[0], str)

    test_location_to_save_csv = "tests/test_toy_drone_schedule_configuration.csv"

    write_to_csv.run(
        nonsense_drone_schedule_configuration, output_file=test_location_to_save_csv
    )

    assert os.path.isfile(test_location_to_save_csv) is True

    os.remove(test_location_to_save_csv)
