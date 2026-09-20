const TENANT_KEYS = Object.freeze({
    HYPE: "hype",
    PEGS_DEMO: "pegs-demo"
});

const KNOWN_TENANT_KEYS = new Set(Object.values(TENANT_KEYS));

const PALETTES = Object.freeze({
    pegs: Object.freeze({
        primary: "#6f8cff",
        secondary: "#9bb0ff"
    }),
    hype: Object.freeze({
        primary: "#d9ab3f",
        secondary: "#edc45c"
    })
});

const TENANT_REGISTRY = Object.freeze({
    [TENANT_KEYS.HYPE]: Object.freeze({
        tenantKey: TENANT_KEYS.HYPE,
        tenantBrandName: "HYPE STUDIO",
        tenantName: "HYPE STUDIO",
        businessType: "Barbearia & Tattoo",
        theme: "dark",
        primary: PALETTES.hype.primary,
        secondary: PALETTES.hype.secondary,
        background: "#0b0b0c",
        surface: "#151517",
        surfaceRaised: "#1d1d20",
        surfaceElevated: "#232326",
        border: "#2d2d31",
        borderStrong: "#414148",
        text: "#f5f2ea",
        textSecondary: "#aaa69c",
        textMuted: "#77736b",
        loginMessage: "Acesse o sistema da HYPE STUDIO",
        slogan: ["ESTILO", "DISCIPLINA", "IDENTIDADE"],
        assets: Object.freeze({
            sidebarLogo: "/tenants/hype/logo.png",
            loginLogo: "/tenants/hype/logo-official.png",
            favicon: "/tenants/hype/logo-official.png",
            loginHero: "/tenants/hype/login-hero.png"
        })
    }),
    [TENANT_KEYS.PEGS_DEMO]: Object.freeze({
        tenantKey: TENANT_KEYS.PEGS_DEMO,
        tenantBrandName: "Pegs",
        tenantName: "Pegs Demo",
        businessType: "Plataforma de gestão",
        theme: "platform",
        primary: PALETTES.pegs.primary,
        secondary: PALETTES.pegs.secondary,
        background: "#0b1017",
        surface: "#11161d",
        surfaceRaised: "#18202b",
        surfaceElevated: "#202a38",
        border: "#2b3544",
        borderStrong: "#43516a",
        text: "#f1f5fb",
        textSecondary: "#aab5c5",
        textMuted: "#718096",
        loginMessage: "Acesse a plataforma Pegs",
        slogan: ["ORGANIZAÇÃO", "OPERAÇÃO", "CRESCIMENTO"],
        assets: Object.freeze({
            sidebarLogo: "/tenants/demo/logo.png",
            loginLogo: "/tenants/demo/logo.png",
            favicon: "/tenants/demo/logo.png",
            loginHero: null
        })
    })
});

export const PLATFORM_ASSETS = Object.freeze({
    logo: "/brand/pegs/logo.png"
});

export class TenantIdentityError extends Error {
    constructor(message, details = {}) {
        super(message);
        this.name = "TenantIdentityError";
        this.details = details;
    }
}

function normalizarTexto(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim()
        .toLowerCase();
}

export function normalizarTenantKey(value) {
    const normalized = normalizarTexto(value).replace(/_/g, "-");
    if (KNOWN_TENANT_KEYS.has(normalized)) return normalized;
    if (["pegs", "coreerp", "demo"].includes(normalized)) return TENANT_KEYS.PEGS_DEMO;
    if (["hype-studio", "hype studio"].includes(normalized)) return TENANT_KEYS.HYPE;
    return null;
}

function tenantKeyFromHost(hostname) {
    const host = normalizarTexto(hostname);
    if (host.includes("hype-studio")) return TENANT_KEYS.HYPE;
    if (host.includes("pegs") || host.includes("coreerp") || host.includes("demo")) {
        return TENANT_KEYS.PEGS_DEMO;
    }
    return null;
}

function tenantKeyFromCompany(empresa) {
    const explicit = normalizarTenantKey(
        empresa?.identidade_codigo || empresa?.tenant_key || empresa?.tenantKey
    );
    if (explicit) return explicit;

    const companyText = normalizarTexto(`${empresa?.nome || ""} ${empresa?.email || ""}`);
    if (companyText.includes("hype")) return TENANT_KEYS.HYPE;
    if (companyText.includes("pegs") || companyText.includes("coreerp") || companyText.includes("demo")) {
        return TENANT_KEYS.PEGS_DEMO;
    }
    return null;
}

