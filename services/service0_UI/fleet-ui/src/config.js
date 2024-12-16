// the id config file hold my URLs to the different services

const config = {
  DRIVER_SERVICE_URL: process.env.REACT_APP_DRIVER_SERVICE_URL,
  VEHICLE_SERVICE_URL: process.env.REACT_APP_VEHICLE_SERVICE_URL,
  ASSIGNMENT_SERVICE_URL: process.env.REACT_APP_ASSIGNMENT_SERVICE_URL,
  MAINTENANCE_URL: process.env.REACT_APP_MAINTENANCE_URL,
  SCHEDULE_SERVICE_URL: process.env.REACT_APP_SCHEDULE_SERVICE_URL,
  FUEL_SERVICE_URL: process.env.REACT_APP_FUEL_SERVICE_URL,
};

//   export it for use
export default config;
