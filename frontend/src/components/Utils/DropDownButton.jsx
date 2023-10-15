import styles from "./dropdown.module.css";
import PropTypes from 'prop-types';

export default function DropDownButton({ name, options, handleSelection }) {
    function handleClick(e) {
        e.preventDefault();
        handleSelection(e.target.innerHTML);
    }
    return (
        <div className={styles.dropdown}>
            <button className={styles.dropbtn}>{name}</button>
            <div className={styles['dropdown-content']}>
                {options.map((option, index) => (
                    <a role="button" key={index} className={styles.option} onClick={handleClick}>{option}</a>
                ))}
            </div>
        </div>
    )
}

DropDownButton.propTypes = {
    name: PropTypes.string.isRequired,
    options: PropTypes.array.isRequired,
    handleSelection: PropTypes.func.isRequired,
};