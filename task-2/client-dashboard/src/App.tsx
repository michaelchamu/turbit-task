import { useEffect, useState } from 'react';
import { ToastContainer } from 'react-toastify';
import TimeseriesChart from './components/charts/TimeSeriesChart';
import SidebarControl from './components/controls/SidebarControl';
import Overlay from './components/common/Overlay';
import Layout from './components/layout/Layout';

const App = () => {
  const [filters, setFilters] = useState<{
    turbineId?: string;
    startDate?: string;
    endDate?: string;
  }>({});

  const [showOverlay, setShowOverlay] = useState<boolean>(true);

  useEffect(() => {

    const timer = setTimeout(() => {
      setShowOverlay(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      {showOverlay && <Overlay />}
      <Layout >

        <ToastContainer position="top-center" autoClose={3000} />
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

      </Layout>
    </>
  );
}

export default App;