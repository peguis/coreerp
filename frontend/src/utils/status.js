export function badgeStatus(status) {

    const mapa = {

        ATIVO: "success",

        INATIVO: "danger",

        ABERTA: "warning",

        FINALIZADA: "success",

        CANCELADA: "danger",

        PAGO: "success",

        PENDENTE: "warning",

        ATRASADO: "danger",

        ENTRADA: "success",

        SAIDA: "danger",

        AJUSTE: "warning"

    };

    return mapa[status] || "default";

}