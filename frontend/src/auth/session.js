export function clearAuthSession(storage = globalThis.localStorage) {
    storage.removeItem("token");
    storage.removeItem("usuario");
}
