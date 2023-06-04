import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import axios from 'axios';

import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

import AddMatchDialog from './AddMatchDialog';
import EventItem from './EventItem';
import MatchItem from './MatchItem';
import MainLobby from './MainLobby';
import { grey } from '@mui/material/colors';
import { BorderColor } from '@mui/icons-material';

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

export default function LobbySetup() {
    const [seasons, setSeasons] = useState([]);
    const [selectedSeason, setSelectedSeason] = useState(null);
    const [matches, setMatches] = useState([]);
    const [highscore, setHighscore] = useState([]);
    const [events, setEvents] = useState([]);
    const [addMatchDialogOpen, setAddMatchDialogOpen] = useState(false);

    const fetchSeasons = async () => {
        try {
            const result = await axios('/api/seasons');
            setSeasons(result?.data);
        } catch (error) {
            console.log(error);
        }
    }

    const fetchEvents = async () => {
        try {
            const result = await axios('/api/events');
            setEvents(result?.data);
        } catch (error) {
            console.log(error);
        }
    }

    {/**check axios documentation*/}
    const fetchSeasonInfo = (seasonId) => {
        if (seasonId === null) return;
        try {
            axios.get(`/api/seasons/${seasonId}/matches`).then((response) => {
                setMatches(response?.data);
            });
            axios.get(`/api/seasons/${seasonId}/highscore`).then((response) => {
                setHighscore(response?.data);
            });
            setSelectedSeason(seasonId);
        } catch (error) {
            console.log(error);
        }
    }

    const handleModalClose = (refetchSeasons = false) => {
        if (refetchSeasons) {
            fetchSeasons();
            fetchSeasonInfo(selectedSeason);
        }
        setAddMatchDialogOpen(false);
    }

    const BorderBox = ({ children }) => {
        return (
            <Box
                sx={{
                    border: '1px solid',
                    borderRadius: '4px',
                    borderColor: 'lightgrey',
                    padding: '12px',
                    mt: 2,
                    mb: 2,
                }}
            >
                {children}
            </Box>
        );
    }

    useEffect(() => {
        fetchSeasons();
        fetchEvents(0);
        fetchSeasonInfo(0);
    }, []);

    const navigate = useNavigate();

    return (
        
        <BorderBox m={4}>
            <Typography>Hi world!</Typography>
        </BorderBox>
    )
}
