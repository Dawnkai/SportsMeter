import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';

import MatchForm from './MatchForm';
import { Button } from '@mui/material';

export default function MatchDetails() {
    const { match_id } = useParams();
    const [ isEditing, setIsEditing ] = useState(false);
    const [ matchDetails, setMatchDetails ] = useState({"match_id": 0, "match_title": "", "season_title": ""});

    useEffect(() => {
        const fetchMatchDetails = async () => {
            const result = await axios(`/api/matches/${match_id}`);
            setMatchDetails(result.data);
        }
        fetchMatchDetails();
    }, []);

    const Demo = styled('div')(({ theme }) => ({
        backgroundColor: theme.palette.background.paper,
    }));

    return (
        <>
            <Typography variant="h1">Match details</Typography>
            {
                isEditing ?
                <MatchForm setMatchDetails={setMatchDetails} setIsEditing={setIsEditing}/>
                :
                <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                        <Typography sx={{ mt: 4, mb: 2 }} variant="h6" component="div">
                            Details for match of id: {match_id}
                        </Typography>
                        <Demo>
                            <List dense={true}>
                                <ListItem>
                                    <ListItemText
                                        primary="Match ID"
                                        secondary={matchDetails.match_id}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Match title"
                                        secondary={matchDetails.match_title}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Season title"
                                        secondary={matchDetails.season_title}
                                    />
                                </ListItem>
                            </List>
                        </Demo>
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={() => setIsEditing(true)}
                        >
                            Edit
                        </Button>
                    </Grid>
                </Grid>
            }
        </>
    )
}
