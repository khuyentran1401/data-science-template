"""Python script to run the notebook"""

from config import Location
from prefect import flow
from prefect_jupyter import notebook


@flow
def run_notebook(location: Location = Location()):
    """Run a notebook with specified parameters then
    generate a notebook with the outputs

    Parameters
    ----------
    location : Location, optional
        Locations of inputs and outputs, by default Location()
    """
    nb = notebook.execute_notebook(
        location.input_notebook,
        parameters={
            "data_process": location.data_process,
            "data_final": location.data_final,
        },
    )
    body = notebook.export_notebook(nb)
    with open(location.output_notebook, "w") as f:
        f.write(body)


if __name__ == "__main__":
    run_notebook()