export function resolveTenantKey({ empresa = null, hostname = "", configuredKey = "" } = {}) {
    return tenantKeyFromCompany(empresa)
        || normalizarTenantKey(configuredKey)
        || tenantKeyFromHost(hostname)
        || (() => {
            throw new TenantIdentityError(
                "Não foi possível resolver a identidade visual do tenant.",
                { empresaId: empresa?.id || null, hostname }
            );
        })();
}

function isValidColor(value) {
    return /^#[0-9a-f]{6}$/i.test(String(value || "").trim());
}

function colorOrFallback(value, fallback, forbidden = []) {
    const normalized = String(value || "").trim().toLowerCase();
    if (!isValidColor(normalized) || forbidden.includes(normalized)) return fallback;
    return normalized;
}

function assetOrFallback(value, fallback, forbiddenPattern) {
    const normalized = String(value || "").trim();
    if (!normalized || forbiddenPattern?.test(normalized)) return fallback;
    return normalized;
}

export function createTenantIdentity(tenantKey, empresa = null) {
    const base = TENANT_REGISTRY[normalizarTenantKey(tenantKey)];
    if (!base) {
        throw new TenantIdentityError("Identidade visual de tenant não cadastrada.", { tenantKey });
    }

    const isHype = base.tenantKey === TENANT_KEYS.HYPE;
    const forbiddenColors = isHype
        ? [PALETTES.pegs.primary, PALETTES.pegs.secondary]
        : [PALETTES.hype.primary, PALETTES.hype.secondary];
    const forbiddenLogo = isHype ? /pegs|coreerp/i : /hype/i;

    return Object.freeze({
        ...base,
        tenantName: empresa?.nome?.trim() || base.tenantName,
        businessType: empresa?.tipo_negocio?.trim() || base.businessType,
        tenantPrimaryColor: colorOrFallback(empresa?.cor_primaria, base.primary, forbiddenColors),
        tenantAccentColor: colorOrFallback(empresa?.cor_secundaria, base.secondary, forbiddenColors),
        tenantBackground: base.background,
        tenantLoginMessage: base.loginMessage,
        tenantTheme: base.theme,
        tenantLogo: assetOrFallback(empresa?.logo_url, base.assets.sidebarLogo, forbiddenLogo),
        assets: Object.freeze({
            ...base.assets,
            sidebarLogo: assetOrFallback(empresa?.logo_url, base.assets.sidebarLogo, forbiddenLogo)
        })
    });
}

export function resolveTenantIdentity(options = {}) {
    const tenantKey = resolveTenantKey(options);
    return createTenantIdentity(tenantKey, options.empresa);
}

export function tenantIdentityToCssVariables(identity) {
    const primary = identity.tenantPrimaryColor;
    const secondary = identity.tenantAccentColor;
    return {
        "--tenant-accent": primary,
        "--tenant-accent-secondary": secondary,
        "--tenant-accent-soft": `color-mix(in srgb, ${primary} 12%, transparent)`,
        "--tenant-bg": identity.tenantBackground,
        "--tenant-surface": identity.surface,
        "--tenant-surface-raised": identity.surfaceRaised,
        "--tenant-surface-elevated": identity.surfaceElevated,
        "--tenant-border": identity.border,
        "--tenant-border-strong": identity.borderStrong,
        "--tenant-text": identity.text,
        "--tenant-text-secondary": identity.textSecondary,
        "--tenant-text-muted": identity.textMuted,
        "--color-primary": primary,
        "--primary": primary,
        "--primary-color": primary,
        "--background": identity.tenantBackground,
        "--background-secondary": identity.surfaceRaised,
        "--bg-page": identity.tenantBackground,
        "--bg-card": identity.surface,
        "--bg-muted": identity.surfaceRaised,
        "--border-color": identity.border,
        "--focus-ring": `0 0 0 3px color-mix(in srgb, ${primary} 18%, transparent)`,
        "--tenant-success": "#43c58b",
        "--tenant-warning": "#e1ae4a",
        "--tenant-danger": "#e26b72"
    };
}

export function applyTenantDocumentIdentity(identity) {
    if (typeof document === "undefined") return;

    document.title = identity.tenantKey === TENANT_KEYS.PEGS_DEMO
        ? `${identity.tenantName} · Pegs`
        : identity.tenantName;
    let favicon = document.querySelector("link[data-tenant-favicon]");
    if (!favicon) {
        favicon = document.createElement("link");
        favicon.rel = "icon";
        favicon.dataset.tenantFavicon = "true";
        document.head.appendChild(favicon);
    }
    favicon.href = identity.assets.favicon;
}

export { TENANT_KEYS, TENANT_REGISTRY };
