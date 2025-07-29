type TimeseriesChartProps = {
  // Add props here later, e.g., data, selectedTurbine, etc.
};

function TimeseriesChart({ }: TimeseriesChartProps) {
  return (
    <div className="bg-white shadow-md rounded-xl p-4 w-full h-full">
      <h2 className="text-xl font-semibold mb-4">Power Generation Over Wind Speed chart</h2>
      {/* Chart will go here */}
      <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500">
        [Chart Placeholder]
      </div>
    </div>
  );
}

export default TimeseriesChart;