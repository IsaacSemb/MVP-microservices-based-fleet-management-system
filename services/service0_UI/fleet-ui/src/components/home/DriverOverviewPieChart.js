import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

// Register the elements you need
ChartJS.register(ArcElement, Tooltip, Legend);

function DriverOverviewPieChart({ dataSummary, colors }) {
  // Dynamically construct labels and data from the dataSummary prop
  const labels = Object.keys(dataSummary || {});
  const dataValues = Object.values(dataSummary || {});

  // Default colors if none are provided
  const defaultColors = ["#28a745", "#ff9800", "#007bff", "#dc3545", "#17a2b8", "#ffc107"];

  const data = {
    labels, // Use the dynamic labels
    datasets: [
      {
        label: "Drivers",
        data: dataValues, // Use the dynamic data values
        backgroundColor: colors || defaultColors.slice(0, labels.length), // Use provided colors or default
        hoverBackgroundColor: colors || defaultColors.slice(0, labels.length), // Match hover colors
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "right", // Position the legend to the right of the chart
        labels: {
          boxWidth: 20, // Size of the box next to each label
          padding: 20, // Spacing between each legend item
        },
      },
    },
    layout: {
      padding: {
        top: 20,
        bottom: 20,
      },
    },
    maintainAspectRatio: false, // Adjust responsiveness
    responsive: true, // Makes the chart responsive
  };

  return (
    <div className="flex items-center w-full h-full">
      <Pie data={data} options={options} />
    </div>
  );
}

export default DriverOverviewPieChart;
