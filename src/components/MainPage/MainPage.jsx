import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';

import MatchItem from './MatchItem';
import axios from 'axios';

export default function MainPage() {
    const [seasons, setSeasons] = useState([]);
    const [matches, setMatches] = useState([]);
    const [highscore, setHighscore] = useState([]);

    useEffect(() => {
        const fetchSeasons = async () => {
            const result = await axios('/api/seasons');
            setSeasons(result.data);
        }
        fetchSeasons();
    }, []);

    const fetchSeasonInfo = (event) => {
        event.preventDefault();
        axios.get(`/api/seasons/${event.currentTarget.id}/matches`).then((response) => {
            setMatches(response.data);
        });
        axios.get(`/api/seasons/${event.currentTarget.id}/highscore`).then((response) => {
            setHighscore(response.data);
        });
    }

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
                                        <ListItem disablePadding key={season.id}>
                                            <ListItemButton>
                                                <ListItemText primary={season.title} onClick={fetchSeasonInfo} id={`${season.id}`}/>
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
                                    matches.map((match) => <MatchItem text={match.title} key={match.id}/>)
                                }
                            </Stack>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={3}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                Scoreboard
                            </Typography>
                            <Divider/>
                            <List>
                                {
                                    highscore.map((score) => 
                                        <ListItem disablePadding key={score.team_id}>
                                            <ListItemText primary={`${score.team_name} (${score.team_score} pts)`}/>
                                        </ListItem>
                                    )
                                }
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    )
}
