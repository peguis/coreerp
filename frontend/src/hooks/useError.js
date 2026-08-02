import { useState } from "react";

export default function useError() {

    const [error, setError] = useState("");

    function clear() {

        setError("");

    }

    return {

        error,

        setError,

        clear

    };

}