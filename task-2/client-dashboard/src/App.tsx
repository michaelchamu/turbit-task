import Header from './components/common/Header';
import Footer from './components/common/Footer';
import TimeseriesChart from './components/charts/TimeSeriesChart';
import { useState } from 'react';
import SidebarControl from './components/charts/SidebarControl';

const App = () => {
  const [filters, setFilters] = useState<{
    turbineId?: string;
    startDate?: string;
    endDate?: string;
  }>({});
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-6">
        <div className='grid grid-cols-1 lg:grid-cols-12 gap-6'>
          <div className='lg:col-span-3'>
            <SidebarControl onFilterChange={setFilters} />
          </div>
          <div className='lg:col-span-9'>
            <TimeseriesChart
              turbineId={filters.turbineId}
              startDate={filters.startDate}
              endDate={filters.endDate}
            />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;