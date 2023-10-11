import { useEffect, useState } from "react";
import ProfilerService from "../../services/ProfilerService";
import styles from "./users.module.css"
import { Link, useNavigate } from "react-router-dom";

const LIMIT = 5;

export default function Users() {
    const [users, setUsers] = useState(null);
    const [offset, setOffset] = useState(0);
    const collId = sessionStorage.getItem('collId');
    const navigate = useNavigate();

    function retrieveUsers(back = false) {
        const newOffset = back ? Math.max(offset - LIMIT, 0) : offset + LIMIT;
        ProfilerService.findUsers(collId, LIMIT, newOffset)
            .then((data) => {
                setUsers(data);
                setOffset(newOffset);
            });
    }
    useEffect(() => {
        ProfilerService.findUsers(collId, LIMIT, 0)
            .then((data) => { data && setUsers(data) });
    }, []);

    if (users == null) {
        return (
            <>
                <p>Todavía no hay usuarios perfilados, perfila una colección para poder ver sus usuarios.</p>
            </>
        )
    }
    return (
        <div className={styles.infoUsers}>
            <>
                <div className={styles.pagination}>
                    <table aria-errormessage="error-access">
                        <thead>
                            <tr>
                                <th style={{ width: "10%" }}>Id</th>
                                <th style={{ width: "10%" }}>Edad</th>
                                <th style={{ width: "15%" }}>Género</th>
                                <th className={styles.prescindible}>Publicaciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users?.map((user) => (
                                <tr key={user.id}
                                    className={styles.userRow}
                                    onClick={() => navigate("/users/" + user.id, { state: user })}>
                                    <th style={{ width: "10%" }}>
                                        {typeof user.id === "string" ? user.id.substring(0, 10) : user.id}
                                    </th>
                                    <th style={{ width: "10%" }}>{user.edad}</th>
                                    <th style={{ width: "15%" }}>{user.genero}</th>
                                    <th className={styles.prescindible} style={{ height: "4.5em" }}>
                                        {user.posts[0].length > 50 ?
                                            user.posts[0].substring(0, 50) + "..." : user.posts[0].padEnd(50, ' ')}
                                    </th>
                                </tr>))}
                        </tbody>
                    </table>

                </div>
                <div className={styles.buttons}>
                    <button onClick={() => retrieveUsers(true)}>Anterior</button>
                    <button onClick={() => retrieveUsers()}>Siguiente</button>
                </div>
            </>
        </div>
    );
}
