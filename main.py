from sustainability.reports import Emissions


def add_data():

    emissions = Emissions()
    carbon_data = emissions.get_carbon(start_year=2023, end_year=2027)
    emissions.data_transform(data=carbon_data)


if __name__ == "__main__":

	add_data()
