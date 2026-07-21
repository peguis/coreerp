import { createContext, useEffect, useState } from "react";


export const AuthContext = createContext();




export function AuthProvider({ children }) {


    const [token, setToken] = useState(null);



    useEffect(() => {


        const tokenSalvo =
            localStorage.getItem("token");


        if (tokenSalvo) {

            setToken(tokenSalvo);

        }


    }, []);





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

                login,

                logout

            }}

        >


            {children}


        </AuthContext.Provider>


    );


}