import { useParams, useLocation } from "react-router-dom";

function VehicleDetailPage() {
  const { id } = useParams(); // Get the vehicle ID from the URL
  const location = useLocation();
  // const navigate = useNavigate();
  const vehicle = location.state?.data;

  const handleEdit = () => {
    // Logic to edit the vehicle
    console.log("Editing vehicle...");
  };

  const handleDelete = () => {
    // Logic to delete the vehicle
    console.log("Deleting vehicle...");
  };

  return (
    <div className="vehicle-detail-page">
      <h1>Vehicle Details</h1>
      {vehicle ? (
        <div>
          <p>
            <strong>Make:</strong> {vehicle.make}
          </p>
          <p>
            <strong>Model:</strong> {vehicle.model}
          </p>
          <p>
            <strong>Year:</strong> {vehicle.year}
          </p>
          <p>
            <strong>Registration No:</strong> {vehicle.reg_no}
          </p>
          <p>
            <strong>Fuel Type:</strong> {vehicle.fuel_type}
          </p>
          <p>
            <strong>Vehicle Type:</strong> {vehicle.vehicle_type}
          </p>

          <div className="vehicle-actions">
            <button className="btn btn-warning" onClick={handleEdit}>
              Edit Vehicle
            </button>
            <button className="btn btn-danger" onClick={handleDelete}>
              Delete Vehicle
            </button>
          </div>
        </div>
      ) : (
        <p>Loading details for vehicle ID: {id}...</p>
      )}
    </div>
  );
}

export default VehicleDetailPage;
