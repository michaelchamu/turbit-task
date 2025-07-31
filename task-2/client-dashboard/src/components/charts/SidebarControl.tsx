// Sidebar.tsx
import { useState, useEffect } from "react";
import { fetchTurbineList } from "../../services/apiService";

type SidebarProps = {
    onFilterChange: (filters: {
        turbineId?: string;
        startDate?: string;
        endDate?: string;
    }) => void;
};

const SidebarControl = ({ onFilterChange }: SidebarProps) => {
    const [turbineOptions, setTurbineOptions] = useState<string[]>([]);
    const [turbineId, setTurbineId] = useState("");
    const [startDate, setStartDate] = useState("2016-01-01");
    const [endDate, setEndDate] = useState("2016-01-10");
    const [isLoading, setIsLoading] = useState(false);

    // Auto-apply filters on component mount
    useEffect(() => {
        //load turbines from database 1st
        fetchTurbines();
        handleApply();
    }, []); // Run once on mount

    const fetchTurbines = async () => {
        try {
            const data = await fetchTurbineList();
            setTurbineOptions(data);
            setTurbineId(data[0] || '');

        } catch (error) {
            console.error('Failed to fetch turbine list:', error);
            alert('Could not load turbine list. Please try again.');
        }
    }
    const handleApply = async () => {
        if (!startDate || !endDate) {
            alert("Please select both start and end dates");
            return;
        }

        // Validate date range
        const start = new Date(startDate);
        const end = new Date(endDate);

        if (start >= end) {
            alert("Start date must be before end date");
            return;
        }

        // Check if date range is too large (optional)
        const daysDiff = (end.getTime() - start.getTime()) / (1000 * 3600 * 24);
        if (daysDiff > 365) {
            const proceed = window.confirm(
                `You've selected ${Math.round(daysDiff)} days of data. This might take a while to load. Continue?`
            );
            if (!proceed) return;
        }

        setIsLoading(true);

        try {
            // Format dates to include time for the API
            const formattedStartDate = `${startDate}T00:00:00`;
            const formattedEndDate = `${endDate}T23:59:59`;

            onFilterChange({
                turbineId,
                startDate: formattedStartDate,
                endDate: formattedEndDate
            });
        } catch (error) {
            console.error("Error applying filters:", error);
            alert("Error applying filters. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    // Quick date range presets
    const handleQuickDate = (days: number) => {
        const end = new Date();
        const start = new Date();
        start.setDate(end.getDate() - days);

        setStartDate(start.toISOString().split('T')[0]);
        setEndDate(end.toISOString().split('T')[0]);
    };

    // Reset to default values
    const handleReset = () => {
        setTurbineId("Turbine2");
        setStartDate("2016-01-01");
        setEndDate("2016-01-10");
    };

    return (
        <div className="bg-white shadow rounded-lg p-4 space-y-4">
            <h2 className="text-lg font-semibold text-gray-800">Data Filters</h2>

            {/* Turbine Selection */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Turbine ID
                </label>
                <select
                    className="w-full h-[40px] border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={turbineId}
                    onChange={(e) => setTurbineId(e.target.value)}
                >
                    {turbineOptions.map((turbine) => (
                        <option key={turbine} value={turbine}>
                            {turbine}
                        </option>
                    ))}
                </select>
            </div>

            {/* Date Range Selection */}
            <div className="space-y-3">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Date Range
                    </label>
                    <div className="flex items-end gap-2">
                        <div className="flex-1">
                            <label className="block text-xs font-medium text-gray-500 mb-1">
                                From
                            </label>
                            <input
                                type="date"
                                className="w-full h-[40px] border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                max={endDate}
                            />
                        </div>
                        <div className="text-gray-400 pb-2">
                            —
                        </div>
                        <div className="flex-1">
                            <label className="block text-xs font-medium text-gray-500 mb-1">
                                To
                            </label>
                            <input
                                type="date"
                                className="w-full h-[40px] border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                min={startDate}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Quick Date Presets */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quick Select
                </label>
                <div className="grid grid-cols-2 gap-2">
                    <button
                        onClick={() => handleQuickDate(7)}
                        className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                    >
                        Last 7 days
                    </button>
                    <button
                        onClick={() => handleQuickDate(30)}
                        className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                    >
                        Last 30 days
                    </button>
                    <button
                        onClick={() => handleQuickDate(90)}
                        className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                    >
                        Last 3 months
                    </button>
                    <button
                        onClick={() => handleQuickDate(365)}
                        className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                    >
                        Last year
                    </button>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-2">
                <button
                    onClick={handleApply}
                    disabled={isLoading || !startDate || !endDate}
                    className={`w-full py-2 px-4 rounded-md font-medium transition-colors ${isLoading || !startDate || !endDate
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                        }`}
                >
                    {isLoading ? (
                        <div className="flex items-center justify-center">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Loading...
                        </div>
                    ) : (
                        'Apply Filters'
                    )}
                </button>

                <button
                    onClick={handleReset}
                    className="w-full py-2 px-4 rounded-md font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                    Reset to Default
                </button>
            </div>
        </div>
    );
};

export default SidebarControl;