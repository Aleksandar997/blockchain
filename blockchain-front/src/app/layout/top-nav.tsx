import { AppBar, Toolbar, IconButton, Typography, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import React, { FC } from 'react';
import { IconHook } from '../common/icon-hook';
import * as menuOptions from "./../routing.json";
import { BrowserRouter as Router, Route, Link, RouteComponentProps } from 'react-router-dom';
import { Form, FormProps } from '../form';

const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
  }));

function initForm({ match }: any) {
  // return <Form/>
  console.log(match)
  return <Form menuCode="accounts" />
}

// const formComponent: FC<string> = (menuCode: string) => {
//   return <Form menuCode={menuCode}/>
// }

// const formComponent: FC = () => {
//   return <div></div>
// }

function TopNav() {
  const classes = useStyles();

  return (
    <Router>
      <AppBar position="static">
      <Toolbar>
          {
            menuOptions.menus.map(m => {
              const Icon = IconHook.hook(m.icon)  
              return (
                // <IconButton aria-label={m.name}>
                //   <Icon/>
                //   {m.name}
                // </IconButton>
                <Link to="/accounts">
                  <Button className='menu-button' startIcon={<Icon/>} size="large">
                    {m.name}
                  </Button>
                </Link>
              )
            })
          }
          {
            menuOptions.menus.map(m => {
              return (
                <Route path={m.route} exact component={initForm} />
              )
            })
          }
          {/* <Icon/>
          <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
          <MenuIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
          News
          </Typography>
          <Button color="inherit">Login</Button> */}
      </Toolbar>
      </AppBar>
    </Router>
  );
}

export default TopNav;
