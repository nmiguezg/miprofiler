import { useLocation, Link } from "react-router-dom";
import styles from "./styles/user.module.css"
import InfoCard from "@/components/Cards/InfoCard";

export default function User() {
    const location = useLocation();
    const { id, edad, genero, posts } = location.state;
    return (
        <>
            <div className={styles.header}><h1>Información de usuario</h1>
                <Link to={-1}>Volver</Link>
            </div>
            <article className={styles.infoUser}>
                <div className={styles.cards}>
                    <InfoCard title="Id" data={id} bigTitle/>
                    <InfoCard title="Edad" data={edad} bigTitle />
                    <InfoCard title="Género" data={genero} bigTitle />
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