import { Link } from "react-router-dom";

const botoes = [
    {
        titulo: "Nova Venda",
        rota: "/vendas/nova",
        icone: "🛒"
    },
    {
        titulo: "Novo Produto",
        rota: "/produtos",
        icone: "📦"
    },
    {
        titulo: "Novo Cliente",
        rota: "/clientes",
        icone: "👤"
    },
    {
        titulo: "Financeiro",
        rota: "/financeiro",
        icone: "💰"
    }
];

export default function QuickActions() {

    return (

        <div
            style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
                gap: 16
            }}
        >

            {

                botoes.map(botao => (

                    <Link
                        key={botao.titulo}
                        to={botao.rota}
                        style={{
                            textDecoration: "none",
                            background: "#2563eb",
                            color: "#fff",
                            padding: 20,
                            borderRadius: 14,
                            textAlign: "center",
                            fontWeight: 600,
                            transition: ".2s"
                        }}
                    >

                        <div
                            style={{
                                fontSize: 34,
                                marginBottom: 10
                            }}
                        >
                            {botao.icone}
                        </div>

                        {botao.titulo}

                    </Link>

                ))

            }

        </div>

    );

}