import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import {IMarket} from "../Markets"
import { Link } from 'react-router-dom';
export function MarketCard(props:IMarket){
      return (
        <Card className='h-fit w-fit' >
          <CardContent>
            <Typography gutterBottom sx={{ color: 'text.secondary', fontSize: 14 }}>
              {props.name}
            </Typography>
            <Typography variant="body2">
              {props.province}-{props.city}
            </Typography>
          </CardContent>
          <CardActions className='text-center item-center'>
            <Link to={"/market-detail/"+props.id} >
              <Button className='text-center' size="small">رزرو</Button>
            </Link>
          </CardActions>
        </Card>
      );
}