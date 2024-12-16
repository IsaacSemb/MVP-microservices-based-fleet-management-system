import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DynamicTable from "../home/DynamicTable";

function DriversPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const driverData = location.state?.data;

  const columnOrder = [
    "driver_id",
    "first_name",
    "last_name",
    "license_no",
    "contact_info",
    "sex",
  ];

  

  const handleRowClick = (driver) => {
    navigate(`/drivers/${driver.driver_id}`, { state: { data: driver } });
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Drivers</h1>
      <DynamicTable
        data={driverData || []}
        columnOrder={columnOrder}
        onRowClick={handleRowClick}
      />
    </div>
  );
}

export default DriversPage;
