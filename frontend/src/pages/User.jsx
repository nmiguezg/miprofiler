import { useLocation, Link } from "react-router-dom";
import styles from "./styles/user.module.css"

export default function User() {
    const location = useLocation();
    const { id, edad, genero, posts } = location.state;
    return (
        <>
            <div className={styles.header}><h1>Información de usuario</h1>
                <Link to={-1}>Volver</Link>
            </div>
            <article className={styles.infoUser}>
                <div className={styles.fields}>
                    <p>Id: {id}</p>
                    <p>Edad: {edad}</p>
                    <p>Género: {genero}</p>
                </div>
                <ol className={styles.posts}>
                    <div className={styles.listHeading}>Publicaciones</div>

                    {posts.map((post, index) => (
                        <li key={index} className={styles.listItem}>{/*"«" + */post/* + "»"*/}</li>
                    ))}
                </ol>
            </article>
        </>
    )
}