import { useState } from "react";

type SidebarProps = {
    // Props for filter logic if needed
    onFilterChange: (filters: {
        turbineId?: string;
        startDate?: string;
        endDate?: string;
    }) => void;
};


const Sidebar = ({ onFilterChange }: SidebarProps) => {
    const [turbineId, setTurbineId] = useState("Turbine2"); //by default always use Turbine1
    const [startDate, setStartDate] = useState("2016-01-01T00:00:00");
    const [endDate, setEndDate] = useState("2016-01-10T00:00:00");

    //fix this to pull Turbine list from API
    const turbineOptions = [
        "Turbine1",
        "Turbine2",
        "Turbine3",
        "Turbine4"
    ];
    const handleApply = () => {
        if (!startDate || !endDate)
            return;
        const formattedStartDate = new Date(startDate).toISOString().slice(0, 19);
        const formattedEndDate = new Date(endDate).toISOString().slice(0, 19);

        onFilterChange({
            turbineId,
            startDate: formattedStartDate,
            endDate: formattedEndDate
        });
    }
    return (
        <div className="bg-white shadow rounded-lg p-4 space-y-4">
            <h2 className="text-lg font-semibold">Filters</h2>

            <div>
                <label className="block text-sm font-medium">Turbine ID</label>
                <input
                    type="text"
                    className="w-full border rounded px-2 py-1"
                    value={turbineId}
                    onChange={(e) => setTurbineId(e.target.value)}
                />
            </div>

            <div>
                <label className="block text-sm font-medium">Start Date</label>
                <input
                    type="date"
                    className="w-full border rounded px-2 py-1"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </div>

            <div>
                <label className="block text-sm font-medium">End Date</label>
                <input
                    type="date"
                    className="w-full border rounded px-2 py-1"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>

            <button
                onClick={handleApply}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            >
                Apply Filters
            </button>
        </div>
    );
};
export default Sidebar;