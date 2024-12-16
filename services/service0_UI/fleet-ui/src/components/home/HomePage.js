// importing necessary dependencies
import { useEffect, useState } from "react";
import DisplayCard from "./DisplayCard";

// mimicking incoming data
const description_data = [
  {
    id: "1",
    title: "Drivers",
    subtitles: "Drivers details",
    description: "this will display all drivers",
    page: "/drivers",
  },
  {
    id: "2",
    title: "Vehicles",
    subtitles: "Vehicles Details",
    description: "a display of all vehicles",
    page: "/vehicles",
  },
  {
    id: "3",
    title: "Vehicle Tracking",
    subtitles: "Tracking locations of the vehicles",
    description: "live tracking of vehicles",
    page: "/vehicle-tracking",
  },
  {
    id: "4",
    title: "Assignments",
    subtitles: "Driver to Vehicle Assignments",
    description: "managing assignments between drivers and vehicles",
    page: "/assignments",
  },
  {
    id: "5",
    title: "Maintenance",
    subtitles: "Vehicle Maintenance Records",
    description: "overview of all scheduled and completed maintenance",
    page: "/maintenance-logs",
  },
  {
    id: "6",
    title: "Schedules",
    subtitles: "Schedules",
    description:
      "management of schedules for vehicle maintenance and assignments",
    page: "/schedules",
  },
];

function Homepage() {
  const [information, setInformation] = useState([]);

  useEffect(() => {
    setInformation(description_data);
  }, []);

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <div className="grid grid-cols-3 grid-rows-2 gap-4 p-4 w-[80%]">
        {information.map((data) => (
          <DisplayCard
            key={data.id}
            title={data.title}
            subtitle={data.subtitles}
            description={data.description}
            page={data.page}
            isDisabled={data.title.toLowerCase() === "vehicle tracking"}
          />
        ))}
      </div>
    </div>
  );
}


export default Homepage;
