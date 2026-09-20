import { useState } from "react";

import { AuthContext } from "./AuthContextValue";




export function AuthProvider({ children }) {


    const [token, setToken] = useState(() =>
        localStorage.getItem("token")
    );

    const [carregando] = useState(false);






    function login(novoToken) {


        localStorage.setItem(

            "token",

            novoToken

        );


        setToken(novoToken);


    }






    function logout() {


        localStorage.removeItem(

            "token"

        );


        setToken(null);


    }







    const autenticado =
        Boolean(token);







    return (


        <AuthContext.Provider

            value={{


                token,

                autenticado,

                carregando,

                login,

                logout


            }}

        >


            {children}


        </AuthContext.Provider>


    );

}
