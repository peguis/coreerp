import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { buscarIdentidadeEmpresaAtual } from "../services/empresaService";
import {
    applyTenantDocumentIdentity,
    createPegsMatrixIdentity,
    resolveTenantIdentity,
    TenantIdentityError,
    tenantIdentityToCssVariables
} from "./tenantIdentity";
import { TenantContext } from "./TenantContextValue";
import { shouldFetchAuthenticatedTenantIdentity } from "./tenantIdentityFlow";

import "./TenantState.css";

function getRuntimeTenantKey() {
    return import.meta.env?.VITE_TENANT_KEY || "";
}

function getHostname() {
    return typeof window === "undefined" ? "" : window.location.hostname;
}

export function TenantProvider({ children }) {
    const { token } = useAuth();
    const location = useLocation();
    const [estado, setEstado] = useState({
        status: "loading",
        empresa: null,
        identity: null,
        error: null
    });

    useEffect(() => {
        let montado = true;
        const hostname = getHostname();
        const configuredKey = getRuntimeTenantKey();
        const isMatrix = location.pathname.startsWith("/matriz");

        async function resolver() {
            setEstado({ status: "loading", empresa: null, identity: null, error: null });
            try {
                if (isMatrix) {
                    const identity = createPegsMatrixIdentity();
                    if (montado) {
                        applyTenantDocumentIdentity(identity);
                        setEstado({ status: "ready", empresa: null, identity, error: null });
                    }
                    return;
                }
                if (!shouldFetchAuthenticatedTenantIdentity(token, location.pathname)) {
                    const identity = resolveTenantIdentity({ hostname, configuredKey });
                    if (montado) {
                        applyTenantDocumentIdentity(identity);
                        setEstado({ status: "ready", empresa: null, identity, error: null });
                    }
                    return;
                }

                const empresa = await buscarIdentidadeEmpresaAtual();
                const identity = resolveTenantIdentity({ empresa, hostname, configuredKey });
                if (montado) {
                    applyTenantDocumentIdentity(identity);
                    setEstado({ status: "ready", empresa, identity, error: null });
                }
            } catch (error) {
                const tenantError = error instanceof TenantIdentityError
                    ? error
                    : new TenantIdentityError("Não foi possível carregar a identidade visual do tenant.", { cause: error });
                if (import.meta.env?.DEV) {
                    console.error("[tenant-identity]", tenantError);
                }
                if (montado) {
                    setEstado({ status: "error", empresa: null, identity: null, error: tenantError });
                }
            }
        }

        void resolver();
        return () => {
            montado = false;
        };
    }, [token, location.pathname]);

    const value = useMemo(() => ({
        ...estado,
        cssVariables: estado.identity ? tenantIdentityToCssVariables(estado.identity) : {},
        autenticado: Boolean(token)
    }), [estado, token]);

    return <TenantContext.Provider value={value}>{children}</TenantContext.Provider>;
}

export function TenantLoading() {
    return (
        <main className="tenant-state" role="status" aria-live="polite">
            <div className="tenant-state-spinner" aria-hidden="true" />
            <strong>Carregando identidade da empresa...</strong>
            <span>Preparando o ambiente correto.</span>
        </main>
    );
}

export function TenantErrorState({ error }) {
    return (
        <main className="tenant-state tenant-state-error" role="alert">
            <strong>Não foi possível identificar este tenant.</strong>
            <span>{error?.message || "Verifique a configuração da empresa e tente novamente."}</span>
            <small>O sistema não aplicou a identidade de outra empresa como fallback.</small>
        </main>
    );
}
