import { useEffect, useRef, useState } from "react";

export const DEFAULT_DELAY = 180;
export const DEFAULT_MIN_DURATION = 280;

export function useLoadingVisibility(loading, options = {}) {
    const delay = options.delay ?? DEFAULT_DELAY;
    const minDuration = options.minDuration ?? DEFAULT_MIN_DURATION;
    const [visible, setVisible] = useState(false);
    const visibleAt = useRef(0);

    useEffect(() => {
        const timers = [];

        if (loading) {
            timers.push(window.setTimeout(() => {
                visibleAt.current = 0;
                setVisible(false);
            }, 0));
            timers.push(window.setTimeout(() => {
                visibleAt.current = Date.now();
                setVisible(true);
            }, delay));
        } else {
            const elapsed = visibleAt.current ? Date.now() - visibleAt.current : minDuration;
            timers.push(window.setTimeout(() => {
                visibleAt.current = 0;
                setVisible(false);
            }, Math.max(minDuration - elapsed, 0)));
        }

        return () => timers.forEach((timer) => window.clearTimeout(timer));
    }, [delay, loading, minDuration]);

    return visible;
}
