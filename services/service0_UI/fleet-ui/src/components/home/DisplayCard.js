// this navigates between pages
import { useNavigate } from "react-router-dom";

// axios is used for making http requests
import axios from "axios";

// we need the driver url
import "../../config.js";
import config from "../../config.js";

function DisplayCard(props) {
  // Create navigate function to navigate to different cases
  const navigate = useNavigate();

  // Handler for button click
  async function handleClick() {
    // create empty fetched data variable
    let fetchedData = null;

    // creating a switch statement to handle every case uniquely
    switch (props.title.toLowerCase()) {
      // case of tapping the go to drivers page button
      case "drivers":
        console.log("Fetching driver data...");

        // get driver details
        fetchedData = await fetchDrivers();
        break;

      // case of tapping the go to vehicles page button
      case "vehicles":
        console.log("Fetching vehicle data...");

        // get vehicle details
        fetchedData = await fetchVehicles();
        break;

      case "assignments":
        console.log("Fetching assignments...");

        // get all assignments
        fetchedData = await fetchAssignmentLogs();
        break;

      case "maintenance":
        console.log("Fetching maintenance logs...");

        // get all maintenance logs
        fetchedData = await fetchMaintanenceLogs();
        break;

      case "schedules":
        console.log("Fetching schedules...");

        // get all maintenance logs
        fetchedData = await fetchScheduleLog();
        break;

      default:
        console.log("Button clicked");
    }

    // finishing fetching data... take the user to the page to see the results
    if (fetchedData) {
      // Navigate to the page and pass the fetched data
      navigate(props.page, { state: { data: fetchedData } });
    } else {
      // tracking error handling for now
      navigate(props.page);
    }
  }

  // the case fucntions
  const fetchDrivers = async () => {
    console.log("carrying out the fetchdrivers logic");

    // use axios to make a call to the back end
    console.log(config.DRIVER_SERVICE_URL);
    const serverResponse = await axios.get(
      `${config.DRIVER_SERVICE_URL}/drivers`
    );

    // log only the data and see your things
    console.log(serverResponse.data);
    return serverResponse.data;
  };

  const fetchVehicles = async () => {
    console.log("carrying out the fetch vehicles logic");
    // use axios to make a call to the back end
    const serverResponse = await axios.get(
      `${config.VEHICLE_SERVICE_URL}/vehicles`
    );

    // log only the data and see your things
    console.log(serverResponse.data);
    return serverResponse.data; // Return fetched data
  };

  const fetchMaintanenceLogs = async () => {
    console.log("carrying out the fetch vehicles logic");
    // use axios to make a call to the back end
    const serverResponse = await axios.get(
      `${config.MAINTENANCE_URL}/maintenance`
    );

    // log only the data and see your things
    console.log(serverResponse.data);
    return serverResponse.data; // Return fetched data
  };

  const fetchAssignmentLogs = async () => {
    console.log("carrying out the fetch vehicles logic");
    // use axios to make a call to the back end
    const serverResponse = await axios.get(
      `${config.ASSIGNMENT_SERVICE_URL}/assignments`
    );

    // log only the data and see your things
    console.log(serverResponse.data);
    return serverResponse.data; // Return fetched data
  };

  const fetchScheduleLog = async () => {
    console.log("carrying out the fetch vehicles logic");
    // use axios to make a call to the back end
    const serverResponse = await axios.get(
      `${config.SCHEDULE_SERVICE_URL}/schedules`
    );

    // log only the data and see your things
    console.log(serverResponse.data);
    return serverResponse.data; // Return fetched data
  };

  return (
    <div className="flex flex-col justify-between border border-gray-200 shadow-md rounded-lg bg-white">
      <div className="text-center bg-gray-100 py-2">{props.title}</div>
      <div className="p-2  flex flex-col">
        <h5 className="text-lg font-semibold">{props.subtitle}</h5>
        <p className="text-gray-600">{props.description}</p>
        
      </div>
      <button
          className={`px-4 py-2 text-white self-start mb-4 ml-4  bg-blue-500 rounded-md ${
            props.isDisabled ? "opacity-50 cursor-not-allowed" : ""
          }`}
          onClick={handleClick}
        >
          Go to page
        </button>
    </div>
  );
}

export default DisplayCard;
