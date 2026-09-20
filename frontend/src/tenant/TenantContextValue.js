import { createContext, useContext } from "react";

export const TenantContext = createContext(null);

export function useTenant() {
    const context = useContext(TenantContext);
    if (!context) throw new Error("useTenant deve ser usado dentro de TenantProvider.");
    return context;
}
