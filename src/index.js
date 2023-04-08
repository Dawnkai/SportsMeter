import { createRoot } from 'react-dom/client';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import MainPage from './components/MainPage/MainPage';
import './styles.css';

const theme = createTheme();

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
                <Routes>
                    <Route exact path="/" element={<MainPage/>}/>
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
