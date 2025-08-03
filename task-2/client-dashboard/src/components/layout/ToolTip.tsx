

export const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;

        if (data.average_wind_speed) {
            return (
                <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
                    <p className="font-semibold text-orange-600">Aggregated Data Point</p>
                    <p>{`Wind Speed: ${data.average_wind_speed.toFixed(1)} m/s`}</p>
                    <p>{`Power: ${data.average_power.toFixed(0)} kW`}</p>
                    <p>{`Azimuth: ${data.average_azimuth.toFixed(0)} `}&deg;</p>
                    <p>{`External Temperature: ${data.average_external_temperature.toFixed(0)}`}&deg;C</p>
                    <p>{`Internal Temperature: ${data.average_internal_temperature.toFixed(0)}`}&deg;C</p>
                    <p>{`Rotor Speed: ${data.average_rpm.toFixed(0)} RPM`}</p>
                </div>
            );
        }
    }
}