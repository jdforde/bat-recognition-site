import { useState } from 'react';
import styles from '../EmailResults/EmailResults.module.css'

const EmailResults = () => {

    const [errorText, setErrorText] = useState('');
    const [file, setFile] = useState(new Object());
    const [date, setDate] = useState(new Date());
    const [email, setEmail] = useState('');
    const [success, setSuccess] = useState(false);
    const emailRegex = new RegExp(/^\S+@\S+\.\S+$/);

    const HandleSubmit = () => {
        if (file === null || email === '' || date === new Date()) {
            setErrorText("Please fill out all fields");
            return;
        }

        if (!emailRegex.test(email)) {
            setErrorText("Enter a valid email address");
            return;
        }


        //Call endpoint for downloading
        //Call endpoint for rs.py
        console.log(file);


        setErrorText('');
        setSuccess(true);
    }

    const HandleSubmitAgain = () => {
        setFile(new Object);
        setDate(new Date());
        setEmail('');
        setSuccess(false);
    }


    //Look into making this transition smooth
    return (
        !success ? 
            <div className={styles.image}>
                <div className={styles.contentBox}>
                    <h1 className={styles.title}>Count with Email</h1>
                    <h4 className={styles.subtitle}>Please enter your email, the date of the count recording, and the count file</h4>

                    <div className={styles.forms}>
                        <div className={styles.formRow}>
                            <h3 className={styles.identifier}>Email: </h3>
                            <input className={styles.input} onChange={(e) => setEmail(e.target.value)}></input>
                        </div>
                        <div className={styles.formRow}>
                            <h3 className={styles.identifier}>File Upload:</h3>
                            <input onChange={(e) => setFile(e.target.files![0])} className={styles.chooseFile}type="file" id="myFile" name="filename"></input>
                        </div>
                        <div className={styles.formRow}>
                            <h3 className={styles.identifier}>Date Recorded:</h3><input className={styles.date} type="date" onChange={(e) => setDate(new Date(Date.parse(e.target.value)))} id="filedate"></input>
                        
                        </div>

                    </div>

                    <button className={styles.submitButton} onClick={HandleSubmit}>Submit</button>
                    <p className={styles.errorText}>{errorText}</p>
                </div>
            </div>
            :
            <div className={styles.image}>
            <div className={styles.contentBox}>
                <br/><br/><br/><br/>

                <h1 className={styles.title}>Success!</h1>
                <h4 className={styles.subtitle}> When the processing is done, you will receive an email with the results. Click the button 
                below if you would like to submit another video.</h4>

            

                <button className={styles.submitButton} onClick={(HandleSubmitAgain)}>Submit</button>
                <p className={styles.errorText}>{errorText}</p>
            </div>
        </div>

    )
};

export default EmailResults;