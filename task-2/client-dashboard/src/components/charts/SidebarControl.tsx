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
    const [turbineId, setTurbineId] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const handleApply = () => {
        onFilterChange({ turbineId, startDate, endDate });
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