import api from "./axios";



export async function loginRequest(
    username,
    password
) {


    const form = new URLSearchParams();


    form.append(
        "username",
        username
    );


    form.append(
        "password",
        password
    );



    const response = await api.post(

        "/usuarios/login",

        form,

        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded"
            }
        }

    );



    if (response.data.access_token) {


        localStorage.setItem(

            "token",

            response.data.access_token

        );


    }



    return response.data;


}





export function logout() {


    localStorage.removeItem(
        "token"
    );


    window.location.href =
        "/login";


}





export function estaLogado() {


    const token =
        localStorage.getItem("token");


    return Boolean(token);


}