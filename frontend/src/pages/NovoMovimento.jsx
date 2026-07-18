import { useState } from "react";
import { useNavigate } from "react-router-dom";


import {
    criarMovimento
} from "../services/estoqueService";


function NovoMovimento() {


    const navigate = useNavigate();


    const [produtoId, setProdutoId] = useState("");
    const [tipo, setTipo] = useState("ENTRADA");
    const [quantidade, setQuantidade] = useState("");
    const [observacao, setObservacao] = useState("");



    async function salvar(e) {

        e.preventDefault();


        await criarMovimento({

            produto_id: Number(produtoId),

            tipo,

            quantidade: Number(quantidade),

            observacao

        });


        navigate("/estoque");

    }



    return (

        <div style={{ display: "flex" }}>



            <main style={{ padding: 30 }}>


                <h1>
                    Nova Movimentação
                </h1>



                <form onSubmit={salvar}>


                    <label>
                        Produto ID
                    </label>

                    <br />

                    <input
                        value={produtoId}
                        onChange={
                            e => setProdutoId(e.target.value)
                        }
                    />


                    <br /><br />


                    <label>
                        Tipo
                    </label>

                    <br />


                    <select
                        value={tipo}
                        onChange={
                            e => setTipo(e.target.value)
                        }
                    >

                        <option value="ENTRADA">
                            Entrada
                        </option>


                        <option value="SAIDA">
                            Saída
                        </option>


                        <option value="AJUSTE">
                            Ajuste
                        </option>


                    </select>



                    <br /><br />


                    <label>
                        Quantidade
                    </label>

                    <br />


                    <input
                        type="number"
                        value={quantidade}
                        onChange={
                            e => setQuantidade(e.target.value)
                        }
                    />



                    <br /><br />



                    <label>
                        Observação
                    </label>


                    <br />


                    <input

                        value={observacao}

                        onChange={
                            e => setObservacao(e.target.value)
                        }

                    />



                    <br /><br />


                    <button>
                        Salvar
                    </button>



                </form>


            </main>


        </div>

    );

}


export default NovoMovimento;