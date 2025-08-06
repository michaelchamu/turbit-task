import { Route, Routes } from "react-router-dom";
import App from "./App";
import Settings from "./components/common/Settings";

const AppRoutes = () => {

    return (
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/settings" element={<Settings />} />
        </Routes>
    )
}
export default AppRoutes;