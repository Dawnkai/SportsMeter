import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


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

import AddMatchDialog from '../MainPage/AddMatchDialog';
import EventItem from '../MainPage/EventItem';
import MatchItem from '../MainPage/MatchItem';
import MainLobby from '../MatchLobby/MainLobby';
import { grey } from '@mui/material/colors';
import { BorderColor, CenterFocusStrong } from '@mui/icons-material';

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
    const [teams, setTeams] = useState([]);
    const [addMatchDialogOpen, setAddMatchDialogOpen] = useState(false);

    const [teamA, setTeamA] = React.useState('');
    const [teamB, setTeamB] = React.useState('');

    const handleTeamA = (event) => {
        setTeamA(event.target.value);
    };
    const handleTeamB = (event) => {
        setTeamB(event.target.value);
    };


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

    {/**check axios documentation*/ }
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

    const fetchTeams = () => {
        try {
            const result = axios.get('/api/teams/');
            setTeams(result?.data);
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
                    padding: '42px',
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
        fetchTeams();
        fetchEvents(0);
        fetchSeasonInfo(0);
    }, []);

    const navigate = useNavigate();

    return (
        
            <Grid container spacing={3}>
                <Grid item xs={3}>

                </Grid>
                
                <Grid item xs={6}>
                <BorderBox>
                    <Grid container spacing={3}>
                        <Grid xs={5}>
                            <Box sx={{ minWidth: 80 }}>
                                <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label2">Team A</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-label2"
                                        id="demo-simple-select2"
                                        value={teamA}
                                        label="Team A"
                                        onChange={handleTeamA}
                                    >
                                        <MenuItem value={10}>Player 5</MenuItem>
                                        <MenuItem value={20}>Player 6</MenuItem>
                                        <MenuItem value={30}>Player 7</MenuItem>
                                    </Select>
                                </FormControl>
                            </Box>
                        </Grid>
                        <Grid xs={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Typography sx>VS</Typography>
                        </Grid>
                        <Grid xs={5}>
                        <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label2">Team B</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-label2"
                                        id="demo-simple-select2"
                                        value={teamB}
                                        label="Team B"
                                        onChange={handleTeamB}
                                    >
                                        <MenuItem value={10}>Player 5</MenuItem>
                                        <MenuItem value={20}>Player 6</MenuItem>
                                        <MenuItem value={30}>Player 7</MenuItem>
                                    </Select>
                                </FormControl>
                        </Grid>
                    </Grid>
                    <Box sx={{ display: 'flex', alignItems: 'right', justifyContent: 'right', marginTop: '22px', }}>
                    <Button 
                    variant="contained"
                    color="success">
                        Start Lobby
                    </Button>
                    </Box>
                    
                    </BorderBox>
                </Grid>
                
                <Grid item xs={3}>

                </Grid>
            </Grid>

    )
}
