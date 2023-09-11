import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Signup() {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    function handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        navigate("/auth")
    }
    return (
        <div className="content">
            <h1>BLM Profiler</h1>
            <form
                className="auth-form"
                encType="multipart/form-data"
                onSubmit={handleSubmit}
            >
                <div className="auth-fields">
                    <label>
                        Usuario
                        <input
                            type="text"
                            name="user"
                            required="True"
                            placeholder="user123">
                        </input>
                    </label>
                    <label>
                        Usuario
                        <input
                            type="text"
                            name="user"
                            required="True"
                            placeholder="user123">
                        </input>
                    </label>
                    <label>
                        Usuario
                        <input
                            type="text"
                            name="user"
                            required="True"
                            placeholder="user123">
                        </input>
                    </label>
                    <label>
                        Contraseña
                        <input
                            type="password"
                            name="password"
                            required="True"
                            placeholder="v5dLR74h">
                        </input>
                    </label>
                </div>
                <input
                    type="submit"
                    name="submit"
                    className="submit"
                    value="Iniciar sesión">
                </input>
            </form>
        </div>
    );
}
