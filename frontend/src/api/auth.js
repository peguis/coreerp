import api from "./axios";


export async function loginRequest(
    username,
    password
){

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
            headers:{
                "Content-Type":
                "application/x-www-form-urlencoded"
            }
        }
    );


    return response.data;

}