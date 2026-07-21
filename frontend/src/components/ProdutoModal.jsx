import { Link } from "react-router-dom";


function ProdutoModal({ produto, fechar }) {


    if (!produto)
        return null;



    function imagemProduto() {


        if (
            produto.imagens &&
            produto.imagens.length > 0
        ) {


            const principal =
                produto.imagens.find(
                    imagem => imagem.principal
                )
                ||
                produto.imagens[0];


            return `http://127.0.0.1:8000/${principal.caminho}`;

        }


        return null;

    }




    return (

        <div

            style={{

                position: "fixed",

                top: 0,

                left: 0,

                width: "100%",

                height: "100%",

                background: "rgba(0,0,0,0.5)",

                display: "flex",

                justifyContent: "center",

                alignItems: "center"

            }}

        >



            <div

                style={{

                    background: "white",

                    padding: 30,

                    borderRadius: 10,

                    width: 400

                }}

            >



                <h2>
                    {produto.nome}
                </h2>




                {
                    imagemProduto()

                    &&

                    <img

                        src={imagemProduto()}

                        width="200"

                        height="200"

                        style={{
                            objectFit: "cover"
                        }}

                    />

                }





                <p>

                    Categoria:
                    {" "}
                    {produto.categoria || "-"}

                </p>



                <p>

                    Marca:
                    {" "}
                    {produto.marca || "-"}

                </p>



                <p>

                    Código:
                    {" "}
                    {produto.codigo_interno || "-"}

                </p>




                <p>

                    Preço:

                    {" "}
                    R$ {Number(produto.preco).toFixed(2)}

                </p>




                <p>

                    Estoque:

                    {" "}
                    {produto.estoque}

                </p>




                <p>

                    Descrição:

                    {" "}
                    {produto.descricao || "-"}

                </p>





                <Link
                    to={`/produtos/${produto.id}`}
                >

                    <button>
                        Editar
                    </button>


                </Link>





                <button

                    onClick={fechar}

                    style={{
                        marginLeft: 10
                    }}

                >

                    Fechar

                </button>




            </div>



        </div>

    );

}


export default ProdutoModal;