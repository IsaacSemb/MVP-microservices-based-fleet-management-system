import { useParams, useLocation, /* useNavigate */ } from "react-router-dom";

// URL   ----- > /maintenance-logs/:id


function MaintenanceLogDetail() {
  const { id } = useParams(); // Get the vehicle ID from the URL
  const location = useLocation();
  // const navigate = useNavigate();
  const maintenanceLog = location.state?.data;

  const handleEdit = () => {
    // Logic to edit the vehicle
    console.log("Editing vehicle...");
  };

  const handleDelete = () => {
    // Logic to delete the vehicle
    console.log("Deleting vehicle...");
  };

  return (
    <div className="maintenance-log-detail-page">
      <h1>Maintenance Log Details</h1>
      {maintenanceLog ? (
        <div>
          <p><strong> maintenance id: </strong>{maintenanceLog.maintenance_id}</p>
          <p><strong> maintenance type: </strong>{maintenanceLog.maintenance_type}</p>
          <p><strong> vehicle id: </strong>{maintenanceLog.vehicle_id}</p>
          <p><strong> start date: </strong>{maintenanceLog.start_date}</p>
          <p><strong> expected completion: </strong>{maintenanceLog.expected_completion}</p>
          <p><strong> end date: </strong>{maintenanceLog.end_date}</p>
          <p><strong> description: </strong>{maintenanceLog.description}</p>
          <p><strong> cost: </strong>{maintenanceLog.cost}</p>
          <p><strong> parts used: </strong>{maintenanceLog.parts_used}</p>
          <p><strong> status: </strong>{maintenanceLog.status}</p>

          <div className="maintenance-log-actions">
            <button className="btn btn-warning" onClick={handleEdit}>
              Edit log
            </button>
            <button className="btn btn-danger" onClick={handleDelete}>
              Delete log
            </button>
          </div>
        </div>
      ) : (
        <p>Loading log for maintenance log ID: {id}...</p>
      )}
    </div>
  );
}

export default MaintenanceLogDetail;
