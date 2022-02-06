import { Routes, Route } from 'react-router-dom';
import App from './pages/App';
import EmailResults from './pages/EmailResults/EmailResults';
import VideoUpload from './pages/Submission/VideoUpload';

const Router = () => {

    return (
        <Routes>
            <Route path="/" element={<App />}/>
            <Route path="/email-results" element={<EmailResults/>}/>
            <Route path="/submission" element={<VideoUpload/>}/>
        </Routes>
    )
}

export default Router;
