import React, { useState, useEffect } from 'react';
import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
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
import Button from '@mui/material/Button';

import MatchItem from './MatchItem';
import AddMatchDialog from './AddMatchDialog';
import axios from 'axios';

export default function MainPage() {
    const [seasons, setSeasons] = useState([]);
    const [selectedSeason, setSelectedSeason] = useState(null);
    const [matches, setMatches] = useState([]);
    const [highscore, setHighscore] = useState([]);
    const [addMatchDialogOpen, setAddMatchDialogOpen] = useState(false);

    const fetchSeasons = async () => {
        const result = await axios('/api/seasons');
        setSeasons(result.data);
    }

    const fetchSeasonInfo = (seasonId) => {
        if (seasonId === null) return;
        axios.get(`/api/seasons/${seasonId}/matches`).then((response) => {
            setMatches(response.data);
        });
        axios.get(`/api/seasons/${seasonId}/highscore`).then((response) => {
            setHighscore(response.data);
        });
        setSelectedSeason(seasonId);
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
                                        <ListItem disablePadding key={season.season_id}>
                                            <ListItemButton>
                                                <ListItemText 
                                                    primary={season.season_title} 
                                                    onClick={(event) => {
                                                        event.preventDefault();
                                                        fetchSeasonInfo(event.currentTarget.id);
                                                    }} 
                                                    id={`${season.season_id}`}
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
                                        text={match.match_title} 
                                        key={match.match_id} 
                                        match_id={match.match_id}
                                    />)
                                }
                            </Stack>
                            { selectedSeason && <Button
                                type="submit"
                                variant="contained"
                                color="success"
                                startIcon={<AddIcon/>}
                                onClick={() => setAddMatchDialogOpen(true)}
                            >
                                Add new match
                            </Button>}
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
            <AddMatchDialog isOpen={addMatchDialogOpen} handleClose={handleModalClose} selectedSeason={selectedSeason}/>
        </Box>
    )
}
