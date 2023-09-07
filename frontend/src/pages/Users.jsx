import { useEffect, useState } from "react";
import ProfileService from "../services/ProfileService";
import "./Users.css"
import { Link, useNavigate } from "react-router-dom";

const LIMIT = 6;

export default function Users() {
    const [users, setUsers] = useState(null);
    const [offset, setOffset] = useState(0);
    const navigate = useNavigate();

    function retrieveUsers(back = false) {
        const newOffset = back ? Math.max(offset - LIMIT, 0) : offset + LIMIT;
        ProfileService.getUsers(LIMIT, newOffset).then((data) => { setUsers(data['usuarios']) });
        setOffset(newOffset);
    }
    useEffect(() => {
        ProfileService.getUsers(LIMIT, 0).then((data) => { setUsers(data['usuarios']) });
    }, []);
    return (
        <>
            <article className="info-users">
                <h1>Usuarios</h1>
                {users != null ? (
                    <>
                        <div className="pagination">
                            <table className="table" aria-errormessage="error-access">
                                <thead>
                                    <tr>
                                        <th style={{ width: "10%" }}>Id</th>
                                        <th style={{ width: "10%" }}>Edad</th>
                                        <th style={{ width: "15%" }}>Género</th>
                                        <th>Publicaciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users?.map((user) => (
                                        <tr key={user.id} className="user-row" onClick={() => navigate("/users/" + user.id, { state: user })}>
                                            <th style={{ width: "10%" }}>{user.id}</th>
                                            <th style={{ width: "10%" }}>{user.edad}</th>
                                            <th style={{ width: "15%" }}>{user.genero}</th>
                                            <th style={{ height: "4.5em" }}
                                            >{user.posts[0].length > 100 ? user.posts[0].substring(0, 100) + "..." : user.posts[0].padEnd(100, ' ')}</th>                                        </tr>))}
                                </tbody>
                            </table>

                        </div>
                        <div className="buttons">
                            <button onClick={() => retrieveUsers(true)}>Anterior</button>
                            <button onClick={() => retrieveUsers()}>Siguiente</button>
                        </div>
                    </>
                ) : (
                    <>
                        <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus usuarios.</p>
                        <Link to="/">Volver</Link>
                    </>
                )}
            </article>
        </>
    );
}
