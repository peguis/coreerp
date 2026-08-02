export function formatarMoeda(valor) {

    return Number(valor ?? 0)
        .toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });

}



export function formatarData(valor) {

    if (!valor) {
        return "-";
    }


    return new Date(valor)
        .toLocaleDateString("pt-BR");

}



export function formatarDataHora(valor) {

    if (!valor) {
        return "-";
    }


    return new Date(valor)
        .toLocaleString("pt-BR");

}



// Compatibilidade com componentes antigos
export function formatCurrency(valor) {

    return formatarMoeda(valor);

}


export function formatDate(valor) {

    return formatarData(valor);

}