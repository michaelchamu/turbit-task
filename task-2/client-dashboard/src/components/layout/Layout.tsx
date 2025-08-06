import Header from '../common/Header';
import Footer from '../common/Footer';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow container mx-auto px-4 py-6">
                {children}
            </main>
            <Footer />
        </div>
    );
}