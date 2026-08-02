export default function Avatar({

    nome

}) {

    return (

        <div className="avatar">

            {nome?.charAt(0)}

        </div>

    );

}