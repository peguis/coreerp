export function shouldFetchAuthenticatedTenantIdentity(token, pathname) {
    return Boolean(token) && pathname !== "/login";
}
