export function getErrorMessage(error, fallback) {

    const detail = error?.response?.data?.detail;

    if (Array.isArray(detail)) {

        return detail
            .map((item) => item.msg || item.message || String(item))
            .join(" ");

    }

    return detail || error?.message || fallback;

}
