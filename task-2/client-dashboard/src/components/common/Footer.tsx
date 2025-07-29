export default function Footer() {
    return (
        <footer className="bg-gray-800 text-gray-200 py-4 mt-auto">
            <div className="container mx-auto px-4 text-center text-sm">
                © {new Date().getFullYear()} Turbit GmbH Demo Dashboard . All rights reserved.
            </div>
        </footer>
    );
}
