import React from "react";

function DynamicTable({ data, columnOrder, onRowClick }) {
  if (!data || data.length === 0) {
    return <div className="text-gray-500 text-lg">No Data Available</div>;
  }

  const columns = Array.from(new Set(data.flatMap((row) => Object.keys(row))));

  const orderedColumns = [
    ...columnOrder,
    ...columns.filter((col) => !columnOrder.includes(col)),
  ];

  return (
    <table className="table-auto w-4/5 border-collapse border border-black">
      <thead>
        <tr>
          {orderedColumns.map((col) => (
            <th
              key={col}
              className="bg-gray-600 text-white border border-black px-4 py-2"
            >
              {col.replace(/_/g, " ").toUpperCase()}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr
            key={index}
            onClick={() => onRowClick && onRowClick(row)}
            className={`${
              index % 2 === 0 ? "bg-gray-100" : "bg-gray-200"
            } hover:bg-blue-200 cursor-pointer`}
          >
            {orderedColumns.map((col) => (
              <td
                key={col}
                className="border border-black px-4 py-2 text-left"
              >
                {row[col] || "n/a"}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default DynamicTable;
