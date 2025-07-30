import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Label
} from "recharts";

//import data fetching service and interfaces
import { fetchTimeSeriesData, type TimeSeriesDataPoint } from "../../services/apiService";

type TimeSeriesChartProps = {
  // Add props here later, e.g., data, selectedTurbine, etc.
  turbineId?: string;
  startDate?: string;
  endDate?: string;
};

const TimeSeriesChart = ({ turbineId, startDate, endDate }: TimeSeriesChartProps) => {
  const [data, setData] = useState<TimeSeriesDataPoint[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const fetchedData = await fetchTimeSeriesData({
          turbine_id: turbineId,
          start_date: startDate,
          end_date: endDate,
          // limit: 1000 // Adjust limit as needed
        });
        setData(fetchedData);
      } catch (error) {
        console.error("Failed to fetch time series data:", error);
      }
    };
    load();
  }, [turbineId, startDate, endDate]);

  // get statistical summaries
  const maxWindSpeed = Math.max(...data.map(d => d.average_wind_speed));
  const maxPower = Math.max(...data.map(d => d.average_power));
  const avgPower = data.reduce((acc, item) => acc + item.average_power, 0) / data.length;
  const avgWindSpeed = data.reduce((acc, item) => acc + item.average_wind_speed, 0) / data.length;


  return (
    <div className="w-full">
      <h2 className="text-xl font-semibold mb-4">Power Curve Summary</h2>
      <p className="text-sm text-gray-600">
        Power Generation for {turbineId}
      </p>
      <p className="text-sm text-gray-600">
        {/* Date Range Info */}
        {startDate && endDate && (
          <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
            <div>Selected range: {Math.ceil((new Date(endDate).getTime() - new Date(startDate).getTime()) / (1000 * 3600 * 24))} days</div>
            <div> Timeframe |  {new Date(startDate).toLocaleDateString()} - {new Date(endDate).toLocaleDateString()} </div>
          </div>

        )}

      </p>
      {/* Statistics */}

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg Power</div>
          <div className="text-lg font-semibold">{avgPower.toFixed(0)} kW</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Max Power</div>
          <div className="text-lg font-semibold">{maxPower.toFixed(0)} kW</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg Wind Speed</div>
          <div className="text-lg font-semibold">{avgWindSpeed.toFixed(1)} m/s</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Data Points</div>
          <div className="text-lg font-semibold">{data.length.toLocaleString()}</div>
        </div>
      </div>
      <br />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg Azimuth</div>
          <div className="text-lg font-semibold">{avgPower.toFixed(0)} kW</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg External Temp</div>
          <div className="text-lg font-semibold">{maxPower.toFixed(0)} kW</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg Internal Temp</div>
          <div className="text-lg font-semibold">{avgWindSpeed.toFixed(1)} m/s</div>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="text-sm text-gray-600">Avg Rotor Speed</div>
          <div className="text-lg font-semibold">{data.length.toLocaleString()}</div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 50 }}>
          <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="average_wind_speed"
            domain={[0, 20]}
            label={{ value: 'Average Wind Speed (m/s)', offset: - 5, position: 'insideBottom' }}
          />

          <YAxis
            type="number"
            dataKey="average_power"
            domain={[0, maxPower]}

            label={{ value: 'Average Power output (kW)', angle: -90, offset: -5, position: 'insideLeft' }}
          />

          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="average_power" stroke="#8884d8" name="Power Output" />

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TimeSeriesChart;