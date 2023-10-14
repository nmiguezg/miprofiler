import styles from "./cards.module.css";
import PropTypes from "prop-types";

export default function InfoCard({ title, data, bigTitle=false }) {
    return (
        <div className={styles.card}>
            <p className={`${bigTitle && styles.title}`}>{title}</p>
            <h2 className={styles.data}>{data}</h2>
        </div >
    )
}

InfoCard.propTypes = {
    title: PropTypes.string.isRequired,
    data: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number
    ]).isRequired
};
