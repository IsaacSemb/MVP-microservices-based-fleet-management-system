import { useLocation, /* useNavigate */ } from "react-router-dom";

function DriverDetailPage() {
  const location = useLocation();
  // const navigate = useNavigate();
  const driver = location.state?.data;

  const handleEdit = () => {
    // Logic to edit the driver
    console.log("Editing driver...");
  };

  const handleDelete = () => {
    // Logic to delete the driver
    console.log("Deleting driver...");
  };

  return (
    <div className="driver-detail-page">
      <h1>Driver Details</h1>
      {driver ? (
        <div>
          <p>
            <strong>First Name:</strong> {driver.first_name}
          </p>
          <p>
            <strong>Last Name:</strong> {driver.last_name}
          </p>
          <p>
            <strong>License No:</strong> {driver.license_no}
          </p>
          <p>
            <strong>Contact Info:</strong> {driver.contact_info}
          </p>
          <p>
            <strong>Sex:</strong> {driver.sex}
          </p>

          <div className="driver-actions">
            <button className="btn btn-warning" onClick={handleEdit}>
              Edit Driver
            </button>
            <button className="btn btn-danger" onClick={handleDelete}>
              Delete Driver
            </button>
          </div>
        </div>
      ) : (
        <p>No details available for this driver.</p>
      )}
    </div>
  );
}

export default DriverDetailPage;
