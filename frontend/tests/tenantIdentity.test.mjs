import assert from "node:assert/strict";
import test from "node:test";

import {
    TENANT_KEYS,
    TenantIdentityError,
    createTenantIdentity,
    resolveTenantIdentity,
    tenantIdentityToCssVariables
} from "../src/tenant/tenantIdentity.js";

test("HYPE resolve a logo oficial e a paleta dourada", () => {
    const identity = createTenantIdentity(TENANT_KEYS.HYPE, { nome: "HYPE STUDIO" });
    const css = tenantIdentityToCssVariables(identity);

    assert.equal(identity.tenantKey, "hype");
    assert.match(identity.tenantLogo, /tenants\/hype\/logo\.png$/);
    assert.match(identity.assets.sidebarLogo, /tenants\/hype\/logo\.png$/);
    assert.equal(identity.tenantPrimaryColor, "#d9ab3f");
    assert.equal(css["--tenant-accent"], "#d9ab3f");
    assert.equal(identity.slogan.join(" "), "ESTILO DISCIPLINA IDENTIDADE");
});

test("Pegs-demo resolve logo, texto e paleta da plataforma", () => {
    const identity = createTenantIdentity(TENANT_KEYS.PEGS_DEMO, { nome: "Studio Demo" });
    const css = tenantIdentityToCssVariables(identity);

    assert.equal(identity.tenantKey, "pegs-demo");
    assert.match(identity.tenantLogo, /tenants\/demo\/logo\.png$/);
    assert.match(identity.assets.loginLogo, /tenants\/demo\/logo\.png$/);
    assert.equal(identity.tenantPrimaryColor, "#6f8cff");
    assert.equal(identity.tenantLoginMessage, "Acesse a plataforma Pegs");
    assert.equal(css["--tenant-accent"], "#6f8cff");
});

test("uma empresa não herda asset ou cor da outra identidade", () => {
    const hype = createTenantIdentity(TENANT_KEYS.HYPE, {
        nome: "HYPE STUDIO",
        logo_url: "/brand/pegs/logo.png",
        cor_primaria: "#6f8cff",
        cor_secundaria: "#9bb0ff"
    });
    const demo = createTenantIdentity(TENANT_KEYS.PEGS_DEMO, {
        nome: "Studio Demo",
        logo_url: "/tenants/hype/logo.png",
        cor_primaria: "#d9ab3f",
        cor_secundaria: "#edc45c"
    });

    assert.match(hype.assets.sidebarLogo, /tenants\/hype\/logo\.png$/);
    assert.equal(hype.tenantPrimaryColor, "#d9ab3f");
    assert.match(demo.assets.sidebarLogo, /tenants\/demo\/logo\.png$/);
    assert.equal(demo.tenantPrimaryColor, "#6f8cff");
});

test("a resolução usa o codigo do tenant, o host ou falha de forma controlada", () => {
    assert.equal(
        resolveTenantIdentity({ empresa: { identidade_codigo: "hype" } }).tenantKey,
        "hype"
    );
    assert.equal(
        resolveTenantIdentity({ hostname: "hype-studio.omrender.com" }).tenantKey,
        "hype"
    );
    assert.equal(
        resolveTenantIdentity({ hostname: "pegs-demo.example.com" }).tenantKey,
        "pegs-demo"
    );
    assert.throws(
        () => resolveTenantIdentity({ hostname: "localhost" }),
        TenantIdentityError
    );
});

test("a configuração explícita funciona no primeiro carregamento e após recarregar", () => {
    const primeiroCarregamento = resolveTenantIdentity({ configuredKey: "hype" });
    const recarregamento = resolveTenantIdentity({ configuredKey: "hype" });
    assert.deepEqual(
        tenantIdentityToCssVariables(primeiroCarregamento),
        tenantIdentityToCssVariables(recarregamento)
    );
    assert.equal(primeiroCarregamento.assets.loginLogo, recarregamento.assets.loginLogo);
});
