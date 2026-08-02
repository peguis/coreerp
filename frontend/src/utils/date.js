export function formatDate(valor) {

    if (!valor) {
        return "-";
    }


    return new Date(valor)
        .toLocaleDateString("pt-BR");

}