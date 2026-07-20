import { useState } from "react";
import api from "../api/axios";


function UploadImagemProduto({ produtoId, atualizar }) {

    const [arquivo, setArquivo] = useState(null);
    const [enviando, setEnviando] = useState(false);


    async function enviarImagem(e) {

        e.preventDefault();

        if (!arquivo)
            return;


        const formData = new FormData();

        formData.append(
            "arquivo",
            arquivo
        );


        try {

            setEnviando(true);


            await api.post(
                `/produtos/${produtoId}/imagem`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );


            setArquivo(null);


            if (atualizar)
                atualizar();


        } finally {

            setEnviando(false);

        }

    }



    return (

        <form onSubmit={enviarImagem}>


            <input

                type="file"

                accept="image/*"

                onChange={
                    e => setArquivo(e.target.files[0])
                }

            />


            <button
                type="submit"
                disabled={enviando}
            >

                {
                    enviando
                        ?
                        "Enviando..."
                        :
                        "Enviar imagem"
                }

            </button>


        </form>

    );

}


export default UploadImagemProduto;