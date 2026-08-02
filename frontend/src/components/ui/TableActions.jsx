import {
    Pencil,
    Trash2
} from "lucide-react";

import Button from "../forms/Button";

import "./TableActions.css";


export default function TableActions({

    onEdit,

    onDelete

}) {


    return (


        <div className="table-actions">


            <Button

                variant="secondary"

                onClick={onEdit}

                title="Editar"

            >

                <Pencil size={16} />


            </Button>





            <Button

                variant="danger"

                onClick={onDelete}

                title="Excluir"

            >

                <Trash2 size={16} />


            </Button>



        </div>


    );


}