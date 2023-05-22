import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

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
import ButtonIcons from '@mui/icons-material'
import DeleteIcon from '@mui/icons-material/Delete';

/*import MatchForm from './MatchForm';*/

import parseDate from '../../utils/parseDate';
import parseTime from '../../utils/parseTime';

export default function MainLobby() {
    const { match_id } = useParams();
    const [ isEditing, setIsEditing ] = useState(false);
    const [ matchDetails, setMatchDetails ] = useState(
        {
            "match_id": 0, "team_a_name": "", "team_a_points": 0,
            "team_b_name": "", "team_b_points": 0, "match_date": "",
            "match_start_time": "", "match_end_time": ""
        }
    );
    
    /*const fetchTeams = async () => {
        try {
            const result = await axios('/api/teams');
            setSeasons(result?.data);
        } catch (error) {
            console.log(error);
        }
    }
    
    useEffect(() => {
        fetchTeams();
    }, []);*/

    const BorderBox = ({ children }) => {
        return (
            <Box
                sx={{
                    border: '1px solid',
                    borderRadius: '4px',
                    borderColor: 'lightgrey',
                    padding: '4px',
                    m: 2,
                }}
            >
                {children}
            </Box>
        );
    }

    const navigate = useNavigate();

    useEffect(() => {
        
    }, [])

    return (
        <>
            {/* score */}
            <BorderBox>
                <Grid container spacing={3}>
                    {/* Team A name, logo and color */}
                    <Grid item xs={3}>
                        <Typography sx={{textAlign:'left', m:2}}>
                            Poznań Capricorns
                        </Typography>
                    </Grid>
                    {/* Score in the middle */}
                    <Grid item xs={6}>
                        <Grid container spacing={5}>
                            <Grid item xs={2}>
                            <IconButton aria-label="snitch_catch">
                                <SportsGolf/>
                            </IconButton>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={3}>
                        {/* Team B name, logo and color */}
                        <Typography sx={{textAlign:'right', m:2}}>
                            Łódź Pirates
                        </Typography>
                    </Grid>
                </Grid>
            </BorderBox>

            {/* People in lobby and timer */}
            <BorderBox>
                
            </BorderBox>

            {/* Statistics*/}
            <BorderBox>
                
            </BorderBox>

            {/* Plan substitutions and add cards */}
            <BorderBox>
                
            </BorderBox>

            {/* Add players box */}
            <BorderBox>
                
            </BorderBox>

        </>
    )
}