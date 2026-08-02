export default function useConfirm() {

    function confirm(texto) {

        return window.confirm(texto);

    }

    return confirm;

}