import { useContext, useState } from "react";
import { Eye, EyeOff, Lock, Mail } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { loginRequest } from "../api/auth";
import { AuthContext } from "../auth/AuthContextValue";
import { TenantErrorState, TenantLoading } from "../tenant/TenantContext";
import { useTenant } from "../tenant/TenantContextValue";
import { PLATFORM_ASSETS } from "../tenant/tenantIdentity";

import "./Login.css";

export default function Login() {

    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
    const tenant = useTenant();

    const [email, setEmail] = useState("");

    const [senha, setSenha] = useState("");

    const [loading, setLoading] = useState(false);

    const [mostrarSenha, setMostrarSenha] = useState(false);

    const [lembrarDeMim, setLembrarDeMim] = useState(false);

    const [mostrarAjudaSenha, setMostrarAjudaSenha] = useState(false);

    if (tenant.status === "loading") return <TenantLoading />;
    if (tenant.status === "error") return <TenantErrorState error={tenant.error} />;

    const { identity, cssVariables } = tenant;
    const loginStyle = {
        ...cssVariables,
        "--tenant-login-hero": identity.assets.loginHero ? `url(${identity.assets.loginHero})` : "none"
    };

    async function entrar(e) {

        e.preventDefault();

        try {

            setLoading(true);

            const dados = await loginRequest(email, senha);
            login(dados.access_token);

            navigate("/");

        } catch {

            alert("E-mail ou senha inválidos.");

        } finally {

            setLoading(false);

        }

    }

    return (
        <main className={`login-page tenant-login tenant-login-${identity.tenantKey}`} data-tenant-key={identity.tenantKey} style={loginStyle}>
            <section className="login-showcase" aria-label={`Identidade ${identity.tenantName}`}>
                <div className="login-showcase-overlay" />
                <div className="login-showcase-content">
                    <div className="login-brand-lockup" aria-label={identity.tenantBrandName}>
                        <img className="login-logo-image" src={identity.assets.loginLogo} alt={identity.tenantBrandName} />
                    </div>
                    <div className="login-showcase-divider" aria-hidden="true" />
                    <div className="login-showcase-slogan">
                        {identity.slogan.map((line) => <strong key={line}>{line}</strong>)}
                    </div>
                </div>
            </section>

            <section className="login-panel">
                <div className="login-card">
                    <div className="login-header">
                        <h1>Bem-vindo de volta!</h1>
                        <p>{identity.tenantLoginMessage}</p>
                    </div>

                    <form onSubmit={entrar} className="login-form">
                        <div className="input-group">
                            <Mail size={20} aria-hidden="true" />
                            <input type="email" aria-label="E-mail" autoComplete="username" placeholder="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} required />
                        </div>

                        <div className="input-group">
                            <Lock size={20} aria-hidden="true" />
                            <input type={mostrarSenha ? "text" : "password"} aria-label="Senha" autoComplete="current-password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} required />
                            <button type="button" className="login-password-toggle" aria-label={mostrarSenha ? "Ocultar senha" : "Mostrar senha"} onClick={() => setMostrarSenha((atual) => !atual)}>
                                {mostrarSenha ? <EyeOff size={17} /> : <Eye size={17} />}
                            </button>
                        </div>

                        <div className="login-support-row">
                            <label className="login-remember">
                                <input type="checkbox" checked={lembrarDeMim} onChange={(e) => setLembrarDeMim(e.target.checked)} />
                                <span>Lembrar de mim</span>
                            </label>
                            <button type="button" className="login-forgot" onClick={() => setMostrarAjudaSenha((atual) => !atual)}>Esqueceu a senha?</button>
                        </div>

                        {mostrarAjudaSenha && (
                            <p className="login-forgot-message" role="status" aria-live="polite">
                                Para trocar a senha, entre em contato com o gerente ou administrador da sua empresa.
                            </p>
                        )}

                        <button type="submit" disabled={loading}>
                            {loading ? "Entrando..." : "Entrar"}
                        </button>
                    </form>
                    <p className="login-powered">
                        <span>Sistema de gestão | Powered by</span>
                        <span className="login-powered-brand">
                            <img src={PLATFORM_ASSETS.logo} alt="Pegs" />
                        </span>
                    </p>
                </div>
            </section>
        </main>
    );

}
