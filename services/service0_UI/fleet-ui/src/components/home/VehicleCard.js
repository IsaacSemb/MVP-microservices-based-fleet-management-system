// Child Component: VehicleCard.js
import React from "react";

const VehicleCard = ({ type, number, available, service }) => {
  return (
    <div className="vehicle-card border border-gray-300 rounded-lg p-4 bg-white shadow-md hover:transform hover:-translate-y-1 hover:shadow-lg transition-transform duration-200 ease-in-out w-[20%] min-w-[200px] ">
      <div className="mb-2">
        <h4 className="font-semibold text-lg">
          {type} :{" "}
          <span className="text-[1.5rem] font-semibold text-blue-500">
            {number}
          </span>
        </h4>
        <hr />

        <div className="text-[1.1rem] text-gray-700 my-2 "></div>
      </div>

      <div className="text-sm mt-2">
        <div className="flex gap-4 justify-around items-center font-semibold">
          <p>
            Available:{" "}
            <span className="text-green-500 text-lg font-bold">{available}</span>{" "}
          </p>

          <p>
            Unavailable: <span className="text-red-500 text-lg font-bold">{service}</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default VehicleCard;
