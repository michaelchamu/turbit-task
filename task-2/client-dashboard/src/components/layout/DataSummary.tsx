import { FaWind } from "react-icons/fa";
import { SiProtractor } from "react-icons/si";
import { LiaTemperatureHighSolid } from "react-icons/lia";
import { IoMdSpeedometer } from "react-icons/io";
import { MdOutlineWindPower, MdBolt } from "react-icons/md"

export const DataSummary = ({ data }: any) => {


    const validWindSpeeds = data
        .map((d: { average_wind_speed: any; }) => d.average_wind_speed)
        .filter((p: unknown) => Number.isFinite(p));
    const maxWindSpeed = validWindSpeeds.length > 0 ? Math.max(...validWindSpeeds) : 0;

    const validPowers = data
        .map((d: { average_power: any; }) => d.average_power)
        .filter((p: unknown) => Number.isFinite(p));
    const maxPower = validPowers.length > 0 ? Math.max(...validPowers) : 0;

    const avgPower = data.reduce((acc: any, item: { average_power: any; }) => acc + item.average_power, 0) / data.length;
    const avgWindSpeed = data.reduce((acc: any, item: { average_wind_speed: any; }) => acc + item.average_wind_speed, 0) / data.length;
    const avgAzimuth = data.reduce((acc: any, item: { average_azimuth: any; }) => acc + item.average_azimuth, 0) / data.length;
    const avgExternalTemperature = data.reduce((acc: any, item: { average_external_temperature: any; }) => acc + item.average_external_temperature, 0) / data.length;
    const avgInternalTemperature = data.reduce((acc: any, item: { average_internal_temperature: any; }) => acc + item.average_internal_temperature, 0) / data.length;
    const avgRPM = data.reduce((acc: any, item: { average_rpm: any; }) => acc + item.average_rpm, 0) / data.length;
    return (
        <div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4">
                <div className="bg-yellow-100 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-yellow-100 text-yellow-600 rounded-full p-2">
                        <MdBolt className="w-5 h-5" />
                    </div>
                    <div>
                        <div className="text-sm text-gray-600">Avg Power</div>
                        <div className="text-lg font-semibold text-gray-800">
                            {isNaN(avgPower) ? 0.0 : avgPower.toFixed(0)} kW
                        </div>
                    </div>
                </div>

                <div className="bg-zinc-300 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-zinc-300 text-yellow-600 rounded-full p-2">
                        <MdBolt className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-black-600">Max Power</div>
                    <div className="text-lg font-semibold text-gray-800">
                        {isNaN(maxPower) ? 0.0 : maxPower.toFixed(0)} kW
                    </div>
                </div>

                <div className="bg-blue-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-blue-200 text-blue-600 rounded-full p-2">
                        <FaWind className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Avg Wind Speed</div>
                    <div className="text-lg font-semibold">
                        {isNaN(avgWindSpeed) ? 0.0 : avgWindSpeed.toFixed(1)} m/s
                    </div>
                </div>
                <div className="bg-blue-300 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-blue-300 text-blue-600 rounded-full p-2">
                        <IoMdSpeedometer className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Max Wind Speed</div>
                    <div className="text-lg font-semibold">
                        {isNaN(maxWindSpeed) ? 0.0 : maxWindSpeed.toFixed(0)} m/s
                    </div>
                </div>
            </div>
            <br />
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-green-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-green-200 text-green-600 rounded-full p-2">
                        <SiProtractor className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Avg Azimuth</div>
                    <div className="text-lg font-semibold">
                        {isNaN(avgAzimuth) ? 0.0 : avgAzimuth.toFixed(0)} &deg;
                    </div>
                </div>
                <div className="bg-red-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-red-200 text-red-600 rounded-full p-2">
                        < LiaTemperatureHighSolid className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Avg External Temp</div>
                    <div className="text-lg font-semibold">
                        {isNaN(avgExternalTemperature) ? 0.0 : avgExternalTemperature.toFixed(1)} &deg;C
                    </div>
                </div>
                <div className="bg-cyan-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-cyan-200 text-cyan-600 rounded-full p-2">
                        < LiaTemperatureHighSolid className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Avg Internal Temp</div>
                    <div className="text-lg font-semibold">
                        {isNaN(avgInternalTemperature) ? 0.0 : avgInternalTemperature.toFixed(1)} &deg;C
                    </div>
                </div>
                <div className="bg-purple-200 p-3 rounded-lg shadow-sm flex items-center gap-3">
                    <div className="bg-purple-200 text-purple-600 rounded-full p-2">
                        <MdOutlineWindPower className="w-5 h-5" />
                    </div>
                    <div className="text-sm text-gray-600">Avg Rotor Speed</div>
                    <div className="text-lg font-semibold">
                        {isNaN(avgRPM) ? 0.0 : avgRPM.toFixed(1)} rpm
                    </div>
                </div>
            </div>
        </div>
    );
}