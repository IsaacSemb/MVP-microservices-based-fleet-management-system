import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DynamicTable from "../home/DynamicTable";

function Vehicles() {
  // Access the passed state using useLocation
  const location = useLocation();
  const vehicleData = location.state?.data?.details;

  console.log('####');
  console.log(vehicleData.details);
  
  

  // function to help us jump pages
  const navigate = useNavigate();

  // function for when some one click on a row
  const handleRowClick = (vehicle) => {
    // Navigate to the driver detail page, using the driver_id as the parameter
    navigate(`/vehicles/${vehicle.vehicle_id}`, { state: { data: vehicle } });
  };

  const columnOrder = [
    'vehicle_id',
    'reg_no',
    'model',
    'make',
    'vehicle_type',
    'fuel_type',
    'status'
  ];



  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Drivers</h1>
      <DynamicTable
        data={vehicleData || []}
        columnOrder={columnOrder}
        onRowClick={handleRowClick}
      />
    </div>
  );
}

export default Vehicles;
