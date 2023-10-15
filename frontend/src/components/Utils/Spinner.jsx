import PropTypes from 'prop-types';
import styles from "./utils.module.css";

export default function Spinner({ condition }) {
  return (
    <div className={styles.spinner_container}>
      <div className={`${styles.spinner} ${!condition && styles.hidden}`} >
      </div>
    </div>

  )
}

Spinner.propTypes = {
  condition: PropTypes.bool.isRequired
};
