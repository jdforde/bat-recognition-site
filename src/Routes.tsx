import { Routes, Route } from 'react-router-dom';
import App from './pages/App';

import EmailResults from './pages/EmailResults/EmailResults';


const Router = () => {

    return (
        <Routes>
            <Route path="/" element={<App />}/>
            <Route path="/email-results" element={<EmailResults/>}/>
        </Routes>
    )
}

export default Router;