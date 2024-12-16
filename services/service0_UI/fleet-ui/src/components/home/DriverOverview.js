import React, { useEffect, useState } from "react";
import DriverOverviewPieChart from "./DriverOverviewPieChart";

function DriverOverview() {
  const [driverSummary, setDriverSummary] = useState({
    available: 0,
    assigned: 0,
    enroute: 0, // Map this to active from the API
    unavailable: 0,
  });

  const fetchDriverSummary = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_DRIVER_SERVICE_URL}/drivers?response_type=summary`
      );
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      const { status_summary } = data.summary;

      setDriverSummary({
        available: status_summary.available || 0,
        assigned: status_summary.assigned || 0,
        enroute: status_summary.active || 0, // Active status maps to enroute
        unavailable: status_summary.unavailable || 0,
      });
    } catch (error) {
      console.error("Failed to fetch driver summary:", error);
    }
  };

  useEffect(() => {
    fetchDriverSummary();
  }, []); // Fetch once on component mount

  return (
    <div
      id="driver-overview"
      className="m-0 w-full h-full bg-white p-4 rounded-lg shadow-md col-span-1 row-start-1"
    >
      <div className="mb-2">
        <h3 className="text-lg font-semibold">Driver Overview</h3>
        <hr className="border-none h-px bg-gray-400 my-2" />
      </div>

      <div className="flex">
        <div className="flex-1">
          <div className="mb-4">
            <p className="text-lg text-green-500">
              Available : <span>{driverSummary.available}</span>
            </p>
            <p className="text-lg text-orange-500">
              Assigned : <span>{driverSummary.assigned}</span>
            </p>
            <p className="text-lg text-blue-500">
              Enroute : <span>{driverSummary.enroute}</span>
            </p>
            <p className="text-lg text-red-500">
              Unavailable : <span>{driverSummary.unavailable}</span>
            </p>
          </div>

          <div>
            <h4 className="mt-2 mb-2">Top performers this week</h4>
            <hr className="border-none h-px bg-gray-400 my-2" />
            <p className="text-base">1. Isaac Semb</p>
            <p className="text-base">2. Sarper Uzun</p>
            <p className="text-base">3. Nicho Mpanga</p>
          </div>
        </div>

        <div className="flex justify-center items-center flex-1">
          

          <DriverOverviewPieChart
            dataSummary={driverSummary}
            colors={["#28a745", "#ff9800", "#007bff", "#dc3545"]}
          />


        </div>
      </div>
    </div>
  );
}

export default DriverOverview;
