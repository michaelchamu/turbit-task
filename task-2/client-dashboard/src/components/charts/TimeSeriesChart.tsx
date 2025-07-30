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
  const maxWindSpeed = Math.max(...data.map(d => d.average_wind_speed));
  const maxPower = Math.max(...data.map(d => d.average_power));

  return (
    <div className="w-full">
      <h2 className="text-xl font-semibold mb-4">Power vs Wind Speed</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 50 }}>
          <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
          <XAxis dataKey="average_wind_speed" type="number" domain={[0, maxWindSpeed]}>
            <Label value="Wind Speed (m/s)" offset={0} position="insideBottom" />
          </XAxis>
          <YAxis dataKey="average_power" type="number" domain={[0, maxPower]}>
            <Label value="Power kW" offset={0} position="left" />
          </YAxis>
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="average_power" stroke="#8884d8" name="Power Output" />

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TimeSeriesChart;