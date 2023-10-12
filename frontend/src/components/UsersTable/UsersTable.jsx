import { useEffect, useState } from "react";
import ProfilerService from "../../services/ProfilerService";
import styles from "./users.module.css"
import { useNavigate } from "react-router-dom";
import { Table, TableBody, TableCell, TableHead, TableRow } from "@material-ui/core";



const LIMIT = 5;

export default function UsersTable({ collId }) {
    const [users, setUsers] = useState(null);
    const [offset, setOffset] = useState(0);
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
                    <Table aria-errormessage="error-access">
                        <TableHead>
                            <TableRow>
                                <TableCell style={{ width: "10%" }}>Id</TableCell>
                                <TableCell style={{ width: "10%" }}>Edad</TableCell>
                                <TableCell style={{ widTableCell: "15%" }}>Género</TableCell>
                                <TableCell className={styles.prescindible}>Publicaciones</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {users?.map((user) => (
                                <TableRow key={user.id}
                                    className={styles.userRow}
                                    onClick={() => navigate("users/" + user.id, { state: user })}>
                                    <TableCell style={{ width: "10%" }}>
                                        {typeof user.id === "string" ? user.id.substring(0, 10) : user.id}
                                    </TableCell>
                                    <TableCell style={{ width: "10%" }}>{user.edad}</TableCell>
                                    <TableCell style={{ width: "15%" }}>{user.genero}</TableCell>
                                    <TableCell className={styles.prescindible} style={{ height: "4.5em" }}>
                                        {user.posts[0].length > 50 ?
                                            user.posts[0].substring(0, 50) + "..." : user.posts[0].padEnd(50, ' ')}
                                    </TableCell>
                                </TableRow>))}
                        </TableBody>
                    </Table>

                </div>
                <div className={styles.buttons}>
                    <button onClick={() => retrieveUsers(true)}>Anterior</button>
                    <button onClick={() => retrieveUsers()}>Siguiente</button>
                </div>
            </>
        </div>
    );
}
