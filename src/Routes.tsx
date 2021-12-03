import { Routes, Route } from 'react-router-dom';
import App from './pages/App';
<<<<<<< HEAD
import Results from './pages/Results/Results';
import YoutubeLink from './pages/YoutubeLink/YoutubeLink';
=======
import EmailResults from './pages/EmailResults/EmailResults';
>>>>>>> e1d56eb7efd329b1ca44360cd6c2268875e48df5

const Router = () => {

    return (
        <Routes>
            <Route path="/" element={<App />}/>
<<<<<<< HEAD
            <Route path="/youtube-link" element={<YoutubeLink/>}/>
            <Route path="/results" element={<Results/>}/>
=======
            <Route path="/email-results" element={<EmailResults/>}/>
>>>>>>> e1d56eb7efd329b1ca44360cd6c2268875e48df5
        </Routes>
    )
}

export default Router;