import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';

import DeleteIcon from '@mui/icons-material/Delete';

/*import MatchForm from './MatchForm';*/

import parseDate from '../../utils/parseDate';
import parseTime from '../../utils/parseTime';

export default function MatchDetails() {
    const { match_id } = useParams();
    const [ isEditing, setIsEditing ] = useState(false);
    const [ matchDetails, setMatchDetails ] = useState(
        {
            "match_id": 0, "team_a_name": "", "team_a_points": 0,
            "team_b_name": "", "team_b_points": 0, "match_date": "",
            "match_start_time": "", "match_end_time": ""
        }
    );
    const navigate = useNavigate();

    useEffect(() => {
        
    }, [])
    
    return (
        <>
            
        </>
    )
}