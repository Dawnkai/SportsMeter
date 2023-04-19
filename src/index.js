import { createRoot } from 'react-dom/client';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import CssBaseline from '@mui/material/CssBaseline';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

import MainPage from './components/MainPage/MainPage';
import MatchDetails from './components/MatchDetails/MatchDetails';
import NavigationBar from './components/NavigationBar';
import SignInPage from './components/Login/SignInPage';
import SignUpPage from './components/Login/SignUpPage';

import './styles.css';

const theme = createTheme({
    palette: {
        neutral: {
            main: '#64748B',
            contrastText: '#fff',
        },
    }
});

const Copyright = () => {
    return (
        <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
                Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    )
}

const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>
            <BrowserRouter>
                <NavigationBar/>
                <Routes>
                    <Route exact path="/" element={<MainPage/>}/>
                    <Route path="/matches/:match_id" element={<MatchDetails/>}/>
                    <Route path="/login" element={<SignInPage/>}/>
                    <Route path="/register" element={<SignUpPage/>}/>
                </Routes>
            </BrowserRouter>
            <Copyright/>
        </ThemeProvider>
    );
}

const root = createRoot(document.getElementById('root'));
root.render(
    <App/>
)
