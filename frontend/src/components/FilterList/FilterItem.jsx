import styles from "./filterList.module.css";
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export default function FilterItem({ name, value, action }) {
    return (
        <li className={styles["filter-item"]}>
            <span className={styles.filterIcon}>
                <i className={styles.icon}>
                    <HighlightOffIcon onClick={action} />
                </i>
            </span>
            <span className={styles.filterText}><b>{capitalizeFirstLetter(name)}:</b> {value}</span>
        </li>
    )
}
