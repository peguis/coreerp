import AppRoutes from "./routes/AppRoutes";
import { TenantProvider } from "./tenant/TenantContext";
import { BrowserRouter } from "react-router-dom";


function App() {


    return (

        <BrowserRouter>
            <TenantProvider>
                <AppRoutes />
            </TenantProvider>
        </BrowserRouter>

    );

}


export default App;
