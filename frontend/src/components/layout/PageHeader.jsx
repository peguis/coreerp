export default function PageHeader({ titulo, subtitulo }) {
    return (
        <div style={{ marginBottom: 30 }}>
            <h1
                style={{
                    fontSize: 34,
                    fontWeight: 700,
                    marginBottom: 6
                }}
            >
                {titulo}
            </h1>

            <p
                style={{
                    color: "#64748b",
                    fontSize: 16
                }}
            >
                {subtitulo}
            </p>
        </div>
    );
}