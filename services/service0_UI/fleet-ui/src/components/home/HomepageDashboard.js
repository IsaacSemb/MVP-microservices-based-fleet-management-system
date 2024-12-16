// importing necessary dependencies
// import { useEffect, useState } from "react";
// import DisplayCard from "./DisplayCard";
import VehicleSummary from "./VehicleSummary";
import DashboardPanels from "./DashboardPanels";
// import Homepage from "./HomePage";


function HomepageDashboard() {
  return (
      <div className="flex flex-col items-center h-[100vh]">
        <VehicleSummary />
        <DashboardPanels />
      </div>
  );
}



export default HomepageDashboard;
