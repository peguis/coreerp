import { useContext, useState } from "react";
import { Check, Eye, EyeOff, Lock, LogIn, Mail } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { loginRequest } from "../api/auth";
import { AuthContext } from "../auth/AuthContext";

import "./Login.css";

export default function Login() {

    const navigate = useNavigate();
    const { login } = useContext(AuthContext);

    const [email, setEmail] = useState("");

    const [senha, setSenha] = useState("");

    const [loading, setLoading] = useState(false);

    const [mostrarSenha, setMostrarSenha] = useState(false);

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
        <main className="login-page">
            <section className="login-showcase" aria-label="Identidade HYPE STUDIO">
                <div className="login-showcase-overlay" />
                <div className="login-showcase-content">
                    <div className="login-brand-lockup">
                        <span className="hype-brand-mark" aria-hidden="true">H</span>
                        <span>
                            <strong>HYPE STUDIO</strong>
                            <small>BARBEARIA &amp; TATTOO</small>
                        </span>
                    </div>
                    <div className="login-showcase-slogan">
                        <strong>ESTILO</strong>
                        <strong>DISCIPLINA</strong>
                        <strong>IDENTIDADE</strong>
                    </div>
                    <p>“Mais que um corte,<br />uma expressão.”</p>
                </div>
            </section>

            <section className="login-panel">
                <div className="login-card">
                    <div className="login-header">
                        <span className="login-eyebrow">HYPE STUDIO · GESTÃO</span>
                        <h1>Bem-vindo de volta!</h1>
                        <p>Acesse o sistema da HYPE STUDIO</p>
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
                            <span><Check size={14} /> Acesso seguro</span>
                            <button type="button" className="login-forgot" onClick={() => undefined}>Esqueceu a senha?</button>
                        </div>

                        <button type="submit" disabled={loading}>
                            <LogIn size={20} />
                            {loading ? "Entrando..." : "Entrar"}
                        </button>
                    </form>

                    <div className="login-divider"><span>ou continue com</span></div>
                    <div className="login-provider-row" aria-label="Provedores de acesso">
                        <span>Google</span>
                        <span>Microsoft</span>
                    </div>
                    <p className="login-powered">Sistema de gestão | Powered by <strong>Pegs</strong></p>
                </div>
            </section>
        </main>
    );

}
