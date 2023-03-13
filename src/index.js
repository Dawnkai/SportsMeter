import { useState, useEffect, StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import Example from './Example';

const App = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/api')
        .then((res) => res.json())
        .then((data) => {
            setData(data['response']);
        });
    }, []);

    return <Example value={data} />;
}

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <App/>
    </StrictMode>
)
