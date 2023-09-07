import { useLocation, Link } from "react-router-dom";

export default function User() {
    const location = useLocation();
    const { id, edad, genero, posts, collection, timestamp } = location.state;
    return (
        <>
            <div className="header"><h1>Información de usuario</h1>
                <Link to="/users">Volver</Link>
            </div>
            <article className="info-user">
                <div className="fields">
                    <p>Id: {id}</p>
                    <p>Edad: {edad}</p>
                    <p>Género: {genero}</p>
                    <p>Colección: {collection}</p>
                </div>
                <ol className="posts">
                    <div className="list-heading">Publicaciones</div>

                    {posts.map((post, index) => (
                        <li key={index} className="list-item">{'"' + post + '"'}</li>
                    ))}
                </ol>
            </article>
        </>
    )
}