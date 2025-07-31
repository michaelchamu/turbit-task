import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";
import { MdOutlineWindPower, MdBolt } from "react-icons/md"
//import data fetching service and interfaces
import { fetchTimeSeriesData, type TimeSeriesDataPoint } from "../../services/apiService";
import { FaWind } from "react-icons/fa";
import { SiProtractor } from "react-icons/si";
import { LiaTemperatureHighSolid } from "react-icons/lia";

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
  const locationNames = ['Bremen', 'Oldenburg', 'Hamburg', 'Bochum', 'Borkum'] // pick a random location name where the turbine is located
  const avgAzimuth = data.reduce((acc, item) => acc + item.average_azimuth, 0) / data.length;
  const avgExternalTemperature = data.reduce((acc, item) => acc + item.average_external_temperature, 0) / data.length;
  const avgInternalTemperature = data.reduce((acc, item) => acc + item.average_internal_temperature, 0) / data.length;
  const avgRPM = data.reduce((acc, item) => acc + item.average_rpm, 0) / data.length;
  const locationIndex = Math.floor(Math.random() * 4);
  const isOnline = Math.random() < 0.5;


  return (
    <div className="w-full">
      <h2 className="text-xl font-semibold mb-4 flex items-center justify-between">
        { /*this section is pseudo-dynamic. I use a random number generator 
        to select a location from the locationNames array then I use another random generator 
        to give an online status. 
         */}
        <span>
          Power Curve Summary for {turbineId} Located at {locationNames[locationIndex]}
        </span>
        <span className="flex items-center gap-1">
          <span
            className={`w-2.5 h-2.5 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}
            title={isOnline ? 'Turbine Online' : 'Turbine Offline'}
          />
          <span className={`text-sm ${isOnline ? 'text-green-600' : 'text-red-600'}`}>
            ({isOnline ? 'online' : 'offline'})
          </span>
        </span>
      </h2>

      <div className="text-sm text-gray-600">
        {/* Date Range Info */}
        {startDate && endDate && (
          <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
            <div>Selected range: {Math.ceil((new Date(endDate).getTime() - new Date(startDate).getTime()) / (1000 * 3600 * 24))} days,&nbsp;

              {new Date(startDate).toLocaleDateString("en-US",
                {
                  month: "short",
                  day: "numeric",
                  year: "numeric"
                })} -

              {new Date(endDate).toLocaleDateString("en-US",
                {
                  month: "short",
                  day: "numeric",
                  year: "numeric"
                })}
            </div>
          </div>

        )}

      </div>
      {/* Statistics */}

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">

        <div className="bg-yellow-100 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-yellow-100 text-yellow-600 rounded-full p-2">
            <MdBolt className="w-5 h-5" />
          </div>
          <div>
            <div className="text-sm text-gray-600">Avg Power</div>
            <div className="text-lg font-semibold text-gray-800">
              {avgPower.toFixed(0)} kW
            </div>
          </div>
        </div>

        <div className="bg-zinc-300 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-zinc-300 text-yellow-600 rounded-full p-2">
            <MdBolt className="w-5 h-5" />
          </div>
          <div className="text-sm text-black-600">Max Power</div>
          <div className="text-lg font-semibold text-gray-800">
            {maxPower.toFixed(0)} kW
          </div>
        </div>

        <div className="bg-blue-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-blue-200 text-blue-600 rounded-full p-2">
            <FaWind className="w-5 h-5" />
          </div>
          <div className="text-sm text-gray-600">Avg Wind Speed</div>
          <div className="text-lg font-semibold">{avgWindSpeed.toFixed(1)} m/s</div>
        </div>
        <div className="bg-blue-300 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="text-sm text-gray-600">Max Wind Speed</div>
          <div className="text-lg font-semibold">{maxWindSpeed.toFixed(0)} m/s</div>
        </div>
      </div>
      <br />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-green-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-green-200 text-green-600 rounded-full p-2">
            <SiProtractor className="w-5 h-5" />
          </div>
          <div className="text-sm text-gray-600">Avg Azimuth</div>
          <div className="text-lg font-semibold">{avgAzimuth.toFixed(0)} &deg;</div>
        </div>
        <div className="bg-red-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-red-200 text-red-600 rounded-full p-2">
            < LiaTemperatureHighSolid className="w-5 h-5" />
          </div>
          <div className="text-sm text-gray-600">Avg External Temp</div>
          <div className="text-lg font-semibold">{avgExternalTemperature.toFixed(1)} &deg; C</div>
        </div>
        <div className="bg-cyan-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-cyan-200 text-cyan-600 rounded-full p-2">
            < LiaTemperatureHighSolid className="w-5 h-5" />
          </div>
          <div className="text-sm text-gray-600">Avg Internal Temp</div>
          <div className="text-lg font-semibold">{avgInternalTemperature.toFixed(1)} &deg; C</div>
        </div>
        <div className="bg-purple-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
          <div className="bg-purple-200 text-purple-600 rounded-full p-2">
            <MdOutlineWindPower className="w-5 h-5" />
          </div>
          <div className="text-sm text-gray-600">Avg Rotor Speed</div>
          <div className="text-lg font-semibold">{avgRPM.toFixed(1)} rpm</div>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={550}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 50 }}>
          <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="average_wind_speed"
            domain={[0, 21]}
            tickCount={10}
            label={{ value: 'Average Wind Speed (m/s)', offset: - 5, position: 'insideBottom' }}
          />

          <YAxis
            type="number"
            dataKey="average_power"
            domain={[0, Math.ceil(maxPower / 100) * 100]}
            label={{ value: 'Average Power output (kW)', angle: -90, offset: -5, position: 'insideLeft', style: { textAnchor: 'middle' } }}
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