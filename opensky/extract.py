class FlightExtractor:
    def __init__(self, client, airport):
        self.client = client
        self.airport = airport

    def extract_day(self, begin, end):
        arrivals = self.client.get_arrivals(self.airport, begin, end)
        departures = self.client.get_departure(self.airport, begin, end)
        return {"arrivals": arrivals, "departures": departures}
