import PropTypes from 'prop-types';
import styles from "./utils.module.css";

export default function Spinner({ condition, leaveSpace = true }) {
  const visibilityStyle = leaveSpace ? styles.invisible : styles.hidden;
  return (
    <div className={`${styles.spinner_container} ${!condition && visibilityStyle} `}>
      <div className={`${styles.spinner} `} >
      </div>
    </div>

  )
}

Spinner.propTypes = {
  condition: PropTypes.bool.isRequired,
  leaveSpace: PropTypes.bool,
};
