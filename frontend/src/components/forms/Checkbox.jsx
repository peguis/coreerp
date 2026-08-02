import "./Checkbox.css";


export default function Checkbox({

    label,

    checked,

    onChange

}) {


    return (

        <label className="checkbox-container">


            <input

                type="checkbox"

                checked={checked}

                onChange={onChange}

            />


            <span className="checkbox-label">

                {label}

            </span>


        </label>

    );

}