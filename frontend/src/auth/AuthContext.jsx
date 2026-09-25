import { useState } from "react";

import { AuthContext } from "./AuthContextValue";
import { clearAuthSession } from "./session";




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
        clearAuthSession();
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
