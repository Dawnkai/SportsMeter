import React from 'react';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';

const StyledItem = styled(Paper)(({theme}) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#FFF',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

export default function MatchItem({text}) {
    return (
        <StyledItem>{text}</StyledItem>
    );
}
