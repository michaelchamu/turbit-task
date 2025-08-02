import { FiAlertTriangle } from "react-icons/fi";

export const NoDataView = () => {
    return (
        <div className="flex flex-col items-center justify-center text-gray-600 bg-gray-50 rounded-lg border border-gray-200 shadow-inner h-[300px] w-full p-6">
            <FiAlertTriangle className="w-10 h-10 text-yellow-500 mb-4" />
            <h3 className="text-lg font-semibold">No Data to Display</h3>
            <p className="text-sm text-gray-500 mt-1">
                Try adjusting your filters or date range to load data.
            </p>
        </div>
    );
};