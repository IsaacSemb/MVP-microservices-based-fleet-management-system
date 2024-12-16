import React from 'react';

function MaintenanceOverview() {
  const maintenanceData = {
    scheduled: 10,
    overdue: 10,
  };

  const repairData = {
    scheduled: 8,
    overdue: 5,
  };

  const recentActivities = [
    {
      vehicle_liscence: 'ABC123',
      description: 'Engine Maintenance',
      date: '27/12/2024',
      time: '14:00'
    },
    {
      vehicle_liscence: 'DEF456',
      description: 'Tire Replacement',
      date: '26/12/2024',
      time: '10:30'
    },
    {
      vehicle_liscence: 'GHI789',
      description: 'Oil Change',
      date: '25/12/2024',
      time: '09:00'
    }
  ];

  return (
    <div className="bg-white flex flex-col  rounded-lg shadow-md col-span-1 row-start-2 p-4">
      <h2 className="text-lg font-semibold">Maintenance Overview</h2>
      <hr className='mb-2' />

      <div className="flex gap-5 justify-around">
        {/* Maintenance Tab */}
        <div className="flex flex-col w-1/3 bg-gray-100 border border-gray-300 rounded p-2 shadow-sm">
          <h3 className="text-sm font-semibold">Maintenance</h3>



          <div className='flex justify-between'>
            <p className="text-sm">Scheduled: {maintenanceData.scheduled}</p>
            <p className="text-sm">Overdue: {maintenanceData.overdue}</p>
          </div>


        </div>

        {/* Repairs Tab */}
        <div className="flex flex-col w-1/3 bg-gray-100 border border-gray-300 rounded p-2 shadow-sm">
          <h3 className="text-sm font-semibold">Repairs</h3>


          <div className='flex justify-between'>

          <p className="text-sm">Scheduled: {repairData.scheduled}</p>
          <p className="text-sm">Overdue: {repairData.overdue}</p>
          </div>



        </div>
      </div>

      {/* Recent Activities */}
      <div className='pt-2'>
        <h3 className="text-m font-semibold mt-3 mb-1">Recent Activities</h3>
        <table className="border-collapse border border-gray-300 shadow-sm w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 text-sm p-1 text-left">Vehicle Info</th>
              <th className="border border-gray-300 text-sm p-1 text-left">Description</th>
              <th className="border border-gray-300 text-sm p-1 text-left">Date & Time</th>
            </tr>
          </thead>
          <tbody>
            {recentActivities.map((activity, index) => (
              <tr key={index} className={index % 2 === 0 ? "bg-gray-50" : "bg-white"}>
                <td className="border border-gray-300 p-1">
                  <div className="flex flex-col">
                    {activity.vehicle_liscence}
                    {/* <span className="text-xs text-gray-600">{activity.vehicle_liscence}</span> */}
                  </div>
                </td>
                <td className="border border-gray-300 text-sm p-1">{activity.description}</td>
                <td className="border border-gray-300 p-1">
                  <div className="flex flex-col">
                    {activity.date}
                    <span className="text-xs text-gray-600">{activity.time}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


export default MaintenanceOverview;
