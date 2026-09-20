import AppRoutes from "./routes/AppRoutes";
import { TenantProvider } from "./tenant/TenantContext";


function App() {


    return (

        <TenantProvider>
            <AppRoutes />
        </TenantProvider>

    );

}


export default App;
