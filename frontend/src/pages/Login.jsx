import { useState } from "react";
import { Mail, Lock, LogIn } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { loginRequest } from "../api/auth";

import "./Login.css";

export default function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");

    const [senha, setSenha] = useState("");

    const [loading, setLoading] = useState(false);

    async function entrar(e) {

        e.preventDefault();

        try {

            setLoading(true);

            await loginRequest(email, senha);

            navigate("/dashboard");

        } catch {

            alert("E-mail ou senha inválidos.");

        } finally {

            setLoading(false);

        }

    }

    return (

        <main className="login-page">

            <div className="login-card">

                <div className="login-header">

                    <h1>

                        CoreERP

                    </h1>

                    <p>

                        Sistema ERP SaaS

                    </p>

                </div>

                <form
                    onSubmit={entrar}
                    className="login-form"
                >

                    <div className="input-group">

                        <Mail size={20} />

                        <input

                            type="email"

                            placeholder="E-mail"

                            value={email}

                            onChange={(e) =>

                                setEmail(e.target.value)

                            }

                            required

                        />

                    </div>

                    <div className="input-group">

                        <Lock size={20} />

                        <input

                            type="password"

                            placeholder="Senha"

                            value={senha}

                            onChange={(e) =>

                                setSenha(e.target.value)

                            }

                            required

                        />

                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                    >

                        <LogIn size={20} />

                        {

                            loading

                                ? "Entrando..."

                                : "Entrar"

                        }

                    </button>

                </form>

            </div>

        </main>

    );

}