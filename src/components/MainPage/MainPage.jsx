import React, { useState, useEffect } from 'react';
import axios from 'axios';

import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

import AddMatchDialog from './AddMatchDialog';
import EventItem from './EventItem';
import MatchItem from './MatchItem';

export default function MainPage() {
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
        } catch(error) {
            console.log(error);
        }
    }

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

    useEffect(() => {
        fetchSeasons();
        fetchEvents();
    }, []);    

    return (
        <Box m={3}>
            <Grid container spacing={2}>
                <Grid item xs={3}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                Seasons
                            </Typography>
                            <Divider/>
                            <List>
                                {
                                    seasons.map((season) => 
                                        <ListItem disablePadding key={season?.season_id}>
                                            <ListItemButton>
                                                <ListItemText 
                                                    primary={season?.season_title} 
                                                    onClick={(event) => {
                                                        event.preventDefault();
                                                        fetchSeasonInfo(event?.currentTarget.id);
                                                    }} 
                                                    id={`${season?.season_id}`}
                                                />
                                            </ListItemButton>
                                        </ListItem>
                                    )
                                }
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                Matches
                            </Typography>
                            <Divider/>
                            <Stack spacing={2}>
                                {
                                    matches.map((match) => 
                                    <MatchItem 
                                        key={match?.match_id} 
                                        match_id={match?.match_id}
                                        team_a={match?.team_a_name}
                                        team_b={match?.team_b_name}
                                        team_a_points={match?.team_a_points}
                                        team_b_points={match?.team_b_points}
                                    />)
                                }
                            </Stack>
                            {/* { selectedSeason && <Button
                                type="submit"
                                variant="contained"
                                color="success"
                                startIcon={<AddIcon/>}
                                onClick={() => setAddMatchDialogOpen(true)}
                            >
                                Add new match
                            </Button>} */}
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={3}>
                    <Stack spacing={2}>
                        <Card variant="outlined">
                            <CardContent>
                                <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                    Leaderboard
                                </Typography>
                                <Divider/>
                                <List>
                                    {
                                        highscore.map((score) => 
                                            <ListItem disablePadding key={score?.team_id}>
                                                <ListItemText 
                                                    primary={`${score?.team_name} (${score?.team_score} pts)`}
                                                />
                                            </ListItem>
                                        )
                                    }
                                </List>
                            </CardContent>
                        </Card>
                        <Card variant="outlined">
                            <CardContent>
                                <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                    Upcoming events
                                </Typography>
                                <Divider/>
                                <List>
                                    {
                                        events.slice(0,2).map((event) =>
                                            <ListItem disablePadding key={event.event_id}>
                                                <EventItem 
                                                    event_title={event.event_title}
                                                    event_description={event.event_description}
                                                />
                                            </ListItem>
                                        )
                                    }
                                </List>
                            </CardContent>
                        </Card>
                    </Stack>
                </Grid>
            </Grid>
            <AddMatchDialog 
                isOpen={addMatchDialogOpen}
                handleClose={handleModalClose}
                selectedSeason={selectedSeason}
            />
        </Box>
    )
}
