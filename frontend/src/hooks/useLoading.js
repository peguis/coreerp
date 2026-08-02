import { useState } from "react";

export default function useLoading(initial = false) {

    const [loading, setLoading] = useState(initial);

    function start() {

        setLoading(true);

    }

    function stop() {

        setLoading(false);

    }

    return {

        loading,

        start,

        stop

    };

}