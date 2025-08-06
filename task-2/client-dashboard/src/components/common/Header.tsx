import { NavLink } from "react-router-dom";

export default function Header() {
    return (
        <header className="bg-gray-800 text-gray-200 py-4 shadow-md">
            <div className="container mx-auto px-4 flex items-center justify-between">
                <h1 className="text-xl font-bold">Wind Turbine Dashboard</h1>
                <nav>
                    <ul className="flex space-x-4">
                        <li><NavLink to="/" className="hover:underline">Turbines</NavLink></li>
                        <li><NavLink to="/settings" className="hover:underline">Settings</NavLink></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}
