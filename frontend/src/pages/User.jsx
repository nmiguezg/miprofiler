import { useLocation } from "react-router-dom";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function User() {
    const [numPost, setNumPost] = useState(0);
    const location = useLocation();
    const { id, edad, genero, posts, collection, timestamp } = location.state;
    function nextPost() {
        setNumPost(Math.min(numPost + 1, posts.length));
    }
    function previousPost() {
        setNumPost(Math.max(numPost - 1, 0));
    }
    return (
        <div className="content">
            <div><h2>Información de usuario</h2>
                <Link to="/collection">Volver</Link>
            </div>
            <article className="info">
                <div className="fields">
                    <p>Id: {id}</p>
                    <p>Edad: {edad}</p>
                    <p>Género: {genero}</p>
                    <p>Colección: {collection}</p>
                </div>
                {/* <p>Fecha de subida: {timestamp */}
                <ol className="posts">
                <div className="list-heading">Posts</div>

                    {posts.map((post, index) => (
                        <li key={index} className="list-item">{'"' + post + '"'}</li>
                    ))}
                    {/* <p>{posts[numPost]}</p> */}
                    {/* <div className="buttons">
                        <button onClick={previousPost}>Anterior</button>
                        <button onClick={nextPost}>Siguiente</button>
                    </div> */}
                </ol>
            </article>
        </div>
    )
}