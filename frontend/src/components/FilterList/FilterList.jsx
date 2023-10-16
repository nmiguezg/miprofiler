import PropTypes from "prop-types";
import styles from "./filterList.module.css";

export default function FilterList({ children }) {
    return (
        <ul className={styles.filterList}>
            {children}
        </ul>
    )
}

FilterList.propTypes = {
    children: PropTypes.node.isRequired,
};
