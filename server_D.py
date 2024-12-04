import zmq


class HydrationCalculator:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://0.0.0.0:4444")  # Bind to port 4444
        self.unit_conversion = {
            1: 1.0,       # Ounces (default)
            2: 33.814,    # Liters to Ounces
            3: 8.0        # Cups to Ounces
        }

    def calculate_total(self, records, target_unit="oz"):
        """
        Calculate total hydration in the requested unit using the provided records.
        """
        total_oz = sum(record['Amount'] * self.unit_conversion.get(record['Unit'], 1.0) for record in records)

        # Convert total to target unit
        if target_unit == "L":
            return total_oz / 33.814
        elif target_unit == "cups":
            return total_oz / 8
        else:  # Default to ounces
            return total_oz

    def format_records(self, records):
        """Formats the hydration records by converting numeric unit codes to proper unit names."""
        unit_map = {1: "oz", 2: "L", 3: "cups"}  # Mapping unit codes to names

        formatted_records = []
        for record in records:
            # Map the unit code to a human-readable unit name
            unit_code = record.get("Unit")
            formatted_record = {
                "Timestamp": record.get("Timestamp"),
                "Amount": record.get("Amount"),
                "Unit": unit_map.get(unit_code, "Unknown")  # Default to 'Unknown' if unit code is not recognized
            }
            formatted_records.append(formatted_record)

        return formatted_records

    def handle_request(self, request):
        """Handle incoming requests."""
        try:
            action = request.get("action")
            if action == "calculate":
                # Calculate total hydration with provided records
                records = request.get("data", [])
                unit = request.get("unit")
                total = self.calculate_total(records, unit)
                return {"status": "success", "total": total}
            elif action == "get_records":
                # Format records and send them back
                records = request.get("data", [])
                formatted_records = self.format_records(records)
                return {"status": "success", "records": formatted_records}
            else:
                return {"status": "error", "message": "Unknown action"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run(self):
        """
        Start the server loop.
        """
        print(">>> Microservice D (CALCULATOR) Server running...")
        while True:
            # Receive JSON request
            message = self.socket.recv_json()
            print(f" D Request Received: {message}")

            # Process request and send response
            response = self.handle_request(message)
            self.socket.send_json(response)


if __name__ == "__main__":
    calculator = HydrationCalculator()
    calculator.run()
    #MICROSERVICE D
