import { Routes, Route } from 'react-router-dom';
import App from './pages/App';
import YoutubeLink from './pages/YoutubeLink/YoutubeLink';

const Router = () => {

    return (
        <Routes>
            <Route path="/" element={<App />}/>
            <Route path="/youtube-link" element={<YoutubeLink/>}/>
        </Routes>
    )
}

export default Router;