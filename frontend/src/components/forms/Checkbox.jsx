import "./Checkbox.css";


export default function Checkbox({

    label,

    checked,

    onChange,

    disabled = false

}) {


    return (

        <label className="checkbox-container">


            <input

                type="checkbox"

                checked={checked}

                onChange={onChange}

                disabled={disabled}

            />


            <span className="checkbox-label">

                {label}

            </span>


        </label>

    );

}
