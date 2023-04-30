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
import DeleteIcon from '@mui/icons-material/Delete';

import { useNavigate } from 'react-router-dom';

export default function MatchDetails() {
    const { match_id } = useParams();
    const [ isEditing, setIsEditing ] = useState(false);
    const [ matchDetails, setMatchDetails ] = useState({"match_id": 0, "match_title": "", "season_title": ""});
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMatchDetails = async () => {
            try {
                const result = await axios(`/api/matches/${match_id}`);
                setMatchDetails(result?.data);
            }
            catch (error) {
                console.log(error);
                navigate("/");
            }
        }
        fetchMatchDetails();
    }, []);

    const Demo = styled('div')(({ theme }) => ({
        backgroundColor: theme.palette.background.paper,
    }));

    const deleteMatch = (event) => {
        event.preventDefault();
        axios.delete(`/api/matches/${match_id}`, {})
        .then((response) => {
            if (response?.status == 201) navigate("/");
        })
        .catch((error) => {
            console.log(error);
            navigate("/");
        });
    }

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
                                        secondary={matchDetails?.match_id}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Team A"
                                        secondary={matchDetails?.team_a_name}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Team A points"
                                        secondary={matchDetails?.team_a_points}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Team B"
                                        secondary={matchDetails?.team_b_name}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Team B points"
                                        secondary={matchDetails?.team_b_points}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Match date"
                                        secondary={matchDetails?.match_date}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Match start time"
                                        secondary={matchDetails?.match_start_time}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Match end time"
                                        secondary={matchDetails?.match_end_time}
                                    />
                                </ListItem>
                            </List>
                        </Demo>
                        {/* <Button
                            variant="contained"
                            color="secondary"
                            onClick={() => setIsEditing(true)}
                        >
                            Edit
                        </Button> */}
                        <Button
                            variant="contained"
                            color="error"
                            onClick={(e) => deleteMatch(e)}
                            startIcon={<DeleteIcon/>}
                        >
                            Delete
                        </Button>
                        <Button
                            variant="contained"
                            color="neutral"
                            onClick={() => navigate("/")}
                        >
                            Cancel
                        </Button>
                    </Grid>
                </Grid>
            }
        </>
    )
}
