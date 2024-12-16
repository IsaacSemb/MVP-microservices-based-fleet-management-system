import React from "react";
import MaintenanceOverview from './MaintenanceOverview'
import DriverOverview from "./DriverOverview";
import TripsOverview from "./TripsOverview";
import TrackingTab from "./TrackingTab";



function DashboardPanels() {
  return (
    <div className="w-[90%] h-[80%] grid grid-cols-2 grid-rows-2 gap-2">

        <MaintenanceOverview />
        <DriverOverview />
        <TrackingTab />
        <TripsOverview />

    </div>

  );
}

export default DashboardPanels;
