import React from 'react';
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

export default function MainPage() {
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
                                <ListItem disablePadding>
                                    <ListItemButton>
                                        <ListItemText primary="Spring Games 2023"/>
                                    </ListItemButton>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemButton>
                                        <ListItemText primary="QUAFL 2022"/>
                                    </ListItemButton>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemButton>
                                        <ListItemText primary="Bayern-Liga '22/'23"/>
                                    </ListItemButton>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemButton>
                                        <ListItemText primary="Brooms Up 2022"/>
                                    </ListItemButton>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemButton>
                                        <ListItemText primary="DQM 2022"/>
                                    </ListItemButton>
                                </ListItem>
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
                                <MatchItem text="Team 1 vs Team 2"/>
                                <MatchItem text="Team 2 vs Team 3"/>
                                <MatchItem text="Team 4 vs Team 5"/>
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
                                <ListItem disablePadding>
                                    <ListItemText primary="Team 1 (2000 pts)"/>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemText primary="Team 2 (3000 pts)"/>
                                </ListItem>
                                <ListItem disablePadding>
                                    <ListItemText primary="Team 3 (500 pts)"/>
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    )
}
