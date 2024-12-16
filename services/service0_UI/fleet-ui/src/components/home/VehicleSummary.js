// Parent Component: VehicleSummary.js
import React, { useEffect, useState } from "react";
import VehicleCard from "./VehicleCard";
import config from "../../config";
import axios from "axios";

const VehicleSummary = () => {
  // state for vehicle data
  const [vehicleData, setVehicleData] = useState([]);

  // state for loading
  const [loading, setLoading] = useState(true);

  // incase of errors
  const [error, setError] = useState(null);

  // Data for the display cards
  // const vehicleData1 = [
  //   { type: "Total Vehicles", number: 50, available: 30, service: 5 },
  //   { type: "Cars", number: 8, available: 3, service: 0 },
  //   { type: "Vans", number: 8, available: 3, service: 0 },
  //   { type: "Buses", number: 8, available: 3, service: 0 },
  //   { type: "Trucks", number: 8, available: 3, service: 0 },
  // ];

  const fetchVehicles = async () => {
    // trying to fetch data from the back end
    try {
      console.log("fetching vehicle data ...");

      // use axios to make a call to the back end
      const serverResponse = await axios.get(
        `${config.VEHICLE_SERVICE_URL}/vehicles?response_type=summary`
      );

      // destructure the summary out of the data
      const { summary } = serverResponse.data;

      console.log(serverResponse.data);
      console.log(summary);

      // manipulate it to your liking
      const mappedData = Object.entries(summary.total_by_type)
        .map(([type, counts]) => ({
          type: type,
          number: counts.available + counts.unavailable,
          available: counts.available,
          service: counts.unavailable,
        }))
        .sort((a, b) =>
          a.type === "total_vehicles" ? -1 : b.type === "total_vehicles" ? 1 : 0
        );

      console.log(mappedData);

      setVehicleData(mappedData);

      // log only the data and see your things
      // console.log(serverResponse.data);
      return serverResponse.data.summary; // Return fetched data
    } catch (error) {
      console.error("Error fetching vehicle data", error);
      setError("Failed to load vehicle data");
    } finally {
      setLoading(false);
    }
  };

  // on component mounting, we fetch the data
  useEffect(() => {
    fetchVehicles();
  }, []);

  // if still loading
  if (loading) {
    return <div>Loading...</div>;
  }

  // incase of any errors
  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="flex gap-4 w-[95%] max-w-[1500px] p-4">
      {vehicleData.map((vehicle, index) => (
        <VehicleCard
          key={index}
          type={vehicle.type}
          number={vehicle.number}
          available={vehicle.available}
          service={vehicle.service}
        />
      ))}
    </div>
  );
};

export default VehicleSummary;
