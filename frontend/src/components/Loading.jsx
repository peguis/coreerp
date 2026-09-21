import { LoadingState } from "./loading/LoadingPrimitives";

export default function Loading({ texto = "Carregando dados...", ...props }) {
    return <LoadingState {...props} message={texto} />;
}
