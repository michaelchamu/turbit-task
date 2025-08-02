export default function Header() {
    return (
        <header className="bg-gray-800 text-gray-200 py-4 shadow-md">
            <div className="container mx-auto px-4 flex items-center justify-between">
                <h1 className="text-xl font-bold">Wind Turbine Dashboard</h1>
                <nav>
                    <ul className="flex space-x-4">
                        <li><a href="#" className="hover:underline">Home</a></li>
                        <li><a href="#" className="hover:underline">Turbines</a></li>
                        <li><a href="#" className="hover:underline">Settings</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}
