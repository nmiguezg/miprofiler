import { useEffect, useState } from "react";
import ProfileService from "../services/ProfileService";
import "./Users.css"
import { Link } from "react-router-dom";

const LIMIT = 5;

export default function Users() {
    const [users, setUsers] = useState(null);
    const [offset, setOffset] = useState(0);

    function retrieveUsers(back = false) {
        const newOffset = back ? Math.max(offset - LIMIT, 0) : offset + LIMIT;
        ProfileService.getUsers(LIMIT, newOffset).then((data) => { setUsers(data['usuarios']) });
        setOffset(newOffset);
    }
    useEffect(() => {
        ProfileService.getUsers(LIMIT, 0).then((data) => { setUsers(data['usuarios']) });
    }, []);
    return (
        <div className="content">
            <article className="info">
                <h2>Usuarios</h2>
                {users != null ? (
                    <div className="pagination">
                        <table className="table" aria-errormessage="error-access">
                            <thead>
                                <tr>
                                    <th style={{ width: "10%" }}>Id</th>
                                    <th style={{ width: "10%" }}>Edad</th>
                                    <th style={{ width: "15%" }}>Género</th>
                                    <th>Posts</th>
                                    <th style={{ width: "15%" }}></th>

                                </tr>
                            </thead>
                            <tbody>
                                {users?.map((user) => (
                                    <tr key={user.id}>
                                        <th style={{ width: "10%" }}>{user.id}</th>
                                        <th style={{ width: "10%" }}>{user.edad}</th>
                                        <th style={{ width: "15%" }}>{user.genero}</th>
                                        <th style={{ height: "4.5em" }}
                                        >{user.posts[0].length > 100 ? user.posts[0].substring(0, 100) + "..." : user.posts[0].padEnd(100, ' ')}</th>
                                        <th ><Link to={"/collection/" + user.id} state= {user}> Ver usuario</Link></th>
                                    </tr>))}
                            </tbody>
                        </table>
                        <div className="buttons">
                            <button onClick={() => retrieveUsers(true)}>Anterior</button>
                            <button onClick={() => retrieveUsers()}>Siguiente</button>
                        </div>
                    </div>
                ) : (
                    <>
                        <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus usuarios.</p>
                        <Link to="/">Volver</Link>
                    </>
                )}
            </article>
        </div>
    );
}
