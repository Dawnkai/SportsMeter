import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
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
import SportsGolf from '@mui/icons-material/SportsGolf';
import AddCircle from '@mui/icons-material/AddCircle';
import RemoveCircle from '@mui/icons-material/RemoveCircle';
import InsertDriveFile from '@mui/icons-material/InsertDriveFile';

import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Stopwatch from './Stopwatch';

/*import MatchForm from './MatchForm';*/

import parseDate from '../../utils/parseDate';
import parseTime from '../../utils/parseTime';

export default function MainLobby() {
    const { match_id } = useParams();
    const [isEditing, setIsEditing] = useState(false);
    const [matchDetails, setMatchDetails] = useState(
        {
            "match_id": 0, "team_a_name": "", "team_a_points": 0,
            "team_b_name": "", "team_b_points": 0, "match_date": "",
            "match_start_time": "", "match_end_time": ""
        }
    );
    const [team_a_score, setTeam_a_score] = useState(0); //add if statement for <0
    const [team_b_score, setTeam_b_score] = useState(0);

    const SnitchCatch = (team_snitch) => {
        if (team_snitch == "a") {
            setTeam_a_score((prevTeam_a_score) => prevTeam_a_score + 30);
        }
        else if (team_snitch == "b") {
            setTeam_b_score((prevTeam_b_score) => prevTeam_b_score + 30);
        }
        return false;
    }

    /*const fetchTeams = async () => {
        try {
            const result = await axios('/api/teams');
            setSeasons(result?.data);
        } catch (error) {
            console.log(error);
        }
    }
    */

    /* DATA FOR STATISTICS: */
    function createData(number, name, shots, passes, tackles, defenses, turnovers, beats, catches) {
        return { number, name, shots, passes, tackles, defenses, turnovers, beats, catches };
    }

    const rows = [
        createData(12, 'Jan Nowak', 0, 0, 0, 0, 0, 0, 0),
        createData(5, 'Joanna Kowalska', 0, 0, 0, 0, 0, 0, 0),
        createData(2, 'Marcin Cośtam', 0, 0, 0, 0, 0, 0, 0),
        createData(5, 'Michał Darkowski', 0, 0, 0, 0, 0, 0, 0),
        createData(22, 'Anna Mowrońska', 0, 0, 0, 0, 0, 0, 0),
        createData(42, 'Aleksandra Mostewska', 0, 0, 0, 0, 0, 0, 0),
    ];





    useEffect(() => {
        SnitchCatch();
    }, []);

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
            {/************************************************ Users in the lobby *****************************************************************************/}
            <BorderBox>
                <List>
                    <ListItem>
                        <Grid container spacing={2}>
                            <Grid item xs={11}>
                                <Typography sx={{ textAlign: 'left', m: 0, fontSize: 18 }}>
                                    Users in the Lobby:
                                </Typography>
                            </Grid>
                            <Grid item xs={1} sx={{ display: 'flex', justifyContent: 'right' }}>
                                <Button
                                    variant="contained"
                                    color="neutral"
                                    onClick={() => navigate("/")}
                                >
                                    Exit
                                </Button>
                            </Grid>
                        </Grid>
                    </ListItem>
                    <Divider />
                    {/*************  Users: ***************/}
                    <Grid>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        Admin1
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    <SportsGolf />
                                </Grid>
                            </Grid>
                        </ListItem>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        User1
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>

                                </Grid>
                            </Grid>
                        </ListItem>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        User2
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>

                                </Grid>
                            </Grid>
                        </ListItem>
                    </Grid>
                </List>
            </BorderBox>

            {/******************************************************************** Score ***************************************************************/}
            <BorderBox>
                <Grid container spacing={3}>
                    {/* Team A name, logo and color */}
                    <Grid item xs={3}>
                        <Typography sx={{ textAlign: 'left', m: 2 }}>
                            Poznań Capricorns
                        </Typography>
                    </Grid>
                    {/* Score in the middle */}
                    <Grid item xs={6}>
                        <Grid container spacing={5}>
                            {/* Team A snitch catch */}
                            <Grid item xs={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton onClick={() => SnitchCatch("a")}
                                    aria-label="snitch_catch_A" sx={{ backgroundColor: 'gold', m: 2, '&:hover': { backGroundColor: 'yellow', }, }}>
                                    <SportsGolf />
                                </IconButton>
                            </Grid>
                            {/* Team A score buttons */}
                            <Grid item xs={2}>
                                <List spacing={0}>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_a_score((prevTeam_a_score) => prevTeam_a_score + 10)}
                                            aria-label="add_points_A"
                                            sx={{ backgroundColor: 'green', m: 1, '&:hover': { backGroundColor: 'darkGreen', }, }}>
                                            <AddCircle />
                                        </IconButton>
                                    </ListItem>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_a_score((prevTeam_a_score) => prevTeam_a_score - 10)}
                                            aria-label="remove_points_A"
                                            sx={{ backgroundColor: 'red', m: 1, '&:hover': { backGroundColor: 'darkRed', }, }}>
                                            <RemoveCircle />
                                        </IconButton>
                                    </ListItem>
                                </List>
                            </Grid>
                            {/* SCORE */}
                            <Grid item xs={4} sx={{ fontSize: 72 }} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {team_a_score}:{team_b_score}
                            </Grid>
                            {/* Team B score buttons */}
                            <Grid item xs={2}>
                                <List spacing={0}>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_b_score((prevTeam_b_score) => prevTeam_b_score + 10)}
                                            aria-label="add_points_A"
                                            sx={{ backgroundColor: 'green', m: 1, '&:hover': { backGroundColor: 'darkGreen', }, }}>
                                            <AddCircle />
                                        </IconButton>
                                    </ListItem>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_b_score((prevTeam_b_score) => prevTeam_b_score - 10)}
                                            aria-label="remove_points_A"
                                            sx={{ backgroundColor: 'red', m: 1, '&:hover': { backGroundColor: 'darkRed', }, }}>
                                            <RemoveCircle />
                                        </IconButton>
                                    </ListItem>
                                </List>
                            </Grid>
                            {/* Team B snitch catch */}
                            <Grid item xs={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton onClick={() => SnitchCatch("b")}
                                    aria-label="snitch_catch_B" sx={{ backgroundColor: 'gold', m: 2, '&:hover': { backGroundColor: 'yellow', }, }}>
                                    <SportsGolf />
                                </IconButton>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={3}>
                        {/* Team B name, logo and color */}
                        <Typography sx={{ textAlign: 'right', m: 2 }}>
                            Łódź Pirates
                        </Typography>
                    </Grid>
                </Grid>
            </BorderBox>

            {/************************************************** Timer ***************************************************************/}
            <BorderBox>
                {/*<StopWatch/>*/}
            </BorderBox>

            {/*********************************************** Statistics ***********************************************************************/}
            <BorderBox>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Name</TableCell>
                                <TableCell align="right">Shots</TableCell>
                                <TableCell align="right">Passes</TableCell>
                                <TableCell align="right">Tackles</TableCell>
                                <TableCell align="right">Defenses</TableCell>
                                <TableCell align="right">Turnovers</TableCell>
                                <TableCell align="right">Beats</TableCell>
                                <TableCell align="right">Catches</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.map((row) => (
                                <TableRow
                                    key={row.name}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                        {row.number}
                                        {" | "}
                                        {row.name}
                                    </TableCell>
                                    <TableCell align="right">{row.shots}</TableCell>
                                    <TableCell align="right">{row.passes}</TableCell>
                                    <TableCell align="right">{row.tackles}</TableCell>
                                    <TableCell align="right">{row.defenses}</TableCell>
                                    <TableCell align="right">{row.turnovers}</TableCell>
                                    <TableCell align="right">{row.beats}</TableCell>
                                    <TableCell align="right">{row.catches}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </BorderBox>

            <Grid container spacing={3}>
                {/********************************************* Plan substitutions ************************************************************/}
                <Grid item xs={6}>
                    <BorderBox>
                    <Grid container spacing={2} m={0} sx={{display: 'flex', alignItems: 'center'}}>
                        <Grid item xs={3}>
                            Plan Substitutions:
                        </Grid>
                        <Grid item xs={4} sx={{padding: '10px'}}>
                            <Button
                            variant="contained"
                            color="success">
                                Execute
                            </Button>
                        </Grid>
                        <Grid item xs={4} sx={{ textAlign: 'right', fontSize: 12, color: 'red'}}>
                            Warning
                        </Grid>
                    </Grid>
                    <Divider/>
                    <Grid container spacing={3} sx={{paddingLeft: "16px"}}>
                        <Grid item xs={3}>
                            Player 1
                        </Grid>
                        <Grid item xs={3}>
                            -
                        </Grid>
                        <Grid item xs={3}>
                            Player 2
                        </Grid>
                    </Grid>
                    <Grid container spacing={3} sx={{paddingLeft: "16px"}}>
                        <Grid item xs={3}>
                            Player 5
                        </Grid>
                        <Grid item xs={3}>
                            -
                        </Grid>
                        <Grid item xs={3}>
                            Player 6
                        </Grid>
                    </Grid>
                    <Divider/>
                    <Grid container spacing={2} m={0}>
                        <Grid item xs={8}>
                            
                        </Grid>
                        <Grid item xs={4}>
                        <Button
                            variant="contained"
                            color="success">
                                New Substitution
                            </Button>
                        </Grid>
                    </Grid>
                    </BorderBox>
                </Grid>
                {/********************************************* Add cards ************************************************************/}
                <Grid item xs={6}>
                <BorderBox>
                    <Grid container spacing={2} m={0} sx={{display: 'flex', alignItems: 'center'}}>
                        <Grid item xs={3}>
                            Add cards:
                        </Grid>
                        <Grid item xs={3}>
                            <IconButton 
                                            aria-label="blue_card"
                                            sx={{ backgroundColor: 'lightblue', m: 1, '&:hover': { backGroundColor: 'Blue', }, }}>
                                            <InsertDriveFile/>
                            </IconButton>
                            <IconButton 
                                            aria-label="yellow_card"
                                            sx={{ backgroundColor: 'yellow', m: 1, '&:hover': { backGroundColor: 'darkYellow', }, }}>
                                            <InsertDriveFile/>
                            </IconButton>
                            <IconButton 
                                            aria-label="red_card"
                                            sx={{ backgroundColor: 'red', m: 1, '&:hover': { backGroundColor: 'darkRed', }, }}>
                                            <InsertDriveFile/>
                            </IconButton>
                        </Grid>
                    </Grid>
                    <Divider/>
                    <Grid container spacing={3} sx={{display: 'flex', alignItems: 'center'}}>
                        <Grid item xs={6} sx={{marginLeft: "16px"}}>
                            Player 3
                        </Grid>
                        <Grid item xs={2}>
                            00:23
                        </Grid>
                        <Grid item xs={2} sx={{padding: "6px"}}>
                        <Button sx={{marginTop: "6px"}}
                            variant="contained"
                            color="success">
                                Release 2
                            </Button>
                        </Grid>
                    </Grid>
                    </BorderBox>
                </Grid>
            </Grid>
            {/***************************************************** Add players box ************************************************************/}
            <BorderBox>

            </BorderBox>

        </>
    )
}