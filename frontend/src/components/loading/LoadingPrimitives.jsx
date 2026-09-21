import { useTenant } from "../../tenant/TenantContextValue";
import { DEFAULT_DELAY, DEFAULT_MIN_DURATION, useLoadingVisibility } from "./loadingTiming";

import "./LoadingPrimitives.css";

function TenantMark({ className = "" }) {
    const tenant = useTenant();
    const identity = tenant.status === "ready" ? tenant.identity : null;
    const source = identity?.assets?.loginLogo || identity?.assets?.sidebarLogo;

    if (!source) {
        return <span className={`loading-mark loading-mark-fallback ${className}`} aria-hidden="true">P</span>;
    }

    return <img className={`loading-mark ${className}`} src={source} alt={identity?.tenantName || "Marca do ambiente"} />;
}

export function LoadingState({
    message = "Preparando o ambiente...",
    variant = "section",
    showBrand = true,
    className = "",
    delay = DEFAULT_DELAY,
    minDuration = DEFAULT_MIN_DURATION
}) {
    const visible = useLoadingVisibility(true, { delay, minDuration });

    return (
        <div
            className={`loading-state loading-state-${variant} ${visible ? "is-visible" : "is-pending"} ${className}`}
            role="status"
            aria-live="polite"
            aria-busy="true"
        >
            {showBrand && <TenantMark />}
            <span className="loading-indicator" aria-hidden="true" />
            <span>{message}</span>
        </div>
    );
}

export function PageLoading({ message = "Preparando o ambiente...", ...props }) {
    return <LoadingState {...props} message={message} variant="page" />;
}

export function SectionLoading({ message = "Carregando dados...", ...props }) {
    return <LoadingState {...props} message={message} variant="section" />;
}

export function SkeletonTable({ columns = 5, rows = 5, className = "" }) {
    return (
        <div className={`loading-table-skeleton ${className}`} role="status" aria-live="polite" aria-busy="true" aria-label="Carregando tabela">
            <div className="loading-table-skeleton-row loading-table-skeleton-head" aria-hidden="true">
                {Array.from({ length: columns }, (_, index) => <span key={index} />)}
            </div>
            {Array.from({ length: rows }, (_, row) => (
                <div className="loading-table-skeleton-row" key={row} aria-hidden="true">
                    {Array.from({ length: columns }, (_, column) => <span key={column} className={column === 0 ? "is-wide" : ""} />)}
                </div>
            ))}
        </div>
    );
}

export function SkeletonCards({ count = 4, className = "" }) {
    return (
        <div className={`loading-cards-skeleton ${className}`} role="status" aria-live="polite" aria-busy="true" aria-label="Carregando indicadores">
            {Array.from({ length: count }, (_, index) => (
                <article className="loading-card-skeleton" key={index} aria-hidden="true">
                    <span className="loading-skeleton-line loading-skeleton-label" />
                    <span className="loading-skeleton-line loading-skeleton-value" />
                    <span className="loading-skeleton-line loading-skeleton-detail" />
                </article>
            ))}
        </div>
    );
}

export function LoadingError({
    message = "Não foi possível carregar os dados.",
    onRetry,
    retryLabel = "Tentar novamente",
    children,
    className = ""
}) {
    return (
        <div className={`loading-feedback loading-feedback-error ${className}`} role="alert" aria-live="assertive">
            {children || <strong>{message}</strong>}
            {onRetry && <button type="button" onClick={onRetry}>{retryLabel}</button>}
        </div>
    );
}

export function LoadingEmpty({
    title = "Nenhum registro encontrado.",
    description = "Não existem dados para exibir.",
    children,
    className = ""
}) {
    return (
        <div className={`loading-feedback loading-feedback-empty ${className}`} role="status" aria-live="polite">
            <strong>{title}</strong>
            <span>{description}</span>
            {children}
        </div>
    );
}
