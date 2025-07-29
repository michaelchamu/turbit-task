import Header from './components/common/Header';
import Footer from './components/common/Footer';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-6">
        This is the main content area.
      </main>
      <Footer />
    </div>
  );
}

export default App;