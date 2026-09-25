export function attachSessionToken(config, storage = globalThis.localStorage) {
    const token = storage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}
