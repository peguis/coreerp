import { Search } from "lucide-react";

import "./SearchInput.css";

export default function SearchInput({

    value,

    onChange,

    placeholder = "Pesquisar..."

}) {

    return (

        <div className="search-input">

            <Search size={18} />

            <input

                value={value}

                onChange={onChange}

                placeholder={placeholder}

            />

        </div>

    );

}