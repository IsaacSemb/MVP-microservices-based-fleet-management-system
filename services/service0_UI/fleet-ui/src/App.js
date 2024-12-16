import React from "react";

// react-router-dom necessities
import {
  Route, //  a single route to a component created
  BrowserRouter, // the whole browser router that moves btn the pages
  Routes, // engulfs all the routes that have the route tag
} from "react-router-dom"; // the router dom helps with the tools for navifgating around pages

// css to be used
import "./styles/main.css";

// components to be used
import Homepage from "./components/home/HomePage";
import HomepageDashBoard from "./components/home/HomepageDashboard";

import DriverPage from "./components/drivers/DriverPage";
import DriverDetailPage from "./components/drivers/DriverDetails";

import Vehicles from "./components/vehicles/vehicle";
import VehicleDetailPage from "./components/vehicles/VehicleDetailPage";

import MaintenanceLogs from "./components/maintenance/MaintenanceLogs";
import MaintenanceLogDetail from "./components/maintenance/MaintenanceLogDetail";

import Tracking from "./components/vehicle_tracking_page/Tracking";






function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* the landing page for when app starts */}


          {/* TESTING PURPOSES */}


          {/* END OF TESTS */}





          <Route path="/" element={<HomepageDashBoard />} />
          <Route path="/home" element={<Homepage />} />

          {/* the page that displays all drivers */}
          <Route path="/drivers" element={<DriverPage />} />

          {/* the page that displays single driver details and other information */}
          <Route path="/drivers/:id" element={<DriverDetailPage />} />

          {/* the page that displays all vehicles */}
          <Route path="/vehicles" element={<Vehicles />} />

          {/* the page that displays single vehicles details and other information */}
          <Route path="/vehicles/:id" element={<VehicleDetailPage />} />

          {/* the page that displays all maintenance-logs */}
          <Route path="/maintenance-logs" element={<MaintenanceLogs />} />

          {/* the page that displays single maintenance-log details and other information */}
          <Route
            path="/maintenance-log/:id"
            element={<MaintenanceLogDetail />}
          />

          {/* the page that displays all drivers */}
          <Route path="/vehicle-tracking" element={<Tracking />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
