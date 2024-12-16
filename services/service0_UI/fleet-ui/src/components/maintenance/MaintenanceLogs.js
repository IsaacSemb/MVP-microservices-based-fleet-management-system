import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DynamicTable from "../home/DynamicTable";
// URL   ----- > /maintenance-logs

function MaintenanceLogs() {
  // Access the passed state using useLocation
  const location = useLocation();
  const maintenanceLogData = location.state?.data;

  // function to help us jump pages
  const navigate = useNavigate();

  // function for when some one click on a row
  const handleRowClick = (maintenanceLog) => {
    console.log(maintenanceLog.maintenance_id);
    // Navigate to the driver detail page, using the driver_id as the parameter
    navigate(`/maintenance-log/${maintenanceLog.maintenance_id}`, {
      state: { data: maintenanceLog },
    });
  };
  const columnOrder = [
    "maintenance_id",
    "vehicle_id",
    "maintenance_type",
    "start_date_time",
    "expected_completion_date_time",
    "end_date_time",
    "description",
    "cost",
    "parts_used",
    "status",
  ];

  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Maintenance</h1>
      <DynamicTable
        data={maintenanceLogData || []}
        columnOrder={columnOrder}
        onRowClick={handleRowClick}
      />
    </div>
  );
}

export default MaintenanceLogs;
