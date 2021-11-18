import { useState } from 'react';
import styles from '../YoutubeLink/YoutubeLink.module.css'

const YoutubeLink = () => {

    const [errorText, setErrorText] = useState('<Error Text Here>');
    const [email, setEmail] = useState('');
    const [link, setLink] = useState('');

    const handleSubmit = () => {
        //Validate email and link

        //Call rs.py 

        //Update display to success page
        setErrorText("Button was Clicked!");
        console.log('here');
    }


    return (
        <div className={styles.image}>
            <div className={styles.contentBox}>
                <h1 className={styles.title}>Count from Youtube Link</h1>
                <h4 className={styles.subtitle}>Enter a Youtube link to the emergence count and an email
                to send the results to when the count is completed</h4>

                <div className={styles.forms}>
                    <div className={styles.formRow}>
                        <h3 className={styles.identifier}>Link: </h3>
                        <input className={styles.input} onChange={(e) => setLink(e.target.value)}></input>
                    </div>
                    <div className={styles.formRow}>
                        <h3 className={styles.identifier}>Email: </h3>
                        <input className={styles.input} onChange={(e) => setEmail(e.target.value)}></input>
                    </div>
                </div>

                <button className={styles.submitButton} onClick={handleSubmit}>Submit</button>
                <p className={styles.errorText}>{errorText}</p>
            </div>
        </div>
    )
};

export default YoutubeLink;