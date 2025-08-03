import { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { fetchTurbineList } from "../../services/api_service";
import { errorNotification, warningNotification } from "../common/ToastNotification";
import logger from '../../utils/logger';

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
    const [dateRange, setDateRange] = useState<[Date | null, Date | null]>([
        new Date("2016-01-01"),
        new Date("2016-01-10")
    ]);
    const [startDate, endDate] = dateRange;
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetchTurbines();
        handleApply();
    }, []);

    const fetchTurbines = async () => {
        try {
            const data = await fetchTurbineList();
            setTurbineOptions(data);
            setTurbineId(data[0] || '');
        } catch (error) {
            logger.error('Failed to fetch turbine list:', error);
            errorNotification('Could not load turbine list. Please try again.');
        }
    };

    const handleApply = async () => {

        if (!startDate || !endDate) {
            warningNotification("Please select both start and end dates.");
            return;
        }

        const start = new Date(startDate);
        const end = new Date(endDate);

        const daysDiff = (end.getTime() - start.getTime()) / (1000 * 3600 * 24);
        if (daysDiff > 365) {
            const proceed = window.confirm(
                `You've selected ${Math.round(daysDiff)} days of data. This might take a while to load. Continue?`
            );
            if (!proceed) return;
        }

        setIsLoading(true);

        try {
            const formattedStartDate = `${startDate.toISOString().split('T')[0]}T00:00:00`;
            const formattedEndDate = `${endDate.toISOString().split('T')[0]}T23:59:59`;

            onFilterChange({
                turbineId,
                startDate: formattedStartDate,
                endDate: formattedEndDate
            });
        } catch (error) {
            logger.error("Error applying filters:", error);
            errorNotification("Error applying filters. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleQuickDate = (days: number) => {
        const end = new Date();
        const start = new Date();
        start.setDate(end.getDate() - days);
        setDateRange([start, end]);
    };

    const handleReset = () => {
        setTurbineId("Turbine1");
        setDateRange([new Date("2016-01-01"), new Date("2016-01-10")]);
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

            {/* Unified Date Range Picker */}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date Range
                </label>
                <DatePicker
                    selectsRange
                    startDate={startDate}
                    endDate={endDate}
                    onChange={(update) => {
                        setDateRange(update);
                    }}
                    showMonthDropdown
                    showYearDropdown
                    isClearable={true}
                    className="w-full h-[40px] border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    dateFormat="yyyy-MM-dd"
                    placeholderText="Select date range"
                /></div>

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