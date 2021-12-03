import { Routes, Route } from 'react-router-dom';
import App from './pages/App';
import Results from './pages/Results/Results';
import YoutubeLink from './pages/YoutubeLink/YoutubeLink';

const Router = () => {

    return (
        <Routes>
            <Route path="/" element={<App />}/>
            <Route path="/youtube-link" element={<YoutubeLink/>}/>
            <Route path="/results" element={<Results/>}/>
        </Routes>
    )
}

export default Router;